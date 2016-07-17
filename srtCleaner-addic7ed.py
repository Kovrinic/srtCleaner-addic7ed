#!/usr/bin/env python

import argparse
import traceback
import os
import re

class srtcleaner(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='srtCleaner-addic7ed', description='Clean "Addic7ed" from srt files.')

        self.parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
        self.parser.add_argument('srt', help='Parse input.')
        self.parser.add_argument('-d', action='store_true', help='Specify a Directory to clean all the srt files within.')
        self.parser.add_argument('-r', action='store_true', help='Recursively parse directories. Used with "-d".')
        self.parser.add_argument('-n', action='store_true', help='Run in test mode. Do not save output.')
        self.parser.add_argument('-v', action='store_true', help='Run in Verbose mode. Outputs extra information.')
        self.parser.add_argument('-s', action='store_true', help='Run Silently. Squash all output including errors.')

        self.args = self.parser.parse_args()
        self.skip = False
        self.arg_handler()

    def arg_handler(self):
        if self.args.d:
            return self.input_dir()
        return self.input_file(self.args.srt)

    def input_file(self, srt_input):
        file_path = os.path.abspath(srt_input)
        if not os.path.exists(file_path):
            raise argparse.ArgumentTypeError('File \"%s\" does not exist!' %file_path)
        elif os.path.isdir(file_path):
            raise argparse.ArgumentTypeError('\"%s\" is a directory. Please use the "-d" flag for directory input.' %file_path)

        if not self.args.s:
            print('Cleaning "Addic7ed" from %s' %srt_input)

        if not self.remove_addic7ed(file_path):
            if not self.args.s:
                print('\"%s\" Skipped due to unknow error.' %srt_input)
        return

    def input_dir(self):
        dir_path = os.path.abspath(self.args.srt)
        if not os.path.exists(dir_path):
            raise argparse.ArgumentTypeError('Direcotry \"%s\" does not exist!' %dir_path)
        elif os.path.isfile(dir_path):
            raise argparse.ArgumentTypeError('Expected directory but found file \"%s\".' %dir_path)

        if self.args.r:
            if not self.args.s:
                print('Parsing \"%s\" recursively' %self.args.srt)
            srt_file_list = list()
            for r, d, filenames in os.walk(dir_path):
                for filename in filenames:
                    if filename.endswith('.srt'):
                        srt_file_list.append(os.path.join(r, filename))
        else:
            srt_file_list = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(".srt")]

        if not srt_file_list:
            raise argparse.ArgumentTypeError('Skipping. No \".srt\" files found within \"%s\".' %dir_path)

        return [self.input_file(f) for f in srt_file_list]

    def del_addic7ed(self, data):
        matches = re.findall(r'(?m)^(\d+\r\n(?:.+\r\n.+)+addic7ed.+\r\n+(?:\r\n)?)', data)
        self.skip = False
        if len(matches) == 0:
            self.skip = True
            if not self.args.s:
                print('Skipping: No addic7ed info in current data set.')
            return data
        for m in matches:
            if self.args.v and not self.args.s:
                print('Removing lines -->')
                print(m)
            data = data.replace(m, '')
        return data

    def update_index(self, data):
        matches = re.findall(r'(?m)^(\d+\r\n)', data)
        for i, m in enumerate(matches):
            data = re.sub(r'(?m)^(%s)' %m, r'%i\r\n' %(i+1), data)
        return data

    def load_srt(self, path):
        data = None
        try:
            with open(path, 'r') as f:
                data = f.read()
        except Exception as e:
            if not self.args.s:
                print('Load Error: %s' %str(e))
                traceback.print_exc()
            else:
                pass
        return data

    def save_srt(self, path, data):
        try:
            with open(path+'new', 'w') as f:
                f.write(''.join(data).strip())
        except Exception as e:
            if not self.args.s:
                print('Save Error: %s' %str(e))
                traceback.print_exc()
            else:
                pass
            return False
        return True

    def remove_addic7ed(self, file_path):
        data = self.load_srt(file_path)
        if data:
            data = self.del_addic7ed(data)
            data = self.update_index(data)
            if self.args.n:
                return True
            elif self.skip:
                return True
            if not self.save_srt(file_path, data):
                return False
            return True
        return False

# Run the script :D
srtcleaner()

import argparse
from collections import namedtuple
import csv
from datetime import datetime
import os
import re
import sys


INPUT_FILE_NAME = 'screen_scrape.txt'
OUTPUT_FILE_NAME = 'grid_search.csv'
PROJECT_DIR = '/Users/rotobi/Projects/udacity/deep-reinforcement-learning/p2_continuous-control'

def parse_argv(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help="file to be parsed")
    args = parser.parse_args()
    # print(args)
    if args.file_name:
        print("file_name given")
    return args

def change_dir(project_dir):
    os.chdir(project_dir)
    print('Changed working directory to {}.'.format(os.getcwd()))

def read_file(file_name):
    print('Reading in file {}...'.format(file_name))
    with open(file_name) as f:
        content = f.readlines()
        print('... read in {} lines.'.format(len(content)))

        lines = []
        for line in content:
            words = line.split()
            lines.append(words)
            # print(line)
            # print(words)
            
        # print(lines)
    return lines

def parse_lines(lines):
    print('Parsing {} lines...'.format(len(lines)))

    data = []  # will be a collection of entries
    
    fields = ('id', 'buffer_size', 'batch_size', 'learn_rate', 'max_t',
                'neurons', 'episodes', 'avg_score', 'time')

    create_empty_entry = lambda : {key: None for key in fields}  # Create a dict for a single data entry
    entry = None
    
    # Entry = namedtuple('Entry', fields)
    # Entry.__new__.__defaults__ = (None,) * len(Entry._fields)

    for line in lines:
        
        if line is None or not line:
            # print('Found None or empty line, skipping...')
            continue

        if line[0] == 'IOPub' or \
            (line[0] == 'The' and line[1] == 'notebook') or \
            (line[0] == 'to' and line[1] == 'the') or \
            (line[0] == 'To' and line[1] == 'change') or \
            (line[0] == 'Current' and line[1] == 'values:') or \
            'NotebookApp' in line[0]:
            continue

        elif line[0] == 'Testing':
            entry = create_empty_entry()
            entry['id'], _ = re.findall(r"[\d']+", line[3])

        elif 'Combination' in line[0]:
            get_number = lambda x: x.split('=')[1][:-1]
            
            entry['buffer_size'] = int(get_number(line[0]))
            entry['batch_size'] = int(get_number(line[1]))
            entry['learn_rate'] = float(get_number(line[2]))
            entry['max_t'] = int(get_number(line[3]))
            entry['neurons'] = int(get_number(line[4]))
        
        elif 'Episode' in line[0]:
            if line[2] == 't:':
                # Ignore this
                continue
            else:
                entry['episodes'] = line[1][:-1]
                entry['avg_score'] = float(line[4])
                avg_score_improvement = float(line[5][1:-2])
                entry['time'] = datetime.strptime(line[9], '%H:%M:%S.%f')
        
        elif 'Saving' in line[0] or 'aborting' in line[9]:
            # Add entry to data
            if entry:
                data.append(entry)
                entry = None
        
        else:
            print("!!!Don't know how to handle this!!!")
            assert False
    
    print_statistics(data)
    print('... done parsing data.')
    return data

def print_statistics(data):
    print('... identified {} entries in data!'.format(len(data)))

def write_to_csv(data, file_name):
    print('Writing data to CSV file {}'.format(file_name))
    keys = data[0].keys()
    with open(file_name, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print('... wrote data to {}'.format(file_name))

def main(argv):
    # args = parse_argv(argv)
    change_dir(PROJECT_DIR)
    lines = read_file(INPUT_FILE_NAME)
    data = parse_lines(lines)
    write_to_csv(data, OUTPUT_FILE_NAME)

if __name__ == "__main__":
    main(sys.argv[1:])

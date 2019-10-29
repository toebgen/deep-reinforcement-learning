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

    lines = []
    with open(file_name) as f:
        content = f.readlines()

        for line in content:
            words = line.split()
            lines.append(words)

    print('... read in {} lines.'.format(len(lines)))
    return lines

def parse_lines(lines):
    """
    Parse lines one by one, extracting the information.
    """
    print('Parsing {} lines...'.format(len(lines)))

    data = []  # will be a collection of entries
    
    # Define format of data, in the form of entry
    fields = ('id', 'buffer_size', 'batch_size', 'learn_rate', 'max_t',
                'neurons', 'episodes', 'avg_score', 'time')
    create_empty_entry = lambda : {key: None for key in fields}
    entry = None
    
    for line in lines:
        
        if line is None or not line or \
            line[0] == 'IOPub' or \
            (line[0] == 'The' and line[1] == 'notebook') or \
            (line[0] == 'to' and line[1] == 'the') or \
            (line[0] == 'To' and line[1] == 'change') or \
            (line[0] == 'Current' and line[1] == 'values:') or \
            (line[0] == 'CPU' and line[1] == 'times:') or \
            (line[0] == 'Wall' and line[1] == 'time:') or \
            'NotebookApp' in line[0]:
            continue

        elif line[0] == 'Testing':
            # New run starts here, prepare the next entry
            entry = create_empty_entry()
            entry['id'], _ = re.findall(r"[\d']+", line[3])
            entry['id'] = int(entry['id'])

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
                entry['episodes'] = int(line[1][:-1])
                entry['avg_score'] = float(line[4])
                avg_score_improvement = float(line[5][1:-2])
                entry['time'] = datetime.strptime(line[9], '%H:%M:%S.%f')
        
        elif 'Saving' in line[0] or 'aborting' in line[9]:
            # Add entry to data
            if entry:
                id_exists_already = next((item for item in data if item['id'] == entry['id']), None)
                if id_exists_already is None:
                    data.append(entry)
                    entry = None
                else:
                    assert False, "Entry with ID is already in data! {}".format(id_exists_already)
        
        else:
            assert False, "!!!Don't know how to handle this line!!! >>> {}".format(line)
    
    print_statistics(data)
    print('... done parsing data.')
    return data

def print_statistics(data):
    print('... identified {} entries in data!'.format(len(data)))

def write_to_csv(data, file_name):
    """
    Write data to CSV file with a header line, containing of the keys of
    the entry dictionary
    """
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

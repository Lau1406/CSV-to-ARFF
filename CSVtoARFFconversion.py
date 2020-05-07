###############
# CSV to ARFF #
###############
from argparse import ArgumentParser
import sys
import csv

parser = ArgumentParser()
parser.add_argument(
    '-in',
    '-input',
    '-csv',
    dest='csv_file',
    help='The input csv file location',
    metavar='FILE',
    required=True
)
parser.add_argument(
    '-out',
    '-output',
    '-arff',
    dest='output_file',
    help='The output arff file location',
    metavar='FILE',
    required=True
)
parser.add_argument(
    '-d',
    '-delimiter',
    dest='delimiter',
    default=',',
    help='If you need a different delimiter from the default comma',
    metavar='STRING',
    required=False,
    choices=[',', ':', ';', '?', ' ']
)

args = parser.parse_args()


class Convert(object):
    content = []
    name = ''
    lookup = [
        'nominal',
        'numeric',
        'string',
        'date',
    ]

    def __init__(self):
        self.csv = args.csv_file
        self.arff = args.output_file
        self.parse_args()

        self.parse_csv()
        self.arff_output()
        print('\nFinished.')

    def get_input(self, name: str) -> str:
        print('Is the type of ' + name, end='')
        for i in range(len(self.lookup)):
            if i == 0:
                print(' ' + self.lookup[i] + '[' + str(i) + ']', end='')
            elif i == len(self.lookup) - 1:
                # Last entry
                print(' or ' + self.lookup[i] + '[' + str(i) + ']?')
            else:
                print(', ' + self.lookup[i] + '[' + str(i) + ']', end='')
        return input()

    def parse_args(self):
        if not self.csv.endswith('.csv'):
            sys.exit('Input file not specified correctly, missing .csv')
        if not self.arff.endswith('.arff'):
            sys.exit('Output file not specified correctly, missing .arff')

    # import CSV
    def parse_csv(self):

        # remove .csv
        if self.csv.endswith('.csv'):
            self.name = self.csv.replace('.csv', '')
            
        print('Opening CSV file.')
        try:
            with open(self.csv) as csvfile:
                lines = csv.reader(csvfile, delimiter=args.delimiter)
                for row in lines:
                    self.content.append(row)
            csvfile.close()
            
        # just in case user tries to open a file that doesn't exist
        except IOError:
            print('File not found.\n')
            self.parse_csv()
            
    # export ARFF
    def arff_output(self):
        print('Converting to ARFF file.\n')
        if '/' in self.csv:
            parts = self.csv.split('/')
        elif '\\' in self.csv:
            parts = self.csv.split('\\')
        else:
            parts = [self.csv]

        title = str(parts[len(parts)-1][:-4])
        new_file = open(self.arff, 'w')

        ##
        # following portions formats and writes to the new ARFF file
        ##

        # write relation
        new_file.write('@relation ' + title + '\n\n')

        # get attribute type input
        for i in range(len(self.content[0])):
            choice = None
            while choice is None:
                choice = self.get_input(self.content[0][i])
                try:
                    choice = self.lookup[int(choice)]
                except (ValueError, IndexError) as e:
                    choice = None
                    print('Not a valid option, please try again')

            # Choice is a valid choice
            new_file.write('@attribute ' + str(self.content[0][i]) + ' ' + choice + '\n')

        # create list for class attribute
        last = len(self.content[0])
        class_items = []
        for i in range(len(self.content)):
            name = self.content[i][last-1]
            if name not in class_items:
                class_items.append(self.content[i][last-1])
            else:
                pass  
        del class_items[0]
    
        string = '{' + ','.join(sorted(class_items)) + '}'
        new_file.write('@attribute ' + str(self.content[0][last-1]) + ' ' + str(string) + '\n')

        # write data
        new_file.write('\n@data\n')

        del self.content[0]
        for row in self.content:
            new_file.write(','.join(row) + '\n')

        # close file
        new_file.close()


run = Convert()

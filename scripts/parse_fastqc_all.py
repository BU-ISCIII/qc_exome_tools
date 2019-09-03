


import argparse
import sys
import re
import csv
import pickle
import os

'''
Example of terminal command with arguments for execution of this script in Exome pipeline:
 
>>>python3 parse_fastqc_all.py -p "/home/masterbioinfo/EXOME/Data/fastqc/" -s _R1.fastq.gz _R2.fastq.gz .trimmed_R1.fastq .trimmed_R2.fastq -t  pre_R1 pre_R2 post_R1 post_R2  -c  "/home/masterbioinfo/EXOME/Results/dic_fastqc_stats_all.csv" -b "/home/masterbioinfo/EXOME/Results/dic_fastqc_stats_all.bn"

'''
#################
### FUNCTIONS ###
#################


def check_arg (args=None) :

    '''
	Description:
        Function collect arguments from command line using argparse
    Input:
        args # command line arguments
    Constant:
        None
    Variables
        parser
    Return
        parser.parse_args() # Parsed arguments
    '''

    parser = argparse.ArgumentParser(prog = 'parse_fastqc_all.py', formatter_class=argparse.RawDescriptionHelpFormatter, description= 'parse_fastqc_all.py creates a csv file from fastqc_data.txt files.')


    parser.add_argument('--path' ,'-p',required=True, help='Insert path where there are all the fastqc_data.txt as an example:/home/user/Service_folder/ANALYSIS/')

    parser.add_argument('--step' ,'-s',nargs='+',required=True, help='Insert list from fastqc_data.txt check the line of filename and insert the end of the string which has the information of the step and the forward and reverse reads as an example:_R1.fastq.gz _R2.fastq.gz _R1_filtered.fastq.gz _R2_filtered.fastq.gz')

    parser.add_argument('--tag' ,'-t',nargs='+',required=True, help='Insert list of nomenclature to define the step and the reads that has to combine with the arguments.step as an example: pre_R1 pre_R2 post_R1 post_R2')

    parser.add_argument('--output_bn','-b', required=True, help='The output in binary file')

    parser.add_argument('--output_csv','-c', required=True, help='The output in csv file')


    return parser.parse_args()



#################
### FUNCTIONS ###
#################


def find_files_in_folder(path, path_list, extension, subFolders = True):

    '''

    Recursive function to find all files of an extension type in a folder (and optionally in all subfolders too)

    path:        Base directory to find files
    pathList:    A list that stores all paths
    extension:   File extension to find
    subFolders:  Bool.  If True, find files in all subfolders under path. If False, only searches files in the specified folder

    '''

    try:   # Trapping a OSError:  File permissions problem I believe
        for entry in os.scandir(path):
            if entry.is_file() and entry.path.endswith(extension):
                path_list.append(entry.path)
            elif entry.is_dir() and subFolders:   # if its a directory, then repeat process as a nested function
                path_list = find_files_in_folder(entry.path, path_list, extension, subFolders)
    except OSError:
        print('Cannot access ' + path +'. Probably a permissions error')

    return path_list



#################
### FUNCTIONS ###
#################


def fastqc_all_dictionary (path_list, argument_step, argument_tag):

    '''
    Description:
        Function to create a dictionary from all fastqc_data.txt  files.

   Input:
        pathList with all the fastqc_data.txt from a folder
        argument_step: from fastqc_data.txt check the line of filename and add the end of the string which has the information of the step and the forward and reverse reads as an example:"_R1.fastq.gz", "_R2.fastq.gz","_R1_filtered.fastq.gz","_R2_filtered.fastq.gz"
        argument_tag : our nomenclature to define the step and the reads that has to combine with the argument_step (pre_R1","pre_R2", "post_R1","post_R2")

    Return:
        fastqc_all_dict (dictionary)

    '''

    fastqc_all_dict ={}
    for path in path_list:
        print (path)
        header = False
        sample = False
        with open (path, 'r') as fd:
            for line in fd:

                m = re.search ('Filename',line)

                if m:
                    line = line.replace('\n','')
                    value = line.split("\t")
                    filename = value [1]
                    for i in range (len(argument_step)):
                        start = '(.*(?='
                        end = '))'
                        search_data = start + argument_step [i] + end
                        if re.search (str(search_data), filename):
                            sample = re.search (str(search_data), filename).group(0)
                            print(sample)
                            step = argument_tag [i]
                            if not sample in fastqc_all_dict:
                                fastqc_all_dict [sample]={}
                                break

        if not sample:
            continue
        else:
            with open (path, 'r') as fd:
                for line in fd:
                    n = re.search ('END_MODULE',line)
                    if n:
                        break
                    n = re.search('FastQC', line)
                    if header:
                        line = line.replace('\n','')
                        line = line.split('\t')
                        fastqc_all_dict [sample][step +'_'+ line[0]] = line[1]

                    if n:
                        header = True
    print(fastqc_all_dict)
    return (fastqc_all_dict)


#################
### FUNCTIONS ###
#################


def dictionary2csv (dictionary, csv_file):

    '''

    Description:
        Function to create a csv from a dictionary
    Input:
        dictionary
    Return:
        csv file

   '''


    header = sorted(set(i for b in map(dict.keys, dictionary.values()) for i in b))
    with open(csv_file, 'w', newline="") as f:
        write = csv.writer(f)
        write.writerow(['sample', *header])
        for a, b in dictionary.items():
            write.writerow([a]+[b.get(i, '') for i in header])

#################
### FUNCTIONS ###
#################


def dictionary2bn (dictionary, binary_file):

    '''

    Description:
        Function to create a binary file from a dictionary
    Input:
        dictionary
    Return:
        binary file
    '''


    pickle_out = open(binary_file,"wb")
    pickle.dump(dictionary, pickle_out)
    pickle_out.close()

    return

###################
### MAIN SCRIPT ###
###################



if __name__ == '__main__' :


    # Variables
    version = 'fastqc_all v 0.1.0.'  # Script version
    arguments = check_arg(sys.argv[1:])


    #Create pathList
    path_list = []
    extension = "fastqc_data.txt"

    path_list_fastqc = find_files_in_folder(arguments.path, path_list, extension, True)
    print ('path_list_fastqc done')
    #print(path_list_fastqc)


    # Create a dictionary
    fastqc_all_dict = fastqc_all_dictionary (path_list_fastqc, arguments.step, arguments.tag)

    print ('fastqc_all_dictionary done')
    #print (fastqc_all_dict)


    #Convert the dictionary to csv file

    dictionary2csv (fastqc_all_dict, arguments.output_csv)

    print ('fastqc_all_dictionary_csv done')



    # Save the dicctionary to binary file

    dictionary2bn (fastqc_all_dict, arguments.output_bn)

    print ('fastqc_all_dictionary_bn done')




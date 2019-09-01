import re
import argparse
import sys
import os
import csv


######################
##Function_Arguments##
######################
 

def check_arg(args=None):

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
    parser = argparse.ArgumentParser(prog = 'parse_bedtools_stats.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Dictionary of bedtools_stats from file: exons_not_covered_stats.csv')

    
    parser.add_argument('-v, --version', action='version', version='v0.2')
    parser.add_argument('--input', required= True, nargs='+' ,
                                    help = 'exons_not_covered_stats.csv file including path where is stored.')
    parser.add_argument('--out',  required= True,
                                    help = 'csv file name incluiding path where the csv file will be stored.')


    return parser.parse_args()
    
########################
##Function_Dictionary ##
########################

def bedtools_dictionary (files_input):

    '''
    Description:
     'Dictionary of bedtools_stats from file: exons_not_covered_stats.csv'
    
    Input:
     'exons_not_covered_stats.csv files including path where is stored.' 
    
    Return:
      d (dictionary)
           
    ''' 
    d={}
    header=False
    for file in files_input:
        with open(file) as bedstats_file:

            for line in bedstats_file:
                line=line.strip('\n')
                if len(line) == 0 :
                    continue
                if 'exons' in line :
                    header = True
                    print('found_header:' , header)
                    continue

                if header :
                    line = line.split('\t')
                    sample = line[0].split('.')
                    sample = sample[0]
                    sample = re.sub(r"\"", "", sample)
                    #print( 'sample', sample)
                    d[sample] = {}
                    step= 'bedtools_'
                    d[sample][step + 'exons_below_20']= float(line[1])
                    d[sample][step + 'fr_covered']= float(line[2])
                    d[sample][step + 'fr_NOT_covered']= float(line[3])
    return(d)


######################
##Function_Dic2CSV  ##
######################   

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





##########
## MAIN ##
########## 
   
if __name__ == '__main__' :

    
    #Arguments: 
    
    '''
    Example arguments:
    
    --input /home/masterbioinfo/EXOME/Data/bedtools/*.csv
    --out /home/masterbioinfo/EXOME/Results/dic_bedtools_all.csv
    '''
    
    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)
    
    #Dictionary of hsMetrics.out data:
    
    dic_bedtools_all = bedtools_dictionary(arguments.input)
    
    print ('bedtools_dictionary done')
    #print (dic_bedtools_all)
    
    
    #Export dictionary as csv file:
    
    dictionary2csv (dic_bedtools_all, arguments.out)

    print ('bedtools_csv done')
    
    
    '''
    #Visualize CSV file using pandas:
     
    import pandas
    panda_file = pandas.read_csv(arguments.out)
    print(panda_file)
    
    '''
    
 

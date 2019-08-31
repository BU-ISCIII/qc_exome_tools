

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

    parser = argparse.ArgumentParser(prog = 'parse_familypedigree_ped.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Dictionary of familypedigree_data from .ped file')

    
    parser.add_argument('-v, --version', action='version', version='v0.2')
    parser.add_argument('--input', required= True, nargs='+' ,
                                    help = 'familypedigree.ped files including path where are stored.')
    parser.add_argument('--out',  required= True,
                                    help = 'csv file name incluiding path where the csv file will be stored.')


    return parser.parse_args()
    


########################
##Function_Dictionary ##
########################

def familypedigree_dictionary (ped_input):
    
    '''
    Description:
     Function to create a Dictionary with the familypedigree data from a ped file
    
    Input:
     familypedigree.ped files including path where are stored   
    
    Return:
      d (dictionary)
           
    '''
    
    
    d={}
    for file in ped_input:
        with open(file) as pedfile:

            for line in pedfile:
                line=line.strip('\n')
                line = re.sub(r"\s+", "\t", line)
                line=line.split('\t')
                sample=line[1]
                d[sample]={}
                d[sample]['ped_familyID']=line[0]
                d[sample]['ped_paternalID']=line[2]
                d[sample]['ped_maternalID']=line[3]
                d[sample]['ped_gender']=line[4]
                d[sample]['ped_phenotype']=line[5]
                
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
    --input /home/masterbioinfo/EXOME/Data/ped_files/*familypedigri.ped
    --out  /home/masterbioinfo/EXOME/Results/dic_pedigree_all.csv
    '''
    
    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)


    #Dictionary of familypedigree data:
    
    dic_pedigree_all = familypedigree_dictionary(arguments.input)
    
    print ('familypedigree_dictionary done')
    #print (dic_pedigree_all)
    
    
    #Export dictionary as csv file:
    
    dictionary2csv (dic_pedigree_all, arguments.out)

    print ('familypedigree_csv done')
    
    
    #Visualize CSV file using pandas:
     
    import pandas
    panda_file = pandas.read_csv(arguments.out)
    print(panda_file)

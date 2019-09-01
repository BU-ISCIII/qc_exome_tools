import re
import argparse
import sys
import os
import re
import csv
import glob


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
    parser = argparse.ArgumentParser(prog = 'parse_bamstats.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description= 'Dictionary of bamstats from file: SAMPLE_bamstats.txt')


    parser.add_argument('-v, --version', action='version', version='v0.2')
    parser.add_argument('--input', required= True, nargs='+' ,
                                    help = 'Bamstat.txt files including path where are stored.')
    parser.add_argument('--out',  required= True,
                                    help = 'csv file name incluiding path where the csv file will be stored.')

    return parser.parse_args()


########################
##Function_Dictionary ##
########################

def bamstats_dictionary (bamstat_txt):

    '''
    Description:
     'Dictionary of bamstats from file: SAMPLE_bamstats.txt'
    
    Input:
     'Bamstat.txt files including path where are stored.' 
    
    Return:
      d (dictionary)
           
    ''' 
    d={}
    for file in bamstat_txt:
        sample = (os.path.basename(file)).split('_')
        sample = sample[0]
        #print('sample:', sample)
        found_start=False
        d[sample]={}
        #print('Dictionary samples', d)

        with open(file) as bamstats_file:

            for line in bamstats_file:
                line=line.strip('\n')
                if len(line) == 0 :
                    continue
                if 'Number of records' in line :
                    found_start = True
                    print('found_start:' , found_start)
                    continue
                if found_start :
                    line = line.split('\t')
                    if not re.search('(.*\(e6\)|.*\(%\))$',line[0]):
                        key=line[0]+'(e6)'
                        value=float(line[1])/1000000
                    else:
                        key=line[0]
                        value=float(line[1])
                    d[sample]['bamstats_'+ key]= value
    
    #print('Dictionary_Bamstats done.')
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
    
    --input /home/masterbioinfo/EXOME/Data/bamstats/*.txt
    --out /home/masterbioinfo/EXOME/Results/dic_bamstats_all.csv
    '''
    
    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)


    #Dictionary of bamstats:
    
    dic_bamstats_all = bamstats_dictionary(arguments.input)
    
    print ('bamstats_dictionary done')
    #print (dic_bamstats_all)
    
    
    #Export dictionary as csv file:
    
    dictionary2csv (dic_bamstats_all, arguments.out)

    print ('bamstats_csv done')
    
    '''
    #Visualize CSV file using pandas:
     
    import pandas
    panda_file = pandas.read_csv(arguments.out)
    print(panda_file)
    
    '''
    
    


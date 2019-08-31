import re
import argparse
import sys
import glob
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

    parser = argparse.ArgumentParser(prog = 'parse_hsmetrics_v0.2.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Dictionary of hsmetrics_data from hsmetrics.out file')

    
    parser.add_argument('-v, --version', action='version', version='v0.2')
    parser.add_argument('--input', required= True, nargs="+",
                                    help = 'hsMetrics.out files incluiding path where files are stored.')
    parser.add_argument('--out',  required= True,
                                    help = 'csv file name incluiding path where the csv file will be stored.')


    return parser.parse_args()


########################
##Function_Dictionary ##
########################

def hsmetrics_dictionary (files_out_input):
    '''
    Description:
     'Dictionary of hsmetrics_data from hsmetrics.out file'
    
    Input:
     hsMetrics.out file including path where is stored.' 
    
    Return:
      d (dictionary)
           
    '''
    
    d={}
    for file in files_out_input :
        sample = (os.path.basename(file)).split('_')
        sample = sample[0]
        found_start=False
        found_value=False
        d[sample]={}
      
        with open(file) as hsmetrics_file:

            for line in hsmetrics_file:
                line=line.strip('\n')
                if len(line) == 0 :
                    continue
                if 'METRICS CLASS' in line :
                    found_start = True
                    #print('found start:' , found_start)
                    continue
                if found_start :
                    keys = line.split('\t')
                    found_value=True
                    found_start=False
                    continue
                if found_value:
                    values=line.split('\t')
                    break
            hs_keys = ["hsMetrics_" + key for key in keys ]
            #print('hskeys', hs_keys)
           
            for i in range(len(hs_keys)):
                d[sample][hs_keys[i]]= values[i]
                
                #convert string to numbers:
                for val in d[sample][hs_keys[i]] :
                    try:
                        d[sample][hs_keys[i]]= float(values[i])
                    except (ValueError, TypeError):
                        d[sample][hs_keys[i]]= values[i]

        
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
    --input /home/masterbioinfo/EXOME/Data/hsmetrics/*.out
    --out /home/masterbioinfo/EXOME/Results/dic_hsMetrics_all.csv
    '''
    
    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)



    #Dictionary of hsMetrics.out data:
    
    dic_hsmetrics_all = hsmetrics_dictionary(arguments.input)
    
    print ('hsmetrics_dictionary done')
    #print (dic_hsmetrics_all)
    
    
    #Export dictionary as csv file:
    
    dictionary2csv (dic_hsmetrics_all, arguments.out)

    print ('hsmetrics_csv done')
    
    
    #Visualize CSV file using pandas:
     
    import pandas
    panda_file = pandas.read_csv(arguments.out)
    print(panda_file)
    


















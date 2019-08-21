import re
import argparse
import sys
import os
import csv

# Definition of required arguments (input_file path , output path) with argparse module: 

def check_arg(args=None):
    parser = argparse.ArgumentParser(prog = 'script_dic_bedtools_stats.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Dictionary of bedtools_stats from file: exons_not_covered_stats.csv')

    
    parser.add_argument('-v, --version', action='version', version='v0.2')
    parser.add_argument('--input', required= True, nargs='+' ,
                                    help = 'exons_not_covered_stats.csv file including path where is stored.')
    parser.add_argument('--out',  required= True,
                                    help = 'csv file name incluiding path where the csv file will be stored.')


    return parser.parse_args()
if __name__ == '__main__' :

    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)

   #Dictionary of Bedtools file (exons_not_covered_stats.csv) data:
    d={}
    heather=False
    for file in arguments.input:
        with open(file) as bedstats_file:

            for line in bedstats_file:
                line=line.strip('\n')
                if len(line) == 0 :
                    continue
                if 'exons' in line :
                    heather = True
                    print('encuentre sample:' , heather)
                    continue

                if heather :
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
        print(d)
        

        #Export dictionary as csv file:

        outfile = arguments.out
        dic = d #Nested dictionary 
        headers = list(list (dic.values())[1].keys()) #Encabezado de las columnas
        #print (len (headers))
        #print (dic.values()) 
            
        with open(outfile, "w") as f:
            w = csv.writer( f )
            
            w.writerow(['sample'] + headers)# printea la primera fila
            
            parameters = list(list (dic.values())[0].keys())
            #print (parameters)
            for sample in dic.keys():
                #print (dic.keys())
                w.writerow([sample] + [dic[sample][parameter] for parameter in parameters])
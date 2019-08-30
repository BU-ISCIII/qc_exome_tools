import re
import argparse
import sys
import os
import csv

# Definition of required arguments (input_file path , output path) with argparse module: 

def check_arg(args=None):
    parser = argparse.ArgumentParser(prog = 'script_dic_familypedigree.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Dictionary of familypedigree_data from .ped file')

    
    parser.add_argument('-v, --version', action='version', version='v0.2')
    parser.add_argument('--input', required= True, nargs='+' ,
                                    help = 'familypedigree.ped files including path where are stored.')
    parser.add_argument('--out',  required= True,
                                    help = 'csv file name incluiding path where the csv file will be stored.')


    return parser.parse_args()

if __name__ == '__main__' :

    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)


    #Dictionary of familypedigree data:
    d={}
    for file in arguments.input:
        with open(file) as pedfile:

            #print('tipo', type(pedfile))
            for line in pedfile:
                line=line.strip('\n')
                #print(line)
                #print(type(line))
                line = re.sub(r"\s+", "\t", line)
                line=line.split('\t')
                #print(line)    
                #print(type(line))
                sample=line[1]
                #print('sample', sample)
                d[sample]={}
                d[sample]['ped_familyID']=line[0]
                d[sample]['ped_paternalID']=line[2]
                d[sample]['ped_maternalID_ped']=line[3]
                d[sample]['ped_gender']=line[4]
                d[sample]['ped_phenotype']=line[5]
                
                
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
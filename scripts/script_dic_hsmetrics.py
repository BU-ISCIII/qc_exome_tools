import re
import argparse
import sys
import os
import csv

def check_arg(args=None):
    parser = argparse.ArgumentParser(prog = 'script_dic_hsmetrics.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Dictionary of hsmetrics_data from hsmetrics.out file')

    
    parser.add_argument('-v, --version', action='version', version='v0.1')
    parser.add_argument('--input', required= True,
                                    help = 'hsMetrics.out file including path where is stored.')
    parser.add_argument('--out',  required= True,
                                    help = 'Directory where the result files will be stored.')


    return parser.parse_args()
if __name__ == '__main__' :

    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)   

    d={}
    #hsmetrics_path ="/home/masterbioinfo/EXOME/Data/ND0801_hsMetrics.out"
    sample = (os.path.basename(arguments.input)).split('_')
    sample = sample[0]
    print('sample:', sample)
    found_start=False
    found_value=False
    d[sample]={}

    with open(arguments.input) as hsmetrics_file:
        print('type_file', type(hsmetrics_file))

        for line in hsmetrics_file:
            line=line.strip('\n')
            if len(line) == 0 :
                continue
            if 'METRICS CLASS' in line :
                found_start = True
                print('encuentre start:' , found_start)
                continue
            if found_start :
                keys = line.split('\t')
                #print(keys)
                found_value=True
                found_start=False
                continue
            if found_value:
                values=line.split('\t')
                
                break
        for i in range(len(keys)):
            d[sample][keys[i]]= values[i]
            
            #convert string to numbers
            for val in d[sample][keys[i]] :
                try:
                    d[sample][keys[i]]= float(values[i])
                except (ValueError, TypeError):
                    d[sample][keys[i]]= values[i]

    print(len(keys), '-', len(values))
                
    print('Dictionary_hsmetrics:' , d)

    #Export dictionary as csv file:

    outfile = os.path.join(arguments.out, 'dic_hsmetrics.csv')
    dic = d #Nested dictionary

    headers = list(list (dic.values())[0].keys()) #Encabezado de las columnas
    #print (len (headers))
    #print (headers)
      
    with open(outfile, "w") as f:
        w = csv.writer( f )
        
        w.writerow(['sample'] + headers)# printea la primera fila
        
        parameters = list(list (dic.values())[0].keys())
        #print (parameters)
        for sample in dic.keys():
            #print (dic.keys())
            w.writerow([sample] + [dic[sample][parameter] for parameter in parameters])



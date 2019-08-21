import re
import argparse
import sys
import os
import csv
import glob

# Definition of required arguments (input_file path , output path) with argparse module: 
def check_arg(args=None):
    parser = argparse.ArgumentParser(prog = 'script_dic_bamstats_v0.2.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Dictionary of bamstats from file: SAMPLE_bamstats.txt')

    
    parser.add_argument('-v, --version', action='version', version='v0.2')
    parser.add_argument('--input', required= True, nargs='+' , 
                                    help = 'Directory where SAMPLE_bamstats.txt files are stored.')
    parser.add_argument('--out',  required= True,
                                    help = 'csv file name incluiding path where the csv file will be stored.')

    return parser.parse_args()

if __name__ == '__main__' :

    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)
    #files_out = [os.path.realpath(path) for path in glob.glob(arguments.input + '/*bamstat.txt')]
    #print('files' , files_out)

    #Dictionary of bamstat.txt data:
    d={}
    for file in arguments.input:
        #bamstats_path ="/home/masterbioinfo/EXOME/Data/ND0801_bamstat.txt"
        sample = (os.path.basename(file)).split('_')
        sample = sample[0]
        #print('sample:', sample)
        found_start=False
        d[sample]={}
        print('Dictionary samples', d)


        with open(file) as bamstats_file:
            #print('type_file', type(bamstats_file))

            for line in bamstats_file:
                line=line.strip('\n')
                if len(line) == 0 :
                    continue
                if 'Number of records' in line :
                    found_start = True
                    print('encuentre start:' , found_start)
                    continue
                if found_start :
                    line = line.split('\t')
                    key=line[0]
                    value=float(line[1])
                    d[sample]['bamstats_'+ key]= value
        
        print('Dictionary_Bamstats:' , d)
        
        #Export dictionary as csv file:

        outfile = arguments.out
        dic = d #Nested dictionary 
        headers = list(list (dic.values())[0].keys()) #Encabezado de las columnas
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


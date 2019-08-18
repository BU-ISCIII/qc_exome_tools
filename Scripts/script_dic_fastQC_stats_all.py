import json
import csv
import os
import re
import pandas as pd
import glob
import argparse
import sys


def check_arg(args=None):
    parser = argparse.ArgumentParser(prog = 'script_dic_fastQC_stats_all_v0.1.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Dictionary of fastQC_stats from file: fastqc_data.txt')

    
    parser.add_argument('-v, --version', action='version', version='v0.1')
    parser.add_argument('--input', required= True,
                                    help = 'Directory where the results of fastqc analysis will be stored.')
    #
    parser.add_argument('--out',  required= True,
                                    help = 'Directory where the result files will be stored.')


    return parser.parse_args()

if __name__ == '__main__' :

    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)


    #path = "/home/masterbioinfo/EXOME/Data/fastqc/"
    path = arguments.input
    sample_list = []#listado de los nombres de las muestras
    sample_list = os.listdir (path)#listaria ficheros y directorios 
    print(sample_list)

    # Function to create a dictionary from fastqc_data.txt file:
    def fastqc_dict (file):
        qc_dict = {}
        header = False
        with open (file, 'r') as fd:
            for line in fd:
                m = re.search ('END_MODULE',line)
                if m:
                    break
                m = re.search('FastQC', line)
                if header:
                    line = line.replace('\n','') 
                    line = line.split('\t')
                    for step in steps:
                        qc_dict[step +"_"+ line[0]] = line[1]
                if m:
                    header = True
        return qc_dict

    #fastqc_dict('/home/masterbioinfo/EXOME/Data/fastqc/ND0801/ND0801_R1_fastqc/fastqc_data.txt')

    #Dictionary of fastqc data pre_trimming:
    dic_fastqc_pre = {}
    steps = ['R1_fastqc' , 'R2_fastqc']
    for step in steps:
        for sample in sample_list:
            file_name = os.path.join (path,sample,sample+"_"+step,"fastqc_data.txt")#Crear una variable de path, recordar separar por comas
            dic_fastqc_pre[sample] = fastqc_dict (file_name)
    print ('Dic_fastqc_pre', dic_fastqc_pre)#nested dict

    #Dictionary of fastqc data post_trimming:
    dic_fastqc_trimmed = {}
    steps = ['trimmed_R1_fastqc' , 'trimmed_R2_fastqc']
    for step in steps:

        for sample in sample_list:
            file_name = os.path.join (path,sample,sample+"."+step,"fastqc_data.txt")#Crear una variable de path, recordar separar por comas
            dic_fastqc_trimmed[sample] = fastqc_dict (file_name)
    print ('Dic_fastqc_trimmed',dic_fastqc_trimmed)#nested dict

    #Dictionary of fastqc data pre and post trimming:

    dic_fastQC_all= {}
    for key in dic_fastqc_pre:
        if key in dic_fastqc_trimmed:
            dic_fastqc_pre[key].update(dic_fastqc_trimmed[key])
            dic_fastQC_all = dic_fastqc_pre
    print('juntos' , dic_fastQC_all)



    #Export dictionary as csv file:

    outfile = os.path.join(arguments.out, 'dic_fastqc_stats_all.csv')
    dic = dic_fastQC_all #Nested dictionary 
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

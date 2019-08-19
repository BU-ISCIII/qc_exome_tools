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

# Function to create a dictionary from fastqc_data.txt file:
def fastqc_dict (file,step):
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
                qc_dict[step +"_"+ line[0]] = line[1]
            if m:
                header = True
    return qc_dict

if __name__ == '__main__' :

    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)


    #path = "/home/masterbioinfo/EXOME/Data/fastqc/"
    path = arguments.input
    sample_list = []#listado de los nombres de las muestras
    sample_list = os.listdir (path)#listaria ficheros y directorios 
    print(sample_list)

   
    #fastqc_dict('/home/masterbioinfo/EXOME/Data/fastqc/ND0801/ND0801_R1_fastqc/fastqc_data.txt')

    #Dictionary of fastqc data pre_trimming:
    dic_fastqc_pre = {}
    dic_tmp = {}
    steps = ['R1_fastqc' , 'R2_fastqc']
    for sample in sample_list:
        dic_fastqc_pre[sample] = {}
        for step in steps:
            file_name = os.path.join (path,sample,sample+"_"+step,"fastqc_data.txt")#Crear una variable de path, recordar separar por comas
            if os.path.exists(file_name)== False:
                print(file_name, 'false')
                break
            if os.path.exists(file_name)== True:
                print('path exists' , os.path.exists(file_name))
                dic_tmp = fastqc_dict (file_name,step)
                if not dic_fastqc_pre[sample]:
                    dic_fastqc_pre[sample] = dic_tmp
                else:
                    #dic_fastqc_pre[sample] = {**dic_fastqc_pre[sample],**dic_tmp} 
                    dic_fastqc_pre[sample].update(dic_tmp)
                

            
    print ('Dic_fastqc_pre', dic_fastqc_pre)#nested dict

    #Dictionary of fastqc data post_trimming:
    dic_fastqc_trimmed = {}
    dic_tmp_trim = {}
    steps = ['trimmed_R1_fastqc' , 'trimmed_R2_fastqc']
    for sample in sample_list:
        dic_fastqc_trimmed[sample] = {}
        for step in steps:
            file_name = os.path.join (path,sample,sample+"."+step,"fastqc_data.txt")#Crear una variable de path, recordar separar por comas
            if os.path.exists(file_name)== False:
                print(file_name, 'false')
                break
            if os.path.exists(file_name)== True:
                print('path exists' , file_name)
                dic_tmp_trim = fastqc_dict (file_name,step)
                if not dic_fastqc_trimmed[sample]:
                    dic_fastqc_trimmed[sample] = dic_tmp_trim
                else:
                    #dic_fastqc_trimmed[sample] = {**dic_fastqc_trimmed[sample],**dic_tmp_trim} 
                    dic_fastqc_trimmed[sample].update(dic_tmp_trim)
            #dic_fastqc_trimmed[sample] = fastqc_dict (file_name)
    print ('Dic_fastqc_trimmed',dic_fastqc_trimmed)#nested dict


    #Dictionary of fastqc data pre and post trimming:

    dic_fastQC_all= {}
    for key in dic_fastqc_pre:
        if key in dic_fastqc_trimmed:
            dic_fastqc_pre[key].update(dic_fastqc_trimmed[key])
            dic_fastQC_all = dic_fastqc_pre
    print('Dic_fastQC_all:' , dic_fastQC_all)
    
    #Export dictionary as csv file:
    
    dic = dic_fastQC_all
    outfile = os.path.join(arguments.out, 'dic_fastqc_stats_all.csv')
    header = sorted(set(i for b in map(dict.keys, dic.values()) for i in b))
    with open(outfile, 'w', newline="") as f:
        write = csv.writer(f)
        write.writerow(['sample', *header])
        for a, b in dic.items():
            write.writerow([a]+[b.get(i, '') for i in header])





import json
import csv
import os
import re
import pandas as pd
import glob

path = "/home/masterbioinfo/EXOME/Data/fastqc/"
sample_list = []#listado de los nombres de las muestras
sample_list = os.listdir (path)#listaria ficheros y directorios 
print(sample_list)


def fastqc_dict (file):
    step = 'preFastQC_'
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
                qc_dict[step + line[0]] = line[1]
            if m:
                header = True
    return qc_dict

#fastqc_dict('/home/masterbioinfo/EXOME/Data/fastqc/ND0801/ND0801_R1_fastqc/fastqc_data.txt')


fastq_all = {}

for sample in sample_list:
    file_name = os.path.join (path,sample,sample+"_R1_fastqc","fastqc_data.txt")#Crear una variable de path, recordar separar por comas
    fastq_all[sample] = fastqc_dict (file_name)
print (fastq_all)#nested dict

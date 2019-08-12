import json
import csv
import os
import re
import pandas as pd
import glob

path = "D:/Users/smonzon/Desktop/Documentos_Sara/Pipeline/03-preprocQC/"
#sample_list = []#listado de los nombres de las muestras
#tmp = os.listdir (path)#listaria ficheros y directorios 
#print
def fastqc_dict (file):
    step = '03-preprocQC_'
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
'''              
fastq_all = {}

for sample in sample_list:
    file_name = os.path.join (path,sample,sample+"_R1_filtered_fastqc","fastqc_data.txt")#Crear una variable de path, recordar separar por comas
    fastq_all[sample] = fastqc_dict (file_name)


print (fastq_all)#nested dict
'''

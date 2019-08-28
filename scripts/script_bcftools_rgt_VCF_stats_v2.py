import re
import argparse
import sys
import os
import csv

def check_arg(args=None):
    parser = argparse.ArgumentParser(prog = 'script_dic_rgt_VCF_stats.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Dictionary of rgt_VCF_stats from file: all_samples_gtpos_fil_annot.vcf')

    
    parser.add_argument('-v, --version', action='version', version='v0.1')
    parser.add_argument('--input', required= True,
                                    help = '(command)rtg vcfstats and (arguments) all_samples_gtpos_fil_annot.vcf file including path where is stored.')
    #
    parser.add_argument('--out',  required= True,
                                    help = 'Directory where the result files will be stored.')


    return parser.parse_args()

if __name__ == '__main__' :

    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)


    #Run bash script for rtg vcfstats:
    import subprocess


    #stats = subprocess.getoutput(str ('/home/masterbioinfo/Programas/rtg-tools-3.10.1/rtg vcfstats /home/masterbioinfo/EXOME/Data/VCF/ND0800/all_samples_gtpos_fil_annot.vcf') )
    
    stats = subprocess.getoutput(str (arguments.input) )
    
    #print(stats)

    
    #Dictionary of rtg vcfstats results for each sample: 

    d={}
    found_samplename=False
    stats = stats.split('\n')
    print(stats)

    for line in stats:
        
        if len(line) == 0 :
            continue
        if 'Sample' in line :
            found_samplename = True
            print('encuentre sample:' , found_samplename)
            line = line.split(':')
            sample = line[1].strip()
            print(sample)
            d[sample] = {}
            continue
        if found_samplename :
            line = line.split(':')
            key=line[0].rstrip()
            #print(line)
            value=line[1].lstrip()
            data = value.split(' ')[0]
            data= data.replace('%', '')
            if '-'  in data:
                data = '0'
            d[sample][key]=  float(data) 
            
    print('Dictionary_VCFstats :' , d)

    #Export dictionary as csv file:

    outfile = os.path.join(arguments.out, 'dic_rtg_vcf_stats.csv')
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














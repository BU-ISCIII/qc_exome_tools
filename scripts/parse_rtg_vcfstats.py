import re
import argparse
import sys
import os
import csv
import subprocess

def check_arg(args=None):
    parser = argparse.ArgumentParser(prog = 'script_dic_rgt_VCF_stats.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Dictionary of rgt_VCF_stats from file: all_samples_gtpos_fil_annot.vcf')

    
    parser.add_argument('-v, --version', action='version', version='v0.2')
    parser.add_argument('--input', required= True, nargs='+',
                                    help = 'all_samples_gtpos_fil_annot.vcf files including path where is stored.')
    
    parser.add_argument('--out',  required= True,
                                    help = 'csv file name incluiding path where the csv file will be stored.')


    return parser.parse_args()

if __name__ == '__main__' :

    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)


    d={}
    for file in arguments.input:

        #Run bash script for rtg vcfstats:

        found_samplename=False
        cmd = ["rtg" , "vcfstats"]
        #parametro = [' /home/masterbioinfo/EXOME/Data/VCF/ND0800/all_samples_gtpos_fil_annot.vcf']
        parametro = [file]
        cmd.extend(parametro)
        cmd2 = ' '.join(cmd)
        print(cmd2)
        stats = subprocess.getoutput(str(cmd2))
        
        #Dictionary of rtg vcfstats results for each sample:

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
                d[sample]['rtg_vcfstats_' + key]=  float(data) 
                
    print('Dictionary_VCFstats :' , d)
    
    #Export dictionary as csv file:

    dic = d
    outfile = arguments.out
    header = sorted(set(i for b in map(dict.keys, dic.values()) for i in b))
    with open(outfile, 'w', newline="") as f:
        write = csv.writer(f)
        write.writerow(['sample', *header])
        for a, b in dic.items():
            write.writerow([a]+[b.get(i, '') for i in header])

    #Visualize CSV file using pandas:
     
    import pandas
    gender_pandas = pandas.read_csv(outfile)
    print(gender_pandas)











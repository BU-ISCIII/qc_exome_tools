
import subprocess
import re
import argparse
import sys
import os
import csv


def check_arg(args=None):
    parser = argparse.ArgumentParser(prog = 'script_bcftools_rgt_VCF_Homo_v5.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Determine gender using SNP Het/Homo ratio of Chrx from RGT VCF stats')
    
    parser.add_argument('-v, --version', action='version', version='v0.5')
    parser.add_argument('--input', required= True,
                                    help = 'bash script (script_bcftools_rgt_VCF_Homo_v1_wooutput.sh) including path where is stored.')
    parser.add_argument('--out',  required= True,
                                    help = 'Directory where the result files will be stored.')


    return parser.parse_args()

if __name__ == '__main__' :

    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)

    #Run bash script for rtg vcfstats of ChrX.vcf:


    #rgt_stats_chrx = subprocess.getoutput(str('/home/masterbioinfo/EXOME/Scripts/script_bcftools_rgt_VCF_Homo_v1_wooutput.sh'))
    rgt_stats_chrx = subprocess.getoutput(str(arguments.input))

    #Dictionary of VCF stats of ChrX 

    d={}
    found_samplename=False
    rgt_stats_chrx=rgt_stats_chrx.split('\n')

    for line in rgt_stats_chrx:
        if '[' in line:
            continue
        if len(line) == 0 :
            continue
        if 'Sample' in line :
            found_samplename = True
            print('encuentre sample:' , found_samplename)
            line = line.split(':')
            name = line[1].strip()
            print(name)
            d[name] = {}
            continue
        if found_samplename :
            line = line.split(':')
            key=line[0].rstrip()
            #print(line)
            value=line[1].lstrip()
            d[name][key]= value
    print('Dictionary_VCFstats_ChrX :' , d)


    #Determine gender using SNP Het/Homo ratio of Chrx VCF stats:

    Het_Homo_ratio_str = None
    Het_Homo_ratio_number = 0
    gender = None

    #outfile = '/home/masterbioinfo/EXOME/Results/gender_rtg_homo/gender_results_homo.csv'

    outfile = os.path.join(arguments.out, 'gender_results_homo.csv')
    
    with open( outfile , mode='w') as gender_file:
        gender_results_homo = csv.writer(gender_file, delimiter=',')
        gender_results_homo.writerow(['sample', 'SNP Het/Hom ratio', 'Gender' ])
        for sample , stats in d.items():
            print("\nSample:", sample)
            
            for item in stats:
                if 'SNP Het/Hom ratio' in item :
                    print(item + ':', stats[item])
                    ratio_str = stats[item]
                    ratio_str = ratio_str.split(' ')
                    ratio_number = float(ratio_str[0])
                    print(ratio_number)
                    if ratio_number < 1.2 :
                        gender = 'Male'
                        print(sample, gender)
                        gender_results_homo.writerow([ sample , ratio_number, gender])
                    else:
                        gender = 'Female'
                        print(sample, gender)
                        gender_results_homo.writerow([ sample , ratio_number, gender])

    #Dictionary of gender_homo results for each sample:
    
    with open(outfile) as gender_homo:
        dr = csv.DictReader(gender_homo, delimiter=',')
        dic_gender_homo = {}
        for row in dr:

            dic_gender_homo[row['sample']]={}
            for key, value in row.items():
                if not key == 'sample':
                        
                    print(key)
                    dic_gender_homo[row['sample']][key] = value

    print(dic_gender_homo)















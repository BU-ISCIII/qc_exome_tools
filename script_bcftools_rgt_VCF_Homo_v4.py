
#Run bash script for rtg vcfstats of ChrX.vcf:
import subprocess

subprocess.run( ['/home/masterbioinfo/EXOME/Scripts/script_bcftools_rgt_VCF_Homo_v1.sh'] , shell=True)

#Dictionary of VCF stats of ChrX 
from os import path

file_path ="/home/masterbioinfo/EXOME/Results/gender_rtg_homo/file_vcfstats_chrX.txt"
d={}
found_samplename=False

with open(file_path) as stats:
    print(stats)
    for line in stats:
        line=line.strip('\n')
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
import csv
#Determine gender using SNP Het/Homo ratio of Chrx VCF stats:
Het_Homo_ratio_str = None
Het_Homo_ratio_number = 0
gender = None
outfile = '/home/masterbioinfo/EXOME/Results/gender_rtg_homo/gender_results_homo.csv'
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
    

 
 














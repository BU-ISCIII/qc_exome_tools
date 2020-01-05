import re
import argparse
import sys
import os
import csv
import subprocess

#Necessary: bcftools==1.9 , rtg-tools==3.10.1, samtools==1.9 and - htslib==1.9 
#Install Conda environment for QC_Exome Tools: qc_exome_tools.yml

def check_arg(args=None):
    parser = argparse.ArgumentParser(prog = 'sex_determination_using_rtg_vcfstats_x_homo.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Determine genetic sex from vcf file using rtg vcfstats to obtain ChrX homozygosity')

    
    parser.add_argument('-v, --version', action='version', version='v0.0')
    parser.add_argument('--input', required= True, nargs='+',
                                    help = 'vcf files including path where are stored.')
    
    parser.add_argument('--out',  required= True,
                                    help = 'csv file name incluiding path where the csv file will be stored.')

    return parser.parse_args()

if __name__ == '__main__' :

    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)
    
    d={}
    d_gender={}
    for file in arguments.input :

        ##Compress vcf to gz using subprocess.run:

        filegz = file + ".gz"
        cmd = ["bgzip" , "-c", file, ">", filegz] 
        subprocess.run(' '.join(cmd), shell=True)
        print(' '.join(cmd))

        #Create file .tbi using tabix:
        cmd2 = ["tabix" , "-p" , "vcf" , filegz]
        subprocess.run(' '.join(cmd2), shell=True)
        print(' '.join(cmd2))

        #Obtain CHR_X variants with bcftools:
        file_chrX_vcf = filegz + "_chrX.vcf"
        cmd3= ["bcftools" , "view" ,"-r" , "X", filegz , ">", file_chrX_vcf]
        subprocess.run(' '.join(cmd3), shell=True)
        print(' '.join(cmd3))

        # Obtain vcfstats of ChrX with rtg-tools:

        cmd4 = ["rtg" , "vcfstats", file_chrX_vcf]
        rgt_stats_chrx = subprocess.getoutput(str(' '.join(cmd4)))
        print(' '.join(cmd4))
        #print(rgt_stats_chrx)
        
        #Obtain sample name from vcf files* 
        #(*necessary when vcfstats are obtained from vcf files with only one sample):

        parameter = [file]
        cmd_name = ["bcftools" , "query" , "-l"]
        cmd_name.extend(parameter)
        cmd_name2 = ' '.join(cmd_name)
        print(cmd_name2)
        name = subprocess.getoutput(cmd_name2)
        print('sample names:', name)
        name = name.split('\n')

        #Dictionary of VCF stats of ChrX 

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
                sample = line[1].strip()
                print(sample)
                d[sample] = {}
                continue 
                
            elif 'Passed Filters' in line :
                sample = name[0]
                print('number of vcf samples:', len(name))
                if len(name) == 1 :
                    print(sample)
                    d[sample] = {}
                    found_samplename = True
                    print('found sample_unique:' , found_samplename)     
                    continue
            if found_samplename :
                line = line.split(':')
                key=line[0].rstrip()
                #print(line)
                value=line[1].lstrip()
                data = value.split(' ')[0]
                data= data.replace('%', '')
                if '-'  in data:
                    data = '-'
                    #data = value.split(' ')[1]
                d[sample][key]=  data

        print('Dictionary_VCFstats_ChrX :' , d)

        #Determine gender using SNP Het/Homo ratio of Chrx VCF stats:

        Het_Homo_ratio_str = None
        Het_Homo_ratio_number = 0
        gender = None
        for sample , stats in d.items():
                #print("\nSample:", sample)
                for item in stats:
                    if 'SNP Het/Hom ratio' in item :
                        print(item + ':', stats[item])
                        ratio_str = stats[item]
                        ratio_str = ratio_str.split(' ')
                        #ratio_number = float(ratio_str[0])
                        ratio_number = ratio_str[0]
                        if '-' in ratio_number:
                            gender = 'unknown'
                            print(sample, gender)
                        else:
                            ratio_number = float(ratio_str[0])
                            #if ratio_number < 1.2 :
                            if ratio_number < 0.77 :
                                gender = 'Male'
                                print(sample, gender)
                                #gender_results_homo.writerow([ sample , ratio_number, gender])
                            else:
                                gender = 'Female'
                                print(sample, gender)
                            #   gender_results_homo.writerow([ sample , ratio_number, gender])

                parameters = ['Gender_HomoChrX_SNP_Het/Hom_ratio', 'Gender_HomoChrX_Gender']
                values = [ratio_number, gender]
              
                #Dictionary of gender_homo results:

                d_gender[sample]= {}
                i=0
                for i in range (0 , len(values)):
                    d_gender[sample][parameters[i]]= values[i]
                    print(d_gender[sample][parameters[i]])
                    i=+1
    print(d_gender)

    #Export dictionary as csv file:
        
    dic = d_gender
    outfile = arguments.out
    header = sorted(set(i for b in map(dict.keys, dic.values()) for i in b))
    with open(outfile, 'w', newline="") as f:
        write = csv.writer(f)
        write.writerow(['sample', *header])
        for a, b in dic.items():
            write.writerow([a]+[b.get(i, '') for i in header])

'''
    #Visualize CSV file using pandas:

    import pandas
    gender_pandas = pandas.read_csv(outfile)
    print(gender_pandas)

'''












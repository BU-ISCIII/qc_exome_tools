import re
import argparse
import sys
import os
import csv
import subprocess

#Necessary: bcftools==1.9  and rtg-tools==3.10.1 (Install Conda environment for QC_Exome Tools: qc_exome_tools.yml)

def check_arg(args=None):
    parser = argparse.ArgumentParser(prog = 'script_dic_rgt_VCF_stats.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Dictionary of rgt_VCF_stats from file: all_samples_gtpos_fil_annot.vcf')

    
    parser.add_argument('-v, --version', action='version', version='v0.2')
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
        for sample , stats in d.items():
                #print("\nSample:", sample)
                for item in stats:
                    if 'SNP Het/Hom ratio' in item :
                        print(item + ':', stats[item])
                        ratio_str = stats[item]
                        ratio_str = ratio_str.split(' ')
                        ratio_number = float(ratio_str[0])

                        if ratio_number < 1.2 :
                            gender = 'Male'
                            print(sample, gender)
                            #gender_results_homo.writerow([ sample , ratio_number, gender])
                        else:
                            gender = 'Female'
                            print(sample, gender)
                            #gender_results_homo.writerow([ sample , ratio_number, gender])

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

    #Visualize CSV file using pandas:

    import pandas
    gender_pandas = pandas.read_csv(outfile)
    print(gender_pandas)


''''
        outfile = arguments.out
        
        with open( outfile , mode='w') as gender_file:
            gender_results_homo = csv.writer(gender_file, delimiter=',')
            gender_results_homo.writerow(['sample', 'Gender_HomoChrX_SNP Het/Hom ratio', 'Gender_HomoChrX_Gender' ])
            for sample , stats in d.items():
                #print("\nSample:", sample)
                for item in stats:
                    if 'SNP Het/Hom ratio' in item :
                        print(item + ':', stats[item])
                        ratio_str = stats[item]
                        ratio_str = ratio_str.split(' ')
                        ratio_number = float(ratio_str[0])

                        if ratio_number < 1.2 :
                            gender = 'Male'
                            print(sample, gender)
                            gender_results_homo.writerow([ sample , ratio_number, gender])
                        else:
                            gender = 'Female'
                            print(sample, gender)
                            gender_results_homo.writerow([ sample , ratio_number, gender])

        #Dictionary of gender_homo results:
        
        with open(outfile) as gender_homo:
            dr = csv.DictReader(gender_homo, delimiter=',')
            dic_gender_homo = {}
            for row in dr:
                dic_gender_homo[row['sample']]={}
                for key, value in row.items():
                    if not key == 'sample':
                        dic_gender_homo[row['sample']][key] = value

    print(dic_gender_homo)


'''












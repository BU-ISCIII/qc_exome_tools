import re
import argparse
import sys
import os
import csv
import subprocess


######################
##Function_Arguments##
######################
 

def check_arg(args=None):

    '''
	Description:
        Function collect arguments from command line using argparse
    Input:
        args # command line arguments
    Constant:
        None
    Variables
        parser
    Return
        parser.parse_args() # Parsed arguments
    '''

    parser = argparse.ArgumentParser(prog = 'parse_rtg_vcfstats.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Dictionary of rtg_VCF_stats from file: all_samples_gtpos_fil_annot.vcf')

    
    parser.add_argument('-v, --version', action='version', version='v0.2')
    parser.add_argument('--input', required= True, nargs='+',
                                    help = 'all_samples_gtpos_fil_annot.vcf files including path where are stored.')
    
    parser.add_argument('--out',  required= True,
                                    help = 'csv file name incluiding path where the csv file will be stored.')


    return parser.parse_args()


##################################
##Function_VCF_Stats_Dictionary ##
##################################

def rtg_vcfstats_dictionary (vcf_input):

    '''
    Description:
     #Necessary rtg-tools==3.10.1 (Install Conda environment for QC_Exome Tools: qc_exome_tools.yml)
     'Obtain vcf statistics using rtg-tools from vcf files and return a Dictionary of rtg_VCF_stats '
    
    Input:
    'all_samples_gtpos_fil_annot.vcf files including path where are stored.'
    
    Return:
      d (dictionary)
           
    '''  
      
    d={}
    for file in vcf_input:

        #Obtain rtg vcfstats from:

        found_samplename=False
        cmd = ["rtg" , "vcfstats"]
        parametro = [file]
        cmd.extend(parametro)
        cmd2 = ' '.join(cmd)
        print(cmd2)
        stats = subprocess.getoutput(str(cmd2))
        
        #Obtain sample name from vcf files* 
        #(*necessary when vcfstats are obtained from vcf files with only one sample):

        cmd_name = ["bcftools" , "query" , "-l"]
        cmd_name.extend(parametro)
        cmd_name2 = ' '.join(cmd_name)
        print(cmd_name2)
        name = subprocess.getoutput(cmd_name2)
        print('sample names:', name)
        name = name.split('\n')
    
        
    
        #Dictionary of rtg vcfstats results for each sample:

        stats = stats.split('\n')
        #print(stats)

        for line in stats:
            
            if len(line) == 0 :
                continue
            if 'Sample' in line :
                found_samplename = True
                print('found_samples:' , found_samplename)
                line = line.split(':')
                sample = line[1].strip()
                #print(sample)
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
                    data = '0'
                d[sample]['rtg_vcfstats_' + key]=  float(data) 
    
    return(d)
    
######################
##Function_Dic2CSV  ##
######################   

def dictionary2csv (dictionary, csv_file):

    '''

    Description:
        Function to create a csv from a dictionary
    Input:
        dictionary
    Return:
        csv file

   '''

    header = sorted(set(i for b in map(dict.keys, dictionary.values()) for i in b))
    with open(csv_file, 'w', newline="") as f:
        write = csv.writer(f)
        write.writerow(['sample', *header])
        for a, b in dictionary.items():
            write.writerow([a]+[b.get(i, '') for i in header])





##########
## MAIN ##
########## 
   
if __name__ == '__main__' :

    
    #Arguments: 
    
    '''
    Example arguments:
    
    --input /home/masterbioinfo/EXOME/Data/VCF/*_all_samples_gtpos_fil_annot.vcf
    --out /home/masterbioinfo/EXOME/Results/dic_rtg_vcfstats_all.csv
    '''
    
    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)

    
    #Dictionary of rtg_VCF_stats:
    
    dic_rtg_vcfstats_all = rtg_vcfstats_dictionary(arguments.input)
    
    print ('rtg_vcfstats_dictionary done')
    #print (dic_rtg_vcfstats_all)
    
    
    #Export dictionary as csv file:
    
    dictionary2csv (dic_rtg_vcfstats_all, arguments.out)

    print ('rtg_vcfstats_csv done')
    
  
    #Visualize CSV file using pandas:
     
    import pandas
    panda_file = pandas.read_csv(arguments.out)
    print(panda_file)




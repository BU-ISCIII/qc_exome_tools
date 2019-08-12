
import sys
import pysam
import os
import concurrent.futures as cfutures
import glob
import matplotlib.pyplot as plt
import statistics
import argparse
import csv


# Definition of required arguments (bam file, bed file , output path) with argparse module: 

def check_arg(args=None):
    parser = argparse.ArgumentParser(prog = 'determine_gender_using_idxstats_bedfile_dev7.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter, 
                                     description= 'Determine gender from bam file of WES using idxstats data and bed file')

    
    parser.add_argument('-v, --version', action='version', version='v0.9')
    parser.add_argument('--bam', required= True,
                                    help = 'Bam file including path where is stored.')
    parser.add_argument('--bed', required= True,
                                    help = 'Bed file including path where is stored.')
    parser.add_argument('--out',  required= True,
                                    help = 'Directory where the result files will be stored.')


    return parser.parse_args()



if __name__ == '__main__' :

    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)

    bams_name = os.path.basename(arguments.bam)
    print ('BAM file name: ', bams_name)

    
    #Calculate the number of total_bases and each chrom_bases from the exome targets of the BED file
    #and Remove prefix 'chr' form chromosome number: 

    total_bases = 0
    with open(arguments.bed) as bedfile:
        chrom_bases = { str(i):0 for i in range(1,23)}
        sex_chrom_bases = {'X' : 0 , 'Y' : 0 , 'M' : 0 }
        chrom_bases.update(sex_chrom_bases)	
        for line in bedfile:
            field=line.split('\t')
            field[0]=field[0].strip('chr')
            total_bases += (int(field[2])-int(field[1]))
            chrom_bases[field[0]] += (int(field[2])-int(field[1]))
        print('total_bases', total_bases )
        print('dicc de chrom_bases', chrom_bases)	


    #Obtain reads with idxstats and normalized with (A) Chrom_Length_idxstats or (B) Bed_targets 
         
    norm_reads=[]                   #normalized with (A) Chrom_Length
    norm_reads_bed=[]               #normalized with (B) Bed_targets_length
    total_chrom_length = 0
        
    workfile = pysam.idxstats(arguments.bam)
    line_workfile = workfile.split('\n')
    
    for j in range(24):
        column_workfile = line_workfile[j].split('\t')
        #print('data_workfile_idxstats:', column_workfile)
        total_chrom_length += int(column_workfile[1])
        #print('total_chrom_length:' , total_chrom_length)
        
        ratio=int(column_workfile[2])/int(column_workfile[1])
        #ratio=int(column_workfile[2]) * (int(column_workfile[1])/int(total_chrom_length))
        norm_reads.append(ratio)


        if j in range(0,21):
            chrom=str(j+1)
        elif j == 22:
            chrom='X'
        elif j == 23:
            chrom='Y'    

        bases_bed = chrom_bases[chrom]
        ratio_bed = int(column_workfile[2]) * (int(bases_bed)/int(total_bases))
        norm_reads_bed.append(ratio_bed)
        
                 

    #print('norm_reads' , norm_reads)
    #print('norm_reads_bed:', norm_reads_bed)

    #Calculate Xratio, Yratio, Mean_Auto using normalized reads with Chrom_Length_idxstats
    print ('Calculate Xratio, Yratio, Mean_Autosomic using normalized reads with Chrom_Length_idxstats:')

    mean_auto=statistics.mean(norm_reads[0:21])
    print('mean_auto', mean_auto)
    xratio=norm_reads[22]/mean_auto
    print('xratio', xratio)
    yratio=norm_reads[23]/mean_auto
    print('yratio', yratio)
    x_y_substract = xratio - yratio

    if x_y_substract >= 0.5:
        gender = 'Female'
        print('Xratio-Yratio in:' ,bams_name,'is', x_y_substract, 'Gender is ', gender)
    else:
        gender = 'Male'
        print('Xratio-Yratio in:' ,bams_name, 'is', x_y_substract, 'Gender is ', gender)

    #Calculate Xratio, Yratio, Mean_Auto using normalized reads with Bed_targets
    print ('Calculate Xratio, Yratio, Mean_Autosomic using normalized reads with Bed_targets:')

    mean_auto_bed=statistics.mean(norm_reads_bed[0:21])
    print('mean_auto_bed', mean_auto_bed)
    xratio_bed=norm_reads_bed[22]/mean_auto_bed
    print('xratio_bed', xratio_bed)
    yratio_bed=norm_reads_bed[23]/mean_auto_bed
    print('yratio_bed', yratio_bed)
    x_y_substract_bed = xratio_bed-yratio_bed

    #print(gender_bed)

    if x_y_substract_bed >= 0.55:
        gender_bed = 'Female'
        print('Xratio_bed-Yratio_bed in:' ,bams_name,'is', x_y_substract_bed, 'Gender_bed is ' , gender_bed )
    else:
        gender_bed = 'Male'
        print('Xratio_bed-Yratio_bed in:' ,bams_name, 'is', x_y_substract_bed, 'Gender_bed is ', gender_bed)

    #Comparation of gender results obtained with both methods:
    if gender == gender_bed:
        equal_gender_results = True
    else:
        equal_gender_results = False
    print('Obtained equal gender results: ', equal_gender_results)

    #Export results as csv file:
    
    outfile = os.path.join(arguments.out, 'gender_results_idxstats.csv')
    with open( outfile , mode='w') as gender_file:
        bams_name = bams_name.split('.')
        bams_name = bams_name[0]
        gender_results_idxstats = csv.writer(gender_file, delimiter=',')

        gender_results_idxstats.writerow(['sample', 'X/Auto', 'Y/Auto' , 'Gender' , 'X/Auto_bed', 'Y/Auto_bed' , 'Gender_bed' , 'Equal_results' ])
        gender_results_idxstats.writerow([ bams_name , xratio, yratio, gender , xratio_bed, yratio_bed, gender_bed , equal_gender_results ])

    with open(outfile) as gender_results_idxstats:
        dr = csv.DictReader(gender_results_idxstats, delimiter=',')
        dic_gender_idxstats = {}
        for row in dr:

            dic_gender_idxstats[row['sample']]={}
            for key, value in row.items():
                if not key == 'sample':
                    
                    print(key)
                    dic_gender_idxstats[row['sample']][key] = value

          
 
    print(dic_gender_idxstats)

'''
    import pandas
    gender_pandas = pandas.read_csv(outfile)
    print(gender_pandas)
'''

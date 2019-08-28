#!/bin/bash
 


#FORMAT Genome Reference to SDF: The format command converts the contents of sequence data files (FASTA/FASTQ/SAM/BAM) into the RTG Sequence Data File (SDF) format.


./Programas/rtg-tools-3.10.1/rtg format -o /home/masterbioinfo/EXOME/Data/hg19/genome_reference.SDF /home/masterbioinfo/EXOME/Data/hg19/human_g1k_v37.fasta



#Comprimir vcf a gz:
bgzip -c ./Escritorio/VCF_test/all_samples_gtpos_fil_annot.vcf > ./Escritorio/VCF_test/all_samples_gtpos_fil_annot.vcf.gz
tabix -p vcf ./Escritorio/VCF_test/all_samples_gtpos_fil_annot.vcf.gz




#Mendelian status and Results output in a file.txt
./Programas/rtg-core-non-commercial-3.10.1/rtg mendelian -i /home/masterbioinfo/Escritorio/VCF_test/ND0870/all_samples_gtpos_fil_annot.vcf -t /home/masterbioinfo/determine-gender/BAM_WES/genome_reference.SDF --pedigree /home/masterbioinfo/Escritorio/VCF_test/ND0870/familypedigri.ped > /home/masterbioinfo/Escritorio/VCF_test/results_mendelian_rtg.txt


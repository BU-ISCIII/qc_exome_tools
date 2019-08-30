#!/bin/bash



#Compress vcf to gz:

bgzip -c /home/masterbioinfo/EXOME/Data/VCF/ND0800/all_samples_gtpos_fil_annot.vcf > /home/masterbioinfo/EXOME/Data/VCF/ND0800/all_samples_gtpos_fil_annot.vcf.gz
tabix -p vcf /home/masterbioinfo/EXOME/Data/VCF/ND0800/all_samples_gtpos_fil_annot.vcf.gz


#Obtain each CHR variants with bcftools and Obtain vcfstats with rtg-tools:

for i in {1..22} X Y;
do
	touch /home/masterbioinfo/EXOME/Results/vcfstats_rtg/chr_$i.vcf
	echo $i 
    bcftools view -r $i /home/masterbioinfo/EXOME/Data/VCF/ND0800/all_samples_gtpos_fil_annot.vcf.gz > /home/masterbioinfo/EXOME/Results/vcfstats_rtg/chr_$i.vcf
    /home/masterbioinfo/Programas/rtg-tools-3.10.1/rtg vcfstats /home/masterbioinfo/EXOME/Results/vcfstats_rtg/chr_$i.vcf >>  /home/masterbioinfo/EXOME/Results/vcfstats_rtg/vcfstats_rtg_chr.txt
done






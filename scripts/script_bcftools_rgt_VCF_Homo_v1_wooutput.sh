


#Compress vcf to gz:

bgzip -c /home/masterbioinfo/EXOME/Data/VCF/ND0800/all_samples_gtpos_fil_annot.vcf > /home/masterbioinfo/EXOME/Data/VCF/ND0800/all_samples_gtpos_fil_annot.vcf.gz
tabix -p vcf /home/masterbioinfo/EXOME/Data/VCF/ND0800/all_samples_gtpos_fil_annot.vcf.gz



#Obtain CHR_X variants with bcftools:


bcftools view -r X /home/masterbioinfo/EXOME/Data/VCF/ND0800/all_samples_gtpos_fil_annot.vcf.gz >/home/masterbioinfo/EXOME/Data/VCF/ND0800/chr_X.vcf

# Obtain vcfstats with rtg-tools:


/home/masterbioinfo/Programas/rtg-tools-3.10.1/rtg vcfstats /home/masterbioinfo/EXOME/Data/VCF/ND0800/chr_X.vcf

bcftools norm -Ov -m -any /home/masterbioinfo/Escritorio/VCF_test/ND0870/all_samples_gtpos_fil_annot.vcf  |
 bcftools norm -Ov -f /home/masterbioinfo/EXOME/Data/hg19/human_g1k_v37.fasta  >  test.vcf

#Remove this filter. Problems because vcf output only contains variants of Chr1, why? 
#  bcftools annotate -x ID \
 #   -I +'%CHROM:%POS:%REF:%ALT' > test.vcf


plink2 --vcf test.vcf \
   --vcf-idspace-to _ \
    --const-fid \
    --allow-extra-chr 0 \
    --make-bed \
    --out output


#king to calculate kinship (results in king.kin)

king -b ./output.bed --kinship > result_kinship.txt

more king.kin > ./king_table_results.txt

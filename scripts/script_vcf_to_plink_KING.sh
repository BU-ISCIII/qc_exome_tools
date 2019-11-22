#! /bin/bash

#arguments:
#$1 is vcf file incluiding path:
vcf=$1

#example $1: /home/masterbioinfo/EXOME/Data/KING_vcf/TRIO047.vcf

#$2 is fasta file of genome reference incluiding path:
fasta=$2

#example $2: /home/masterbioinfo/EXOME/Data/hg19/human_g1k_v37.fasta

#Obtain TRIO name:

echo $vcf 

trio=$(basename $vcf | cut -d. -f1)

echo $trio


#Make directory with results:

mkdir $trio
cd $trio


bcftools norm -Ov -m -any $vcf  | bcftools norm -Ov -f $fasta  >  $trio.norm.vcf

#Remove this filter. Problems because vcf output only contains variants of Chr1, why? 
#  bcftools annotate -x ID \
 #   -I +'%CHROM:%POS:%REF:%ALT' > test.vcf


plink2 --vcf $trio.norm.vcf \
   --vcf-idspace-to _ \
    --const-fid \
    --allow-extra-chr 0 \
    --make-bed \
    --out $trio


#king to calculate kinship (results in king.kin):

king -b ./$trio.bed --kinship > $trio.logs_kinship.txt

more king.kin > ./$trio.king_table_results.txt

##
##example to run this script: 
## bash /home/masterbioinfo/desarrollo/qc_exome_tools/scripts/script_vcf_to_plink_KING.v0.2.sh /home/masterbioinfo/EXOME/Data/KING_vcf/TRIO047.vcf /home/masterbioinfo/EXOME/Data/hg19/human_g1k_v37.fasta
##



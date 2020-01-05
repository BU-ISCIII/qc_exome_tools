#! /bin/bash



#example $1: /home/masterbioinfo/EXOME/Data/KING_vcf/TRIO047.vcf

vcf=$1

#$2 is fasta file of genome reference incluiding path:
fasta=$2

echo $vcf 

trio=$(basename $vcf | cut -d. -f1)

echo $trio


#Make directory with results:

mkdir $trio
cd $trio

#To remove multiallelic from vcf files using "bcftools norm"

bcftools norm -Ov -m -any $vcf  | bcftools norm -Ov -f $fasta  >  $trio.norm.vcf


#Obtain kinship using plink2 (required v2.0) -make-king-table to obtain a table .kin0: 

plink2 --vcf $trio.norm.vcf  --make-king-table --allow-extra-chr --out $trio.king.table

cd ..

############################################################################
#Optional:
#to obtain kinship coeficients in a matrix form .king ( to heatmap graphs) using --make-king:
#plink2 --vcf /path/to/merge.vcf  --make-king --allow-extra-chr --out path/to/results/merge.king.matrix

#############################################################################


#############################################################################
##Example to run this script: 
## bash /home/masterbioinfo/desarrollo/qc_exome_tools/scripts/script_vcf_to_plink_king_table.sh /home/masterbioinfo/EXOME/Data/KING_vcf_pruebas/TRIO047.vcf /home/masterbioinfo/EXOME/Data/hg19/human_g1k_v37.fasta 
##############################################################################

###############################################################################
##Example To run this script in several vcfs:
##
##find /home/masterbioinfo/EXOME/Data/KING_vcf_pruebas/ -name "*.vcf" > vcfs.txt
##
##cat vcfs.txt | xargs -I % echo "bash /home/masterbioinfo/desarrollo/qc_exome_tools/scripts/script_vcf_to_plink_king_table.sh % /home/masterbioinfo/EXOME/Data/hg19/human_g1k_v37.fasta" > _00_king_test.sh
##
##bash _00_king_test.sh
#############################################################################

#############################################################################
#To obtain kinship between diferents vcf files:

#Compress vcf to gz: 
#example:
# bgzip -c /path to/file.vcf > /path/file.vcf.gz
# tabix -p vcf /path/file.vcf.gz
#
#to merge several vcf.gz:
#first, obtain a list of vcf.gz files and copy:
# ls *.vcf.gz |xargs
#
#second,merge with vcftools, vcf-merge: 
#/home/masterbioinfo/Programas/vcftools_0.1.13/perl/vcf-merge TRIO058.vcf.gz TRIO059.vcf.gz (copy list of vcf.gz files) > merge.vcf
#
#
##IMP: NOT remove multiallelic from merge.vcf files using "bcftools norm"(doesnt run fine)
##Directly Obtain kinship using plink2 (required v2.0) -make-king-table with merge.vcf file
#example:
#plink2 --vcf merge.vcf  --make-king-table --allow-extra-chr --out merge.king.table

#to obtain kinship coeficients in matrix form .king ( to heatmap graphs):
#plink2 --vcf /path/to/merge.vcf  --make-king --allow-extra-chr --out path/to/results/merge.king.matrix

#############################################################################



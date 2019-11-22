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


bcftools norm -Ov -m -any $vcf  | bcftools norm -Ov -f $fasta  >  $trio.norm.vcf


plink2 --vcf $trio.norm.vcf  --make-king-table --allow-extra-chr --out $trio.king.table

cd ..



##
##example to run this script: 
## bash /home/masterbioinfo/desarrollo/qc_exome_tools/scripts/script_vcf_to_plink_king_table.sh /home/masterbioinfo/EXOME/Data/KING_vcf_pruebas/TRIO047.vcf /home/masterbioinfo/EXOME/Data/hg19/human_g1k_v37.fasta 
##




##
##Example To run this script in several vcfs:
##
##find /home/masterbioinfo/EXOME/Data/KING_vcf_pruebas/ -name "*.vcf" > vcfs.txt
##
##cat vcfs.txt | xargs -I % echo "bash /home/masterbioinfo/desarrollo/qc_exome_tools/scripts/script_vcf_to_plink_king_table.sh % /home/masterbioinfo/EXOME/Data/hg19/human_g1k_v37.fasta" > _00_king_test.sh
##
##bash _00_king_test.sh
##



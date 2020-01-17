
 find ./EXOME/Data/BAM/ -name "*.bam" > ./EXOME/Data/BAM/bam-files.txt
 
 rtg coverage -t /home/masterbioinfo/determine-gender/BAM_WES/genome_reference.SDF --bed-regions ./EXOME/Data/MedExomePlusMito_hg19_capture_targets_ped.bed -s 20 -o ./EXOME/Results/coverage -I ./EXOME/Data/BAM/bam-files.txt
 
 
 #Para quitar chr de chromosomas
 #guardo copia
 cp ./EXOME/Data/MedExomePlusMito_hg19_capture_targets_ped.bed ./EXOME/Data/MedExomePlusMito_hg19_capture_targets_ped.bed.back
 
 perl -i -pe 's/chr//g' ./EXOME/Data/MedExomePlusMito_hg19_capture_targets_ped.bed

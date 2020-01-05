#[sex\_determination\_using\_idxstats.py](https://github.com/BU-ISCIII/qc_exome_tools/blob/develop/scripts/sex_determination_using_idxstats.py)

## Description:
Pyhton script to determine the genetic sex examining the read counts in X and Y chromosomes from the whole exome BAM files.

 
The number of aligned reads on X , Y chromosomes and autosomes(Auto) were obtained running [samtools idxstats](http://www.htslib.org/doc/samtools-idxstats.1.html) with the phyton module [pysam](https://pysam.readthedocs.io/en/latest/api.html) , and normalised in two different ways: (a) dividing them by the corresponding chromosome length or (b) dividing by the number of bases of the exome targeted regions for each chromosome according to the BED file of the used WES capture kit. 

The X/Auto and Y/Auto ratios were calculated: 

- **X/Auto ratio** should be higher in females (theoretical 1) than in males(theoretical 0.5) 
-  **Y/Auto ratio** should be higher in males than in females(theoretical 0.0) 

To determine the genetic sex, if the **(X/Auto ratio) – (Y/Auto ratio)** is equal or higher to **0.5**, the sample was considered **"female"** and if smaller, it was considered to be **"male"**.


## Usage:

###Dependencies:
It is necessary **pysam==0.15.3** (We recommend to execute this script installing the conda qc-exome-tools environment with the [qc-exome-tools.yml file](https://github.com/BU-ISCIII/qc_exome_tools/blob/develop/qc_exome_tools.yml))  



###Input files:

The following input arguments are required:
 
*  --bam  The BAM files including path where these files are stored
*  --bed The BED files of the used WES Capture kit including path
  

``` 
--bam /path/to/*.bam
--bed /path/to/bed_files/Library_capture_targets.bed
```
 
  
### Output files:

A dictionary converted to csv file with the determined_sex results:

```
--out /path/to/Results/dic_gender_idxstats_bed_date.csv
``` 

Column names of the obtained csv file are:

- **idx\_X/Auto** value of X/Auto ratio using normalized reads with Chrom\_Length\_idxstats
- **idx\_Y/Auto** value of Y/Auto ratio using normalized reads with Chrom\_Length\_idxstats
- **idsx\_gender** genetic sex determined with (idx\_X/Auto) - (idx\_Y/Auto)
- **bed\_X/Auto** value of X/Auto ratio using normalized reads with Bed_targets
- **bed\_Y/Auto** value of Y/Auto ratio using normalized reads with Bed_targets
- **bed\_gender** genetic sex determined with (bed\_X/Auto) - (bed\_Y/Auto)
- **idx\_bed\_Equal\_results** boolean values to compare equal results between  **idsx\_gender** and **bed\_gender**



## Example

For running in a local computer:

```
python3 /path/to/scripts/sex_determination_using_idxstats.py
--bam /path/to/*.bam
--bed /path/to/bed_files/Library_capture_targets.bed
--out /path/to/RESULTS/dic_gender_idxstats_bed_date.csv

```
 
For submission to the SGE cluster:

```

qsub -V -b y -j y -cwd -N "sex_idxstats_date" 
-q all.q python3 /path/to/scripts/sex_determination_using_idxstats.py
--bam /path/to/*.bam
--bed /path/to/bed_files/Library_capture_targets.bed
--out /path/to/RESULTS/dic_gender_idxstats_bed_date.csv

```
   
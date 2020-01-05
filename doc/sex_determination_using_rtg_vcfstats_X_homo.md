# [sex\_determination\_using\_rtg\_vcfstats\_X\_homo.py](https://github.com/BU-ISCIII/qc_exome_tools/blob/develop/scripts/sex_determination_using_rtg_vcfstats_X_homo.py)

## Description:
Pyhton script to determine the genetic sex examining the proportion of hetezygous SNPs (**"SNP Het/Hom ratio"**) in the X chromosome. 

The variants of X chromosome from vcf files are selected first with [bcftools](http://samtools.github.io/bcftools/bcftools.html#view) and then, the **"SNP Het/Hom ratio"** value of ChrX variants is obtained with [rtg-tools vcfstats](https://cdn.rawgit.com/RealTimeGenomics/rtg-tools/master/installer/resources/tools/RTGOperationsManual/rtg_command_reference.html#vcfstats).
To determine the genetic sex, if the **"SNP Het/Hom ratio"** of X chomosome variants is equal or higher to **0.77**, the sample was considered **"female"** and if smaller, it was considered to be **"male"**.


## Usage:

### Dependencies:
It is necessary **bcftools==1.9** and **rtg-tools==3.10.1** (We recommend to execute this script installing the conda qc-exome-tools environment with the [qc-exome-tools.yml file](https://github.com/BU-ISCIII/qc_exome_tools/blob/develop/qc_exome_tools.yml))  



### Input files:
The vcf files including path where these files are stored:

``` 
--input /path/to/*.vcf

```
 
  
### Output files:

A dictionary converted to csv file with the determined_sex results:

```
--out /path/to/Results/dic_sex_rtg_xhomo_date.csv
``` 

Column names of the obtained csv file are:

- **"HomoChrX\_SNP\_Het/Hom\_ratio"** value of SNP Het/Hom ratio of X cromosome variants.

- **"HomoChrX\_Gender"** genetic sex determined with **X chromosome SNP Het/Hom ratio**.



## Example

For running in a local computer:

```
python3 /path/to/scripts/sex_determination_using_rtg_vcfstats_X_homo.py
--input /path/to/*.vcf
--out /path/to/RESULTS/dic_sex_rtg_xhomo_date.csv

```
 
For submission to the SGE cluster:

```

qsub -V -b y -j y -cwd -N "sex_idxstats_date" 
-q all.q python3 /path/to/scripts/sex_determination_using_rtg_vcfstats_X_homo.py
--input /path/to/*.vcf
--out /path/to/RESULTS/dic_sex_rtg_xhomo_date.csv

```
   
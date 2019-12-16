# parse-familypedigree-ped.py

## Description:
Python script to create a Dictionary and csv file with the family_pedigree data obtained from a [ped file](https://gatkforums.broadinstitute.org/gatk/discussion/7696/pedigree-ped-files):


The PED file is a white-space (space or tab) delimited file and the first six columns are mandatory:

*   Family ID
*   Individual ID
*   Paternal ID
*   Maternal ID
*   Sex (1=male; 2=female; other=unknown)
*   Phenotype

The IDs are alphanumeric: the combination of family and individual ID should uniquely identify a person. If an individual's sex is unknown, then any character other than 1 or 2 can be used in the fifth column.

A PED file must have 1 and only 1 phenotype in the sixth column. The phenotype can be either a quantitative trait or an "affected status" column:
Affected status should be coded as follows:

*   -9 missing
*   0 missing
*   1 unaffected
*   2 affected

## Input files:

familypedigree.ped files including path where are stored 

```
--input /path/to/*.ped
```
  
## Output files:
A dictionary converted to csv file with the pedigree data.

Column names of the obtained csv file:

* 	sample
*  ped_familyID
*  ped_maternalID
*  ped_paternalID
*  ped_gender
*  ped_phenotype

```
--out /path/to/dic_pedigree_date.csv
``` 

## Example

For running in a local computer:

```
python3 /path/to/parse_familypedigree_ped.py 
--input /path/to/*.ped 
--out /path/to/dic_pedigree_date.csv

```
 

For submission to the SGE cluster:

```
qsub -V -b y -j y -cwd -N "parse_familypedigree_date" 
-q all.q python3 /path/to/parse_familypedigree_ped.py 
--input /path/to/*.ped 
--out /path/to/dic_pedigree_date.csv

```
   
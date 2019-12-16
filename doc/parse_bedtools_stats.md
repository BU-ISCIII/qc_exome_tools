# parse-bedtools-stats.py

## Description:
Python script to create a Dictionary and csv file of bedtools statistics from  "exons\_not\_covered\_stats.csv" files obtained with [bedtools](https://bedtools.readthedocs.io/en/latest/content/tools/coverage.html) in [BU-ISCIII-exome-pipeline](https://github.com/BU-ISCIII/exome_pipeline).

Statistics in "exons\_not\_covered\_stats.csv" files:

* exons\_below\_20: number of exons with coverage below 20X
* fr\_covered: fraction of exons covered
* fr\_NOT\_covered: fraction of exons non-covered



## Input files:

"exons\_not\_covered\_stats.csv" files including path where are stored: 

```
--input /path/to/bedtools/*.csv
    
```
  
## Output files:
A dictionary converted to csv file with the exons\_not\_covered\_statistics:

Column names of the obtained csv file:

* sample
* exons\_below\_20
* fr\_covered
* fr\_NOT\_covered


```
--out /path/to/Results/dic_bedtools_all.csv
``` 

## Example

For running in a local computer:

```
python3 /path/to/parse_bedtools_stats.py 
--input /path/to/bedtools/*.csv 
--out /path/to/RESULTS/dic_bedtools.csv  

```
 

For submission to the SGE cluster:

```
qsub -V -b y -j y -cwd -N "parse_bedtools_date" -q all.q
python3 /path/to/parse_bedtools_stats.py 
--input /path/to/bedtools/*.csv 
--out /path/to/RESULTS/dic_bedtools.csv 

```
   
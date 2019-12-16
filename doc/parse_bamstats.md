# parse-bamstats.py

## Description:
Python script to create a Dictionary and csv file with the statistics of bamstats.txt files obtained with [BamUtil](https://genome.sph.umich.edu/wiki/BamUtil:_stats#Basic_.28--basic.29) in [BU-ISCIII-exome-pipeline](https://github.com/BU-ISCIII/exome_pipeline):

BamUtil Basic statistics (`--basic`) 

Prints summary statistics from .bam files in bamstats.txt:

* TotalReads - # of reads that are in the file 
* MappedReads - # of reads marked mapped in the flag 
* PairedReads - # of reads marked paired in the flag 
* ProperPair - # of reads marked paired AND proper paired in the flag 
* DuplicateReads - # of reads marked duplicate in the flag 
* QCFailureReads - # of reads marked QC failure in the flag 
* MappingRate(%) - # of reads marked mapped in the flag / TotalReads 
* PairedReads(%) - # of reads marked paired in the flag / TotalReads 
* ProperPair(%) - # of reads marked paired AND proper paired in the flag / TotalReads 
* DupRate(%) - # of reads marked duplicate in the flag / TotalReads 
* QCFailRate(%) - # of reads marked QC failure in the flag / TotalReads 
* TotalBases - # of bases in all reads 
* BasesInMappedReads - # of bases in reads marked mapped in the flag

```
##Example for runnig BamUtil in SGE cluster:

qsub -V -b y -cwd -e sample_bamstat.txt -N BAMUTIL.sample -q all.q bam stats 
--regionList /path/to/capture_targets.bed 
--in /path/to/sample.woduplicates.bam 
--baseSum --basic

```




## Input files:

bamstats.txt files including path where are stored 

```
--input /path/to/sample_bamstats.txt
    
```
  
## Output files:
A dictionary converted to csv file with the bamstats.

Column names of the obtained csv file:

* sample
* bamstats_BasesInMappedReads(e6)
* bamstats_DuplicateReads(e6)
* bamstats_DupRate(%)
* bamstats_MappedReads(e6)
* bamstats_MappingRate(%)
* bamstats_PairedReads(%)
* bamstats_PairedReads(e6)
* bamstats_ProperPair(%)
* bamstats_ProperPair(e6)
* bamstats_QCFailRate(%)
* bamstats_QCFailureReads(e6)
* bamstats_TotalBases(e6)
* bamstats_TotalReads(e6)


```
--out /path/to/dic_bamstats_all.csv
``` 

## Example

For running in a local computer:

```
python3 /path/to/parse_bamstats.py 
--input /path/to/*bamstat.txt
--out /path/to/RESULTS/dic_bamstats.csv

```
 

For submission to the SGE cluster:

```
qsub -V -b y -j y -cwd -N "parse_bamstats_date" -q all.q python3 /path/to/parse_bamstats.py 
--input /path/to/*bamstat.txt
--out /path/to/RESULTS/dic_bamstats.csv

```
   
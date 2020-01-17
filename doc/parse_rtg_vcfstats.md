# [parse\_rtg\_vcfstats.py](https://github.com/BU-ISCIII/qc_exome_tools/blob/develop/scripts/parse_rtg_vcfstats.py)

## Description:
Python script to create a Dictionary and csv file with the [rtg-tools vcfstats](https://cdn.rawgit.com/RealTimeGenomics/rtg-tools/master/installer/resources/tools/RTGOperationsManual/rtg_command_reference.html#vcfstats) statistics obtained from the vcf files of the [BU-ISCIII-exome-pipeline](https://github.com/BU-ISCIII/exome_pipeline):

     

### rtg-tools vcfstats

**Synopsis:**

Display simple statistics about the contents of a set of VCF files.

**Syntax:**

<div class="highlight-text">

<div class="highlight">

<pre><span></span>$ rtg vcfstats [OPTION]... FILE+
</pre>

</div>

</div>
**Example:**
<div class="highlight-text">

<div class="highlight">

<pre><span></span>$ rtg vcfstats /data/human/wgs/NA19240/snp_chr5.vcf.gz

Location                      : /data/human/wgs/NA19240/snp_chr5.vcf.gz
Passed Filters                : 283144
Failed Filters                : 83568
SNPs                          : 241595
MNPs                          : 5654
Insertions                    : 15424
Deletions                     : 14667
Indels                        : 1477
Unchanged                     : 4327
SNP Transitions/Transversions : 1.93 (210572/108835)
Total Het/Hom ratio           : 2.13 (189645/89172)
SNP Het/Hom ratio             : 2.12 (164111/77484)
MNP Het/Hom ratio             : 3.72 (4457/1197)
Insertion Het/Hom ratio       : 1.69 (9695/5729)
Deletion Het/Hom ratio        : 2.33 (10263/4404)
Indel Het/Hom ratio           : 3.13 (1119/358)
Insertion/Deletion ratio      : 1.05 (15424/14667)
Indel/SNP+MNP ratio           : 0.13 (31568/247249)
</pre>

</div>

</div>



## Input files:

The vcf files including path where vcf files are stored

```
 --input /path/to/*.vcf

```
  
## Output files:

A dictionary converted to csv file with the rtg vcfstats:


```
 --out /path/to/Results/dic_rtg_vcfstats.csv
``` 

Column names of the obtained csv file:

* sample
* rtg\_vcfstats\_Total Het/Hom ratio
* rtg\_vcfstats\_SNPs
* rtg\_vcfstats\_SNP Transitions/Transversions
* rtg\_vcfstats\_SNP Het/Hom ratio
* rtg\_vcfstats\_Same as reference
* rtg\_vcfstats\_Phased Genotypes
* rtg\_vcfstats\_MNPs
* rtg\_vcfstats\_MNP Het/Hom ratio
* rtg\_vcfstats\_Missing Genotype
* rtg\_vcfstats\_Insertions
* rtg\_vcfstats\_Insertion/Deletion ratio
* rtg\_vcfstats\_Insertion Het/Hom ratio
* rtg\_vcfstats\_Indels
* rtg\_vcfstats\_Indel/SNP+MNP ratio
* rtg\_vcfstats\_Indel Het/Hom ratio
* rtg\_vcfstats\_Deletions
* rtg\_vcfstats\_Deletion Het/Hom ratio



## Example
**_IMP:_** For this script is necessary **rtg-tools==3.10.1** (Install Conda environment with [qc-exome-tools.yml file](https://github.com/BU-ISCIII/qc_exome_tools/blob/develop/qc_exome_tools.yml))

For running in a local computer:



```
python3 /path/to/parse_rtg_vcfstats.py
--input /path/to/*.vcf
--out /path/to/RESULTS/dic_rtg_vcfstats_date.csv

```
 

For submission to the SGE cluster:

```

qsub -V -b y -j y -cwd -N "parse_rtg_vcfstats_date" -q all.q python3 /path/to/parse_rtg_vcfstats.py
--input /path/to/*.vcf
--out /path/to/RESULTS/dic_rtg_vcfstats_date.csv

```
   
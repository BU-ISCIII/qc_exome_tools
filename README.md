# **qc-exome-tools**

<br>


## INTRODUCTION


[Scripts](https://github.com/BU-ISCIII/qc_exome_tools/tree/develop/scripts) for the development of  quality control (QC) tools for the different stages of [BU-ISCIII-exome-pipeline](https://github.com/BU-ISCIII/exome_pipeline/blob/develop/doc/output.md):

* Tools for parsing statistics obtained in the Preprocesing, Mapping and Variant Calling steps.

* Tools for determing genetic-sex and relationship: useful tools to confirm the pedigree data and to check cross-contamination in the WES samples.


<br>

![image](https://github.com/BU-ISCIII/qc_exome_tools/blob/develop/img/imgqctools.png)

<br>

## INSTALLATION & DEPENDENCIES

In order to use these scripts, you can download them or you can also clone this repository from GitHub to create a local copy on your computer (if git is installed):

```
git clone https://github.com/BU-ISCIII/qc_exome_tools

```

Dependencies are listed in the [qc-exome-tools.yml file](https://github.com/BU-ISCIII/qc_exome_tools/blob/develop/qc_exome_tools.yml)

```
dependencies:

    - python=>3.7.1
    - pip==19.1.1
    - pysam==0.15.3
    - pandas==0.25.1
    - bcftools==1.9
    - rtg-tools==3.10.1
    - samtools==1.9
    - htslib==1.9
    - plink2=>1.9
```

We recommend to execute these scripts using the conda qc-exome-tools environment: 

1. Install [anaconda or miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#installation) (if not installed)

2. Activate conda:   
```
conda activate
```
3. Install conda enviroment with yml file:
```
conda env create -f /path/to/qc_exome_tools.yml
```

4. Activate conda enviroment:
```
conda activate qc_exome_tools
```

	

## DESCRIPTION & USAGE


### A) Tools for parsing statistics obtained in the Preprocesing, Mapping and Variant Calling steps:

* [parse-fastqc-all.py](doc/parse_fastqc_all.md)
* [parse-bamstats.py](doc/parse_bamstats.md)
* [parse-hsmetrics.py](doc/parse_hsmetrics.md)
* [parse-bedtools-stats.py](doc/parse_bedtools_stats.md)
* [parse-rtg-vcfstats.py](doc/parse_rtg_vcfstats.md)

### B) Tools for determing genetic-sex and relationship:

* [parse-familypedigree-ped.py](doc/parse_familypedigree_ped.md)
* [script-vcf-to-plink-king-table.sh](doc/script_vcf_to_plink_king_table.md)
* [sex-determination-using-idxstats.py](doc/sex_determination_using_idxstats.md)
* [sex-determination-using-rtg-vcfstats-X-homo.py](doc/sex_determination_using_rtg_vcfstats_X_homo.md)


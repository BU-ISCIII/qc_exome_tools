import re

bedtools_path ="/home/masterbioinfo/EXOME/Data/exons_not_covered_stats.csv"
d={}
heather=False
with open(bedtools_path) as bedstats_file:
    print('tipo', type(bedstats_file))

    for line in bedstats_file:
        line=line.strip('\n')
        #print(line)
        if len(line) == 0 :
            continue
        if 'exons' in line :
            heather = True
            print('encuentre sample:' , heather)
            continue

        if heather :
            line = line.split('\t')
            print(line)
            sample = line[0].split('.')
            sample = sample[0]
            sample = re.sub(r"\"", "", sample)
            print( 'sample', sample)
            d[sample] = {}
            d[sample]['exons_below_20']= float(line[1])
            d[sample]['fr_covered']= float(line[2])
            d[sample]['fr_NOT_covered']= float(line[3])
print(d)
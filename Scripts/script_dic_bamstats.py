import re
import os
d={}
bamstats_path ="/home/masterbioinfo/EXOME/Data/ND0801_bamstat.txt"
sample = (os.path.basename(bamstats_path)).split('_')
sample = sample[0]
print('sample:', sample)
found_start=False
d[sample]={}
print(d)


with open(bamstats_path) as bamstats_file:
    print('type_file', type(bamstats_file))

    for line in bamstats_file:
        line=line.strip('\n')
        if len(line) == 0 :
            continue
        if 'Number of records' in line :
            found_start = True
            print('encuentre start:' , found_start)
            continue
        if found_start :
            line = line.split('\t')
            key=line[0]
            value=float(line[1])
            d[sample][key]= value
        
            
print('Dictionary_Bamstats:' , d)


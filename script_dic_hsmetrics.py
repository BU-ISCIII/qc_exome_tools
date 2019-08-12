import re
import os
d={}
hsmetrics_path ="/home/masterbioinfo/EXOME/Data/ND0801_hsMetrics.out"
sample = (os.path.basename(hsmetrics_path)).split('_')
sample = sample[0]
print('sample:', sample)
found_start=False
found_value=False
d[sample]={}
print(d)

with open(hsmetrics_path) as hsmetrics_file:
    print('type_file', type(hsmetrics_file))

    for line in hsmetrics_file:
        line=line.strip('\n')
        if len(line) == 0 :
            continue
        if 'METRICS CLASS' in line :
            found_start = True
            print('encuentre start:' , found_start)
            continue
        if found_start :
            keys = line.split('\t')
            print(keys)
            found_value=True
            found_start=False
            continue
        if found_value:
            values=line.split('\t')
            
            break
    for i in range(len(keys)):
        d[sample][keys[i]]= values[i]
        
        #convert string to numbers
        for val in d[sample][keys[i]] :
            try:
                d[sample][keys[i]]= float(values[i])
            except (ValueError, TypeError):
                d[sample][keys[i]]= values[i]

#print(len(keys), '-', len(values))
            
print('Dictionary_hsmetrics:' , d)





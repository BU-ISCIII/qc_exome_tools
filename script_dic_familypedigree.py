import re

ped_path ="/home/masterbioinfo/EXOME/Data/VCF/ND0500/familypedigri.ped"
d={}
with open(ped_path) as pedfile:

    print('tipo', type(pedfile))
    for line in pedfile:
        line=line.strip('\n')
        print(line)
        print(type(line))
        line = re.sub(r"\s+", "\t", line)
        line=line.split('\t')
        print(line)    
        print(type(line))
        sample=line[1]
        print('sample', sample)
        d[sample]={}
        d[sample]['familyID_ped']=line[0]
        d[sample]['paternalID_ped']=line[2]
        d[sample]['maternalID_ped']=line[3]
        d[sample]['gender_ped']=line[4]
        d[sample]['phenotype_ped']=line[5]
           
        
print(d)

#Run bash script for rtg vcfstats:
import subprocess


stats = subprocess.getoutput(str ('/home/masterbioinfo/Programas/rtg-tools-3.10.1/rtg vcfstats /home/masterbioinfo/EXOME/Data/VCF/ND0800/all_samples_gtpos_fil_annot.vcf') )


#Dictionary of rtg vcfstats results for each sample: 

d={}
found_samplename=False
stats = stats.split('\n')
#print(stats)

for line in stats:
    
    if len(line) == 0 :
        continue
    if 'Sample' in line :
        found_samplename = True
        print('encuentre sample:' , found_samplename)
        line = line.split(':')
        name = line[1].strip()
        print(name)
        d[name] = {}
        continue
    if found_samplename :
        line = line.split(':')
        key=line[0].rstrip()
        #print(line)
        value=line[1].lstrip()
        data = value.split(' ')[0]
        data= data.replace('%', '')
        if '-'  in data:
            data = '0'
        d[name][key]=  float(data) 
        
print('Dictionary_VCFstats :' , d)















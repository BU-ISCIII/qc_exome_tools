import re
import argparse
import sys
import glob
import os
import csv

# Definition of required arguments (input_file path , output path) with argparse module:

def check_arg(args=None):
    parser = argparse.ArgumentParser(prog = 'script_dic_hsmetrics_v0.2.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description= 'Dictionary of hsmetrics_data from hsmetrics.out file')


    parser.add_argument('-v, --version', action='version', version='v0.2')
    parser.add_argument('--input', required= True, nargs="+",
                                    help = 'Directory where hsMetrics.out files are stored.')
    parser.add_argument('--out',  required= True,
                                    help = 'csv file name incluiding path where the csv file will be stored.')


    return parser.parse_args()

if __name__ == '__main__' :

    arguments = check_arg(sys.argv[1:])
    print('Arguments used: ' , arguments)

    #Dictionary of hsMetrics.out data:
    d={}
    for file in arguments.input :
        sample = (os.path.basename(file)).split('_')
        sample = sample[0]
        #print('sample:', sample)
        found_start=False
        found_value=False
        d[sample]={}
        #print('Dictionary samples', d)

        with open(file) as hsmetrics_file:
            #print('type_file', type(hsmetrics_file))

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
                    found_value=True
                    found_start=False
                    continue
                if found_value:
                    values=line.split('\t')
                    break
            hs_keys = ["hsMetrics_" + key for key in keys ]
            print('hskeys', hs_keys)

            for i in range(len(hs_keys)):
                d[sample][hs_keys[i]]= values[i]

                #convert string to numbers
                for val in d[sample][hs_keys[i]] :
                    try:
                        d[sample][hs_keys[i]]= float(values[i])
                    except (ValueError, TypeError):
                        d[sample][hs_keys[i]]= values[i]

        #print(len(hs_keys), '-', len(values))

        print('Dictionary_hsmetrics:' , d)

        #Export dictionary as csv file:

        outfile = arguments.out
        dic = d #Nested dictionary

        headers = list(list (dic.values())[0].keys()) #Encabezado de las columnas
        #print (len (headers))
        #print (headers)

    with open(outfile, "w") as f:
        w = csv.writer( f )

        w.writerow(['sample'] + headers)# printea la primera fila

        parameters = list(list (dic.values())[0].keys())
        #print (parameters)
        for sample in dic.keys():
            #print (dic.keys())
            w.writerow([sample] + [dic[sample][parameter] for parameter in parameters])



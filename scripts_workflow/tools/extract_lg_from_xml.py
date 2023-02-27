import sys, getopt
import xml.etree.ElementTree as ET

def main(argv):
   global inputfile
   global outputfile
   inputfile = ''
   outputfile = ''
   opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print ('Input file is ', inputfile)
   print ('Output file is ', outputfile)
   
def extract_lg(inputfile, outputfile):
    tree = ET.parse(open(inputfile, encoding='utf-8'))
        
    list_sents = []
    nb_sent = 0

    for sent in tree.findall('.//s'):
        len_sent = 0
        nb_sent += 1
        text_sent = []
        for w in sent.findall('.//w'):
            len_sent += 1
            
            if len(w)!=0:
                for choice in w.findall('.//choice'):
                    for choice in w.findall('.//choice'):
                        for sic, corr in zip(w.findall('.//sic'), w.findall('.//corr')):
                            form = corr.text
                            sic = str(sic.text)

                    for choice in w.findall('.//choice'):
                        for orig, reg in zip(w.findall('.//orig'), w.findall('.//reg')):
                            form = reg.text
                            orig = str(orig.text)
            else:
                form = w.text
            
            text_sent.append(form)
        
        if len_sent > 80:
            x = str(nb_sent)+' \ len: '+str(len_sent)+' \ Long= Yes'+'\n'+' '.join(text_sent)
            list_sents.append(x)
        else:
            x = str(nb_sent)+' \ len: '+str(len_sent)+'\n'+' '.join(text_sent)
            list_sents.append(x)                
        
    outputfile = outputfile.rstrip('.txt')+'.txt'

    with open(outputfile, "w", encoding="utf-8") as out:
        for i in list_sents:
            out.write(i)
            out.write('\n')
            out.write('\n')

if __name__ == "__main__":
   main(sys.argv[1:])
   extract_lg(inputfile, outputfile)
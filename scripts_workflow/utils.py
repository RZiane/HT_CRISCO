import sys, getopt
import xml.etree.ElementTree as ET
import copy
from tqdm import tqdm

def def_args(argv):
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

   return inputfile, outputfile

### XML processing ##############################################
def indent_xml(elem, level=0, more_sibs=False):
    i = "\n"
    if level:
        i += (level-1) * '\t'
    num_kids = len(elem)
    if num_kids:
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
            if level:
                elem.text += '\t'
        count = 0
        for kid in elem:
            indent_xml(kid, level+1, count < num_kids - 1)
            count += 1
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
            if more_sibs:
                elem.tail += '\t'
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            if more_sibs:
                elem.tail += '\t'

def build_div(root, div_type):
    
    type_ = str(div_type)
    
    x = [ele.tag for ele in list(root)]
    if 'head' in x:
        for id_, ele in enumerate(list(root)):        
            if ele.tag == 'head':
                if list(root)[id_+1].tag!='head':

                    new_head = ET.Element("head")
                    new_head.text = ele.text

                    ele.tag = 'div'
                    ele.set ('type', type_)
                    ele.text = ''

                    ele.append(new_head)

                    for ele2 in list(root)[id_+1:]:
                        if ele2.tag != 'head':
                            ele2_clone = copy.deepcopy(ele2)
                            ele.append(ele2_clone)
                            ele2.set('append', 'yes')
                        else:
                            break
    else:
        # fabrication nouvel élément div
        new_div = ET.Element("div")
        new_div.set ('type', type_)
        for id_, ele in enumerate(list(root)):

            ele_clone = copy.deepcopy(ele)
            new_div.append(ele_clone)
            ele.set('append', 'yes')

        root.insert(id_, new_div)

    for id_, ele in enumerate(list(root)):           
        if ele.get('append') == 'yes':
            root.remove(ele)
    
    return root

### Lemmatisation/Conversion tagsets ##########################
def make_d_PRESTO(path_PRESTO):
    #création du dictionnaire python à partir du dictionnaire PRESTO
    PRESTO = open(path_PRESTO, encoding='utf-8')

    #parsing du fichier .dff et création du dictionnaire python
    d_PRESTO = {}
    for entry in tqdm(PRESTO):
        entry = entry.rstrip("\n")
        entry = entry.split("/")
        if entry[0] in d_PRESTO:
            # nouvelle valeur si l'entrée est déjà dans le dictionnaire python
            d_PRESTO[entry[0]].append(entry)
        else:
            # nouvelle entrée dans le dictionnaire python
            d_PRESTO[entry[0]] = [entry]
            
    PRESTO.close()

    return d_PRESTO

def make_d_CorrTable(path_CorrTable):
    #création du dictionnaire python à partir de la table de conversion
    CorrTable = open(path_CorrTable, encoding='utf-8')
    d_CorrTable = {}
    for i in CorrTable:
        i = i.split(",")
        if i[4] in d_CorrTable:
            d_CorrTable[i[4]].append(i)
        else:
            d_CorrTable[i[4]]=[i]
            
    CorrTable.close()

    return d_CorrTable


### Segmentation ##############################################


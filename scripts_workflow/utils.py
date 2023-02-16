import sys, getopt
import xml.etree.ElementTree as ET
import statistics
import copy

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
    for entry in PRESTO:
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
def extract_stats(cible):
    
    tree = ET.parse(open(cible, encoding='utf-8'))
    
    list_len = []
    nb_sent = 0
    
    for sent in tree.findall('.//s'):
        len_sent = 0
        nb_sent += 1
        for w in sent.findall('.//w'):
            len_sent += 1
        
        list_len.append(int(len_sent))
    
    try:
        len_sent_option_var = build_len_sent_option()
    except NameError:
        len_sent_option_var = None

    cnt_lg = 0
    list_len_lg = []
    for i in list_len:
        if len_sent_option_var==None:
            if i>80:
                list_len_lg.append(i)
                cnt_lg += 1
        else:
            if i>int(len_sent_option_var):
                list_len_lg.append(i)
                cnt_lg += 1
            
    print('Nb_phrases_longues: '+ str(cnt_lg)+' sur un total de '+str(nb_sent)+' phrases' )
    print("Après découpe au point-virgule dans les phrases trop longues: ")
    print("\tmoyenne du total: ", statistics.mean(list_len))
    print("\tmediane du total: ", statistics.median(list_len))
    print("\tmoyenne des phrases trop longues: ", statistics.mean(list_len_lg))
    print("\tmediane des phrases trop longues: ", statistics.median(list_len_lg))
    print("\tmax des phrases trop longues: ", sorted(list_len_lg)[len(list_len_lg)-1])

def extract_lg_sents(cible):
        
    tree = ET.parse(open(cible, encoding='utf-8'))
    
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
        
        try:
            len_sent_option_var = build_len_sent_option()
        except NameError:
            len_sent_option_var = None
        
        if len_sent_option_var==None:
            if len_sent > 80:
                x = str(nb_sent)+' \ len: '+str(len_sent)+' \ "too_long"'+'\n'+' '.join(text_sent)
                list_sents.append(x)
            else:
                x = str(nb_sent)+' \ len: '+str(len_sent)+'\n'+' '.join(text_sent)
                list_sents.append(x)
        else:
            if len_sent > len_sent_option_var:
                x = str(nb_sent)+' \ len: '+str(len_sent)+' \ "too_long"'+'\n'+' '.join(text_sent)
                list_sents.append(x)
            else:
                x = str(nb_sent)+' \ len: '+str(len_sent)+'\n'+' '.join(text_sent)
                list_sents.append(x)
        
            
    global cible_txt
    cible_txt = filedialog.asksaveasfilename(initialdir=dir_file,
                                         title="Select a File",
                                         filetypes=(("Text files",
                                                     "*.txt*"),
                                                    ("all files",
                                                     "*.*")))
    
    cible_txt = cible_txt.rstrip('.txt')+'.txt'
    
    with open(cible_txt, "w", encoding="utf-8") as out:
        for i in list_sents:
            out.write(i)
            out.write('\n')
            out.write('\n') 
    
    label_txt_file_downloaded.pack()


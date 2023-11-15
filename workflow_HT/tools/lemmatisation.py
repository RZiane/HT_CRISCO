import itertools, sys
from lxml import etree as ET
from utils import indent_xml, def_args, make_d_PRESTO, make_d_CorrTable, valid_xml, get_word_form, preprocess_word_form, renum_xml
from tqdm import tqdm

path_PRESTO = "/home/ziane212/projects/data/crisco/dico_PRESTO_SIMPLE_05.05.23.dff"
# path_PRESTO = "/home/ziane212/Téléchargements/1563_Guernesey_dict.dff"
path_CorrTable = "/home/ziane212/projects/data/crisco/MICLE_CorrTable_27-02-23.csv"
'''
path_PRESTO = "C:/Users/yagam/Desktop/crisco_ressources/dico_PRESTO_SIMPLE_05.05.23.dff"
path_CorrTable = "C:/Users/yagam/Desktop/crisco_ressources/MICLE_CorrTable_27-02-23.csv"
'''
def lemmatisation(entry, tag, list_prpos, list_prfeat, list_lemma):
    if entry[1] == tag[1]:
        if entry[1] in list_prpos:
            pass
        else:
            list_prpos.append(entry[1])

        if entry[2] in list_prfeat:
            pass
        else:
            list_prfeat.append(entry[2])

        for prfeat, prpos in zip(list_prfeat, itertools.cycle(list_prpos)):
            if entry[1] == prpos and entry[2] == prfeat:
                list_lemma.append(entry[3].lower())

def process_lemmatisation(inputfile, outputfile, d_CorrTable, d_PRESTO):
    tree = ET.parse(open(inputfile, encoding='utf-8'))
    root = tree.getroot()

    for w in tqdm(root.findall('.//w')):

        # lecture des tokens
        s_token = get_word_form(w)
        
        # edit token (lower pour eviter les majuscules en début de phrase, rstrip pour éviter les points agglutinés sur le token)
        s_token = preprocess_word_form(s_token)

        # edit lemme
        s_udpos = w.get('udpos')
                
        list_prpos = []
        list_prfeat = []
        list_lemma = []
        #dev print(s_token)
        #dev print(s_udpos)
        # test de matching dans le dictionnaire
        # if w.get('lemma')=='_':
        # w.set('presto', 'yes')
        if s_token in d_PRESTO.keys():
            # résolution de l'ambiguité en comparant l'étiquette POS UD avec celle dans le dictionnaire PRESTO
            if len(d_PRESTO[s_token]) != 1: # si plusieurs valeurs pour une entrée dans le dictionnaire alors ambiguité
                for entry in d_PRESTO[s_token]: # itération des valeurs pour l'entrée
                    for tag in d_CorrTable[s_udpos]:
                        lemmatisation(entry, tag, list_prpos, list_prfeat, list_lemma)

            else:
                for tag in d_CorrTable[s_udpos]:
                    lemmatisation(d_PRESTO[s_token][0], tag, list_prpos, list_prfeat, list_lemma)
        
        # absence du verbe dans presto
        else:
            w.attrib['NoMatchingPresto'] = 'Word'
        
        list_lemma = list(sorted(set(list_lemma)))
        
        if list_lemma != []:

            if len(list_lemma) > 1:
                s_lemma = '///'.join(list_lemma)
            else:
                s_lemma = list_lemma[0]

            # Gestion de l'absence de conversion de l'étiquette UPenn
            try:
                w.attrib['lemma'] = s_lemma
            except NameError:
                s_lemma = '_'
                w.attrib['lemma'] = s_lemma
        
        elif list_lemma == [] and w.get('NoMatchingPresto')!='Word':
            
            if s_udpos=='PROPN' or s_udpos=='PUNCT':
                s_lemma = w.text
                w.attrib['lemma'] = s_lemma
            else:
                s_lemma = '_'
                w.attrib['lemma'] = s_lemma

                w.attrib['NoMatchingPresto'] = 'POS'
                
        elif list_lemma == [] and w.get('NoMatchingPresto')=='Word':
            
            if s_udpos=='PROPN' or s_udpos=='PUNCT':
                s_lemma = s_token
                w.attrib['lemma'] = s_lemma
                w.attrib.pop('NoMatchingPresto')
            else:
                s_lemma = '_'
                w.attrib['lemma'] = s_lemma
        

        '''
        for i in range(len(list(root.findall('.//w')))+1):
            time.sleep(0.1)
            sys.stdout.write(('='*i)+(''*(len(list(root.findall('.//w')))-i))+("\r [ %d"%i+"% ] "))
            sys.stdout.flush()
        '''


    indent_xml(root)

    ET.ElementTree(root).write(outputfile, encoding="utf-8")


if __name__ == "__main__":
   inputfile, outputfile = def_args(sys.argv[1:])
   renum_xml(inputfile, inputfile)
    #    valid_xml(inputfile, "lemma")
   d_CorrTable = make_d_CorrTable(path_CorrTable)
   print("Processing dictionnary...")   
   d_PRESTO = make_d_PRESTO(path_PRESTO)
   print("Processing file...")
   process_lemmatisation(inputfile, outputfile, d_CorrTable, d_PRESTO)
   print("Done")
        

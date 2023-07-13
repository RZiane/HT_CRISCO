import itertools, sys
from lxml import etree as ET
from utils import indent_xml, def_args, make_d_PRESTO, make_d_CorrTable, valid_xml, get_word_form, preprocess_word_form
from tqdm import tqdm

'''
path_PRESTO = "/home/ziane212/crisco_work_ressources/dico_PRESTO_SIMPLE_10.01.23.dff"
path_CorrTable = "/home/ziane212/crisco_work_ressources/MICLE_CorrTable_13-02-23.csv"
'''

path_PRESTO = "/home/ziane212/projects/data/crisco/dico_PRESTO_SIMPLE_05.05.23.dff"
path_CorrTable = "/home/ziane212/projects/data/crisco/MICLE_CorrTable_27-02-23.csv"

# gestion des conversions Upenn particulières, éditions des listes de lemmes et definition d'une fonction qui regroupe toutes les conditions
l_Q = ['ASSEZ', 
          'AUCUN', 
          'AUTANT', 
          'AUTRETANT', 
          'BEAUCOUP', 
          'CHACUN', 
          'MAINT', 
          'MOULT', 
          'NELUI',
          'NESUN', 
          'NUL', 
          'PEU', 
          'PLUSIEURS', 
          'RIEN', 
          'TANT', 
          'TOUT', 
          'TRESOTOUT', 
          'TROP']

l_QR = ['MOINS', 'PLUS']

l_WH = ['COMME', 'COMMENT', 'POURQUOI', 'QUAND']

l_ADJR = ['MEILLEUR', 'MEILLEURE', 'MOINDRE', 'PIRE']

l_ADJZ = ['MIEN', 'TIEN', 'SIEN', 'NOTRE', 'VOTRE', 'LEUR']

l_ADJQ = ['MAINT', 'NUL', 'NESUN', 'TOUT', 'TRESOTOUT']

l_ADVQ = ['AUTANT', 'AUTRETANT', 'BEAUCOUP', 'TANT', 'TOUT', 'TRESOTOUT', 'TROP']

l_ADVR = ['MIEUX', 'PIRE']

l_DETQ = ['CHACUN', 'MAINT', 'MOULT', 'NUL', 'PLUSIEURS', 'TOUT']

l_PRONQ = ['CHACUN', 'NUL', 'NESUN' , 'PEU', 'PLUSIEURS', 'RIEN', 'TOUT']

l_MD = ['VOULOIR', 'DEVOIR', 'POUVOIR', 'SOULOIR', 'SAVOIR']

l_lemma_spec = [l_ADJQ, l_ADJR, l_ADJZ, l_ADVQ, l_ADVR, l_DETQ, l_PRONQ, l_QR, l_WH]

def ConvSpecUPenn(LEMMA, s_udpos, w):
    
    global upennpos

    if LEMMA in l_ADJQ and s_udpos == 'ADJ':
        w.attrib['uppos'] = 'Q'
    if LEMMA in l_ADJR and s_udpos == 'ADJ':
        w.attrib['uppos'] = 'ADJR'
    if LEMMA in l_ADJZ and s_udpos == 'ADJ':
        w.attrib['uppos'] = 'ADJZ'
    if LEMMA in l_ADVQ and s_udpos == 'ADV':
        w.attrib['uppos'] = 'Q'
    if LEMMA in l_ADVR and s_udpos == 'ADV':
        w.attrib['uppos'] = 'ADVR'
    if LEMMA in l_DETQ and s_udpos == 'DET':
        w.attrib['uppos'] = 'Q'
    if LEMMA in l_PRONQ and s_udpos == 'PRON':
        w.attrib['uppos'] = 'Q'
    if LEMMA in l_QR:
        w.attrib['uppos'] = 'QR'
    if LEMMA in l_WH:
        w.attrib['uppos'] = 'WH'
        
    if LEMMA.endswith('ISME') and i[3]=="ADJ":
        list_upennpos = 'ADJS'
    

def ConvSpecUPenn_VERB(LEMMA, XFEATS_PRESTO):
        
    global XPOS_UPenn
        
    if LEMMA == 'ÊTRE':
        if XFEATS_PRESTO == 'Vuc':
            XPOS_UPenn = 'EJ'
        elif XFEATS_PRESTO == 'Ga':
            XPOS_UPenn = 'EG'
        elif XFEATS_PRESTO == 'Vun':
            XPOS_UPenn = 'EX'
        elif XFEATS_PRESTO == 'Ge':
            XPOS_UPenn = 'EPP'
        
    elif LEMMA == 'AVOIR':
        if XFEATS_PRESTO == 'Vuc':
            XPOS_UPenn = 'AJ'
        elif XFEATS_PRESTO == 'Ga':
            XPOS_UPenn = 'AG'
        elif XFEATS_PRESTO == 'Vun':
            XPOS_UPenn = 'AX'
        elif XFEATS_PRESTO == 'Ge':
            XPOS_UPenn = 'APP'
    
    elif LEMMA != 'AVOIR' and LEMMA != 'ÊTRE':
        if LEMMA in l_MD:
            if XFEATS_PRESTO == 'Ga':
                XPOS_UPenn = 'MDG'
            elif XFEATS_PRESTO == 'Ge':
                XPOS_UPenn = 'MDPP'
            elif XFEATS_PRESTO == 'Vvn':
                XPOS_UPenn = 'MDX'
            elif XFEATS_PRESTO == 'Vvc':
                XPOS_UPenn = 'MDJ'
                
        elif XFEATS_PRESTO == 'Vvc':
            XPOS_UPenn = 'VJ'
        elif XFEATS_PRESTO == 'Vvn':
            XPOS_UPenn = 'VX'
        elif XFEATS_PRESTO == 'Ge':
            XPOS_UPenn = 'VPP'
        elif XFEATS_PRESTO == 'Ga':
            XPOS_UPenn = 'VG'
    
    if XFEATS_PRESTO == 'CHECK':
        XPOS_UPenn = 'CHECK'
    
    return XPOS_UPenn

def convTable(entry, tag, list_prpos, list_prfeat, list_upennpos, s_udpos, d_CorrTable):
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
            
            # UPenn conversion
            for key in d_CorrTable.values():
                for choice in key:
                    if s_udpos == choice[4] and prfeat == choice[2] and prpos == choice[1]:
                        if choice[3] in list_upennpos:
                            pass
                        else:
                            list_upennpos.append(choice[3])

def process_conversion(inputfile, outputfile, d_CorrTable, d_PRESTO):
    tree = ET.parse(open(inputfile, encoding='utf-8'))
    root = tree.getroot()

    for w in tqdm(root.findall('.//w')):
        #dev print(w.text)

        # lecture des tokens
        s_token = get_word_form(w)
        
        # edit token (lower pour eviter les majuscules en début de phrase, rstrip pour éviter les points agglutinés sur le token)
        s_token = preprocess_word_form(s_token)

        # edit lemme
        s_lemma = w.get('lemma')
        s_udpos = w.get('udpos')
                
        list_prpos = []
        list_prfeat = []
        list_upennpos = []
        
        s_lemma = s_lemma.upper()
        
        if s_udpos == 'VERB' or s_udpos == 'AUX':
            # test de matching dans le dictionnaire
            if s_token in d_PRESTO.keys():
                # résolution de l'ambiguité en comparant l'étiquette POS UD avec celle dans le dictionnaire PRESTO
                if len(d_PRESTO[s_token]) != 1: # si plusieurs valeurs pour une entrée dans le dictionnaire alors ambiguité
                    for entry in d_PRESTO[s_token]: # itération des valeurs pour l'entrée
                        if entry[3] == s_lemma:
                            for tag in d_CorrTable[s_udpos]:
                                if entry[1] == tag[1]:
                                    if entry[1] in list_prpos:
                                        pass
                                    else:
                                        list_prpos.append(entry[1])

                                    if entry[2] in list_prfeat:
                                        pass
                                    else:
                                        list_prfeat.append(entry[2])
                                        
                                    for prfeat in list_prfeat:
                                        if ConvSpecUPenn_VERB(s_lemma, prfeat) in list_upennpos:
                                            pass
                                        else:
                                            list_upennpos.append(ConvSpecUPenn_VERB(s_lemma, prfeat))
                                    
                if d_PRESTO[s_token][0][3] == s_lemma: # si une seule valeur pour l'entrée dans presto
                    for tag in d_CorrTable[s_udpos]:
                        if d_PRESTO[s_token][0][1] == tag[1]:

                            if d_PRESTO[s_token][0][1] in list_prpos:
                                pass
                            else:
                                list_prpos.append(d_PRESTO[s_token][0][1])
                            
                            if d_PRESTO[s_token][0][2] in list_prfeat:
                                pass
                            else:
                                list_prfeat.append(d_PRESTO[s_token][0][2])

                            for prfeat in list_prfeat:
                                if ConvSpecUPenn_VERB(s_lemma, prfeat) in list_upennpos:
                                    pass
                                else:
                                    list_upennpos.append(ConvSpecUPenn_VERB(s_lemma, prfeat))
            # absence du verbe dans presto
            else:
                w.attrib['NoMatchingPresto'] = 'Word'
        
        if s_udpos == 'DET' or s_udpos == 'PRON':
            # test de matching dans le dictionnaire
            if s_token in d_PRESTO.keys():
                # résolution de l'ambiguité en comparant l'étiquette POS UD avec celle dans le dictionnaire PRESTO
                if len(d_PRESTO[s_token]) != 1: # si plusieurs valeurs pour une entrée dans le dictionnaire alors ambiguité
                    for entry in d_PRESTO[s_token]: # itération des valeurs pour l'entrée
                        if entry[3] == s_lemma:
                            for tag in d_CorrTable[s_udpos]:
                                convTable(entry, tag, list_prpos, list_prfeat, list_upennpos, s_udpos, d_CorrTable)
                                                    
                if d_PRESTO[s_token][0][3] == s_lemma: # si une seule valeur pour l'entrée dans presto
                    for tag in d_CorrTable[s_udpos]:
                        convTable(d_PRESTO[s_token][0], tag, list_prpos, list_prfeat, list_upennpos, s_udpos, d_CorrTable)

            # absence du verbe dans presto
            else:
                w.attrib['NoMatchingPresto'] = 'Word'

        if list_prpos != [] and list_prfeat != [] and list_upennpos != []:
            if len(list_prpos) > 1:
                XPOS_PRESTO = '///'.join(list_prpos)
            else:
                XPOS_PRESTO = list_prpos[0]

            if len(list_prfeat) > 1:
                XFEATS_PRESTO = '///'.join(list_prfeat)
            else:
                XFEATS_PRESTO = list_prfeat[0]

            if len(list_upennpos) > 1:
                XPOS_UPENN = '///'.join(list_upennpos)
            else:
                XPOS_UPENN = list_upennpos[0]
            
            # Gestion de l'absence de conversion de l'étiquette UPenn
            try:
                w.attrib['uppos'] = XPOS_UPENN
            except NameError:
                XPOS_UPENN = '_'
                w.attrib['uppos'] = XPOS_UPENN
            del XPOS_UPENN

            #w.attrib['pr'] = XPOS_PRESTO
            w.attrib['prpos'] = XFEATS_PRESTO
            del XPOS_PRESTO
            del XFEATS_PRESTO
            
        else:
            if s_udpos=='ADJ':
                w.attrib['uppos'] = 'ADJ'
                #w.attrib['pr'] = 'ADJ'
                w.attrib['prpos'] = 'Ag'

            if s_udpos=='ADP':
                if w.attrib['lemma'] == 'à+le' or w.attrib['lemma'] == 'de+le':
                    #w.attrib['pr'] = 'PREP'
                    w.attrib['prpos'] = 'S+Da'
                else:
                    #w.attrib['pr'] = 'PREP'
                    w.attrib['prpos'] = 'S'
                w.attrib['uppos'] = 'P'

            if s_udpos=='ADV':
                w.attrib['uppos'] = 'ADV'
                #w.attrib['pr'] = 'ADV'
                w.attrib['prpos'] = 'Rg'

            if s_udpos=='NOUN':
                w.attrib['uppos'] = 'NCS'
                #w.attrib['pr'] = 'NOM'
                w.attrib['prpos'] = 'Nc'

            if s_udpos=='PROPN':
                w.attrib['uppos'] = 'NPRS'
                #w.attrib['pr'] = 'NOMP'
                w.attrib['prpos'] = 'Np'

            if s_udpos=='SCONJ':
                w.attrib['uppos'] = 'CONJS'
                #w.attrib['pr'] = 'CON'
                w.attrib['prpos'] = 'Cs'

            if s_udpos=='CCONJ':
                w.attrib['uppos'] = 'CONJO'
                #w.attrib['pr'] = 'CON'
                w.attrib['prpos'] = 'Cc'

            if s_udpos=='NUM':
                w.attrib['uppos'] = 'NUM'
                #w.attrib['pr'] = 'NUM'
                w.attrib['prpos'] = 'Mc'
            
            if s_udpos=='PUNCT':
                w.attrib['uppos'] = 'PON'
                #w.attrib['pr'] = 'NUM'
                w.attrib['prpos'] = 'Fw'

            if s_udpos != 'PUNCT' and w.get('uppos') == None and w.get('prpos') == None and w.get('NoMatchingPresto') == None:
                w.attrib['NoMatchingPresto'] = 'POS'
        
        if w.get('uppos') == None:
            w.attrib['uppos'] = '_'
            
        if w.get('prpos') == None:
            w.attrib['prpos'] = '_'

        if s_udpos == 'PUNCT':
            w.attrib['lemma'] = w.text
        
        for l in l_lemma_spec:
            if s_lemma in l:
                ConvSpecUPenn(s_lemma, s_udpos, w)
                
    indent_xml(root)

    ET.ElementTree(root).write(outputfile, encoding="utf-8")


if __name__ == "__main__":
   inputfile, outputfile = def_args(sys.argv[1:])
   # global d_CorrTable
   valid_xml(inputfile, "convTags")
   d_CorrTable = make_d_CorrTable(path_CorrTable)
   print("Processing dictionnary...")
   d_PRESTO = make_d_PRESTO(path_PRESTO)
   print("Processing file...")
   #renum_xml(inputfile, inputfile)
   process_conversion(inputfile, outputfile, d_CorrTable, d_PRESTO)

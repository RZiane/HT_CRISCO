import sys, getopt, copy, re, os
from lxml import etree as ET
from tqdm import tqdm

ns_map = {'tei': 'http://www.tei-c.org/ns/1.0'}

def def_args(argv):
   inputfile = ''
   outputfile = ''
   opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile=","tfile="])
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

def traverse_dir(repertoire):
    for racine, dossiers, fichiers in os.walk(repertoire):
        for fichier in fichiers:
            if fichier.endswith(".xml"):
                chemin_fichier = os.path.join(racine, fichier)
                yield chemin_fichier

### XML processing ##############################################
def reorderAttrib(root):
    for word in root.findall('.//w'):

        if word.get('join')!=None:
            word.attrib['join'] = word.attrib.pop('join')

        if word.get('n')!=None:
            word.attrib['n'] = word.attrib.pop('n')

        if word.get('head')!=None:
            word.attrib['head'] = word.attrib.pop('head')

        if word.get('function')!=None:
            word.attrib['function'] = word.attrib.pop('function')

        if word.get('lemma')!=None:
            word.attrib['lemma'] = word.attrib.pop('lemma')

        if word.get('udpos')!=None:
            word.attrib['udpos'] = word.attrib.pop('udpos')

        if word.get('prpos')!=None:
            word.attrib['prpos'] = word.attrib.pop('prpos')

        if word.get('uppos')!=None:
            word.attrib['uppos'] = word.attrib.pop('uppos')

        if word.get('retagging')!=None:
            word.attrib['retagging'] = word.attrib.pop('retagging')

        if word.get('NoMatchingPresto')!=None:
            word.attrib['NoMatchingPresto'] = word.attrib.pop('NoMatchingPresto')

        if word.get('ambiguite')!=None:
            word.attrib['ambiguite'] = word.attrib.pop('ambiguite')

        if word.get('fiabilite')!=None:
            word.attrib['fiabilite'] = word.attrib.pop('fiabilite')
        
        if word.get('convNoMatching')!=None:
            word.attrib['convNoMatching'] = word.attrib.pop('convNoMatching')
        
        if word.get('annot_PL')!=None:
            word.attrib['annot_PL'] = word.attrib.pop('annot_PL')
        


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

def drop_head(inputfile, outputfile):

    tree = ET.parse(open(inputfile, encoding="utf-8"))
    root = tree.getroot()

    for token in tree.findall('.//w'):
        token.set('head', '0')

    indent_xml(root)

    reorderAttrib(root)

    ET.ElementTree(root).write(outputfile, encoding="utf-8")

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

def get_word_form(w):
    # lecture des tokens
    if w.tag == 'w':
        if len(list(w))!=0:
            if list(w)[0].tag == 'choice':
                s_token = list(w)[0][1].text
            else:
                s_token = ''
                for child in w.iter():
                    if child.text:
                        s_token += child.text
                    if child.tail:
                        s_token += child.tail
        else:
            s_token = w.text
    
        s_token = s_token.replace('\t', '').replace('\n', '')

        return s_token
    
    else:
        pass

def format_tag_text(root):
    for w in root.findall(".//w"):
        if len(list(w))!=0:
            if list(w)[0].tag == 'choice':
                list(w)[0][1].text = list(w)[0][1].text.replace('\t', '').replace('\n', '').rstrip(' ').lstrip(' ')
                list(w)[0][0].text = list(w)[0][0].text.replace('\t', '').replace('\n', '').rstrip(' ').lstrip(' ')
            else:
                for child in w.iter():
                    if child.text:
                        child.text = child.text.replace('\t', '').replace('\n', '').rstrip(' ').lstrip(' ')
                    if child.tail:
                        child.tail = child.tail.replace('\t', '').replace('\n', '').rstrip(' ').lstrip(' ')
        else:
            try:
                w.text = w.text.replace('\t', '').replace('\n', '').rstrip(' ').lstrip(' ')
                w.tail = w.tail.replace('\t', '').replace('\n', '').rstrip(' ').lstrip(' ')
            except AttributeError:
                pass
        
def preprocess_word_form(s_token):
    l_replace = [('[', ''), ('(', ''), 
                    (']', ''), (')', ''), 
                    ('\t', ''), ('\n', ''), 
                    ('"', ''), ('«', ''), 
                    ('»', '')]
        
    for r in l_replace:
        s_token = s_token.replace(*r)
    
    s_token = s_token.rstrip('-')

    if s_token.endswith('.') and len(s_token)!=1:
        s_token = s_token.replace('.', '')
    
    s_token = s_token.lower()

    return s_token

def actu_list(list_, var):
        find = False

        for i, tpl in enumerate(list_):
            if tpl[0] == var:
                list_[i] = [tpl[0], tpl[1] + 1]
                find = True
                break

        if not find:
            list_.append([var, 1])

def make_table_from_xml(inputfile, outputfile):

    UPOS_select = input("Add UPOS to table (y or n): ") 
    UPENN_POS_select = input("Add UPENN_POS to table (y or n): ")
    PRESTO_POS_select = input("Add PRESTO_POS to table (y or n): ")
    lemma_select = input("Add lemma to table (y or n): ")
    function_select = input("Add function to table (y or n): ")

    tree = ET.parse(open(inputfile, encoding="utf-8"))
    root = tree.getroot()

    list_ = []
    list_.append(['', 0])

    for id_, token in enumerate(root.findall('.//w')):
        
        #dev print(token.text)
        form = get_word_form(token)
        
        try:
            UPOS = token.get('udpos')
        except:
            UPOS = "_"
        
        try:
            UPENN_POS = token.get('uppos')
        except:
            UPENN_POS = "_"
        
        try:
            PRESTO_POS = token.get('prpos')
        except:
            PRESTO_POS = "_"
        
        try:
            lemma = token.get('lemma')
        except:
            lemma = "_"
        
        try:
            lemma_AND = token.get('lemma_AND')
        except:
            lemma_AND = "_"
            
        try:
            lemma_src = token.get('lemma_src')
        except:
            lemma_src = "_"
        
        try:
            function = token.get('function')
        except:
            function = "_"
        
        ele = [form]
        if UPOS_select == 'y':
            ele.append(UPOS)
        if UPENN_POS_select == 'y':
            ele.append(UPENN_POS)
        if PRESTO_POS_select == 'y':
            ele.append(PRESTO_POS)
        if lemma_select == 'y':
            ele.append(lemma)
        if function_select == 'y':
            ele.append(function)

        actu_list(list_, '\t'.join(ele))

    for i in list_:
        if i[1]==0:
            list_.remove(i)
    
    print(list_)
    for id_, i in enumerate(list_):
        i[1] = str(i[1])
        list_[id_] = '\t'.join(i)
    list_ = list(sorted(set(list_)))       

    with open(outputfile, "w", encoding='utf-8') as file:
        for i in list_:
            file.write(i.rstrip('\n')+'\n')

def renum_xml(inputfile, outputfile):
    
    """
    Fonction permettant de lire un fichier XML-TEI pour cibler les
    éléments hiérarchiques div type="book", type="chapter", div type="section", p, s et w et leur ajouter un @n unique, 
    numéroté à partir de 1 et se réinitilisant après la fermeture de l'élément parent.
    Si on souhaite utiliser des entités, elles sont résolues dans le
    fichier de sortie, mieux vaut donc les installer ensuite.
    
    :param chemin_entree: Le chemin local du fichier XML-TEI tokenisé
        aux éléments duquel on souhaite ajouter des numéros.
    :param chemin_sortie: Le chemin local auquel on souhaite écrire le
        fichier XML-TEI de sortie avec ses @n ajoutés.
        
    En l'absence de namesplace, on travaille uniquement en-dehors du TEI.
    
    """
    
    # On importe le XML-TEI d'entrée et on le lit.
    tree = ET.parse(open(inputfile, encoding="utf-8"))
    root = tree.getroot()
    
    # On donne au module XML le namespace de la TEI, sans préfixe car ce sera le seul.
    #ET.register_namespace('', "http://www.tei-c.org/ns/1.0")    
    
    #On crée un compteur pour les numéros de book
    
    # On crée un compteur pour les numéros de chapter
    for counter_book, book in enumerate(root.findall(".//div[@type='book']"), 1):
        if book.get('n'):
            del book.attrib['n']
        book.set('n', str(counter_book))
    
        # On crée un compteur pour les numéros de chapter
        for counter_chapter, chapter in enumerate(book.findall(".//div[@type='chapter']"), 1):
            if chapter.get('n'):
                del chapter.attrib['n']
            chapter.set('n', str(counter_chapter))

        #On boucle sur les éléments <div type="section"> dans l'ordre du fichier, pour chaque chapter.
        # On crée un compteur pour les numéros de section
        #counter_section = 0

            for counter_section, section in enumerate(chapter.findall(".//div[@type='section']"), 1):
                if section.get('n'):
                    del section.attrib['n']
                if section.get('nb'):
                    del section.attrib['nb']
                section.set('n', str(counter_section))

        #On boucle sur les éléments <p> dans l'ordre du fichier

        # On crée un compteur pour les numéros de paragraphe.
        #counter_para = 0

                for counter_para, para in enumerate(section.findall(".//p"), 1):
                    if para.get('n'):
                        del para.attrib['n']
                    para.set('n', str(counter_para))


        #On boucle sur les éléments <s> dans l'ordre du fichier.
        # On crée un compteur pour les numéros de phrase.
        #counter_sentence = 0

                    for counter_sentence, sentence in enumerate(para.findall(".//s"), 1):
                        if sentence.get('n'):
                            del sentence.attrib['n']
                        sentence.set('n', str(counter_sentence))

                        # On boucle sur les éléments <w> dans l'ordre du fichier.
                        # On crée un compteur pour les numéros des tokens.
                        #counter_word = 0

                        for counter_word, word in enumerate(sentence.findall(".//w"), 1):
                            if word.get('n'):
                                del word.attrib['n']
                            word.set('n', str(counter_word))

                        for counter_nullw, nullw in enumerate(sentence.findall(".//nullw"), 1):
                            if nullw.get('n'):
                                del nullw.attrib['n']
                            if nullw.get('nulln'):
                                del nullw.attrib['nulln']
                            nullw.set('nulln', str(counter_nullw))

    # On écrit le TEI obtenu dans le fichier spécifié en second paramètre.
    tree.write(outputfile, xml_declaration=False, encoding="utf-8")
    tree = ET.parse(open(outputfile, encoding='utf-8'))
    root = tree.getroot()
    indent_xml(root)
    reorderAttrib(root)
    ET.ElementTree(root).write(outputfile, encoding="utf-8")

def make_coherence_table(path_corrTable):
    CorrTable = open(path_corrTable, encoding='utf-8')
    l = []
    for i in CorrTable:
        i = i.split(",")
        l.append((i[2], i[3], i[4]))

    l.append(('','_', '_'))
    l.append((None,None,None))

    CorrTable.close()

    return l

def check_coherence(l, prpos, uppos, udpos):
    
    global incoherence
    incoherence = False
    
    if udpos == 'PUNCT' or udpos == 'PROPN':
        pass
    elif (prpos, uppos, udpos) not in l:
        if udpos == 'VERB':
            if (prpos, uppos, 'AUX') not in l:
                incoherence = True
        elif udpos == 'AUX':
            if (prpos, uppos, 'VERB') not in l:
                incoherence = True
        else:
            incoherence = True
    
    return incoherence

def valid_xml(inputfile):

    UPOS_select = input("UPOS validation ? (y or n): ") 
    UPENN_POS_select = input("UPENN_POS validation ? (y or n): ")
    PRESTO_POS_select = input("PRESTO_POS validation ? (y or n): ")
    lemma_select = input("Lemma validation ? (y or n): ")
    coherence_select = input("POS tagsets coherence checking ? (y or n): ")

    tree = ET.parse(open(inputfile, encoding='utf-8'))
    root = tree.getroot()
    format_tag_text(root)
    indent_xml(root)
    reorderAttrib(root)
    ET.ElementTree(root).write(inputfile, encoding="utf-8")

    l_upos = ["ADJ","ADP","PUNCT","ADV",
             "AUX","SYM","INTJ","CCONJ",
             "X","NOUN","DET","PROPN",
             "NUM","VERB","PART","PRON",
             "SCONJ"]
    
    l_upenn = ["ADJ", "ADJNUM", "ADJR", "ADJS",
               "ADJZ", "ADV", "ADVNEG", "ADVR",
               "ADVS", "CONJO", "CONJS", "D",
               "DZ", "PON", "PONFP", "ITJ", 
               "NEG", "NUM", "NCS", "NCPL", 
               "NPRS", "NPRPL", "PRO", "Q",
               "QR", "QS", "AG", "AJ",
               "APP", "AX", "EG", "EJ",
               "EPP", "EX", "MDG", "MDJ",
               "MDPP", "MDX", "VG", "VJ",
               "VPP", "VX", "WADV", "WD", "WPRO", 'P', 'WH']
    
    l_prpos = ["Ag", "As", "Mc", "Mo", "Rg", "Rp", "Ga", "Ge",
               "Vvc", "Vuc", "Vvn", "Vun", "Pp", "Pr", "Pd", "Pi", 
               "Ps", "Pt", "S", "Cs", "Cc", "Da", "Di", "Dn",
               "Ds", "S+Da", "Nc", "Np", "Rp", "Fw", "Fs", "Fo",
               "Rt", "Dt", "Dr", "Xa", "Xe", "INT", "Dd", "S+Di", "Dp", "S+Pr", "S+Dn"]
    
    path_CorrTable = 'ressources/MICLE_CorrTable_coherence_26.10.23.csv'

    list_coherence = make_coherence_table(path_CorrTable)

    error_cnt = 0
    with open(inputfile) as f:
        lines = list(f)

    # for id_, line in enumerate(lines):
    #     line = line.replace('\t', '').replace('\n', '')
    #     if line.startswith('<w'):
    #         if line.endswith('/>'):
    #             print('\n'+'Empty token in the line: '+str(id_+1))
    #             print(line)
    #             error_cnt += 1
    #         elif '><' in line:
    #             print('\n'+'Empty token in the line: '+str(id_+1))
    #             print(line)
    #             error_cnt += 1
    #         elif not line.endswith('/w>'):
    #             lines[id_+1] = lines[id_+1].replace('\t', '').replace('\n', '')
    #             lines[id_+2] = lines[id_+2].replace('\t', '').replace('\n', '')
    #             lines[id_+3] = lines[id_+3].replace('\t', '').replace('\n', '')
    #             lines[id_+4] = lines[id_+4].replace('\t', '').replace('\n', '')
    #             lines[id_+5] = lines[id_+5].replace('\t', '').replace('\n', '')
    #             if id_+1 < len(lines) and id_+2 < len(lines) and id_+3 < len(lines) and id_+4 < len(lines) and id_+5 < len(lines):
    #                 if lines[id_+1].startswith('<hi') and lines[id_+2].endswith('</w>'):
    #                     pass
    #                 elif lines[id_+1].startswith('<choice') and lines[id_+2].startswith('<sic') and lines[id_+3].startswith('<corr') and lines[id_+5].endswith('</w>'):
    #                     pass
    #                 elif lines[id_+1].startswith('<foreign') and lines[id_+2].endswith('</w>'):
    #                     pass
    #                 elif lines[id_+1].startswith('<foreign') and lines[id_+2].startswith('<hi') and lines[id_+4].endswith('</w>'):
    #                     pass
    #                 else:
    #                     print('\n'+'Empty token in the line: '+str(id_+1))
    #                     print(line)
    #                     error_cnt += 1

    # if error_cnt !=0:
    #     sys.exit('\n'+"Error in XML file, see comment above.")
    
    if UPOS_select == "y":
        error_cnt = 0
        with open(inputfile) as f:
            for id_, line in enumerate(f):
                line = line.lstrip('\t')
                if line.startswith('<w'):

                    s_udpos_content = re.findall('udpos=\"([^\"]*)\"', line)
                        
                    if s_udpos_content==[]:
                        print('No udpos attribut inside the line: '+str(id_+1))
                        print(line)
                        # temp_error.append('\n'.join(['No udpos attribut inside the line: '+str(id_+1), line]))
                        error_cnt += 1
                    try:
                        if s_udpos_content[0] in l_upos:
                            pass 
                        else:
                            print('Error in the UPOS class inside line: '+str(id_+1))
                            print(line)
                            error_cnt +=1
                    except:
                        pass

        if error_cnt !=0:
            sys.exit("Error in XML file, see comment above.")

    if UPENN_POS_select == "y":
        error_cnt = 0
        with open(inputfile) as f:
            for id_, line in enumerate(f):
                line = line.lstrip('\t')
                if line.startswith('<w'):

                    s_uppos_content = re.findall('uppos=\"([^\"]*)\"', line)

                    if s_uppos_content==[]:
                        print('No uppos attribut inside the line: '+str(id_+1))
                        print(line)
                        error_cnt += 1
                    try:
                        if s_uppos_content[0] in l_upenn:
                            pass 
                        else:
                            print('Error in the UPPOS class inside line: '+str(id_+1))
                            print(line)
                            error_cnt +=1
                    except:
                        pass

        if error_cnt !=0:
            sys.exit("Error in XML file, see comment above.")

    if PRESTO_POS_select == "y":
        error_cnt = 0
        with open(inputfile) as f:
            for id_, line in enumerate(f):
                line = line.lstrip('\t')
                if line.startswith('<w'):

                    s_prpos_content = re.findall('prpos=\"([^\"]*)\"', line)

                    if s_prpos_content==[]:
                        print('No prpos attribut inside the line: '+str(id_+1))
                        print(line)
                        error_cnt += 1
                    try:
                        if s_prpos_content[0] in l_prpos:
                            pass 
                        else:
                            print('Error in the PRPOS class inside line: '+str(id_+1))
                            print(line)
                            error_cnt +=1
                    except:
                        pass
            
        if error_cnt !=0:
            sys.exit("Error in XML file, see comment above.")

    if coherence_select == "y":

        error_cnt = 0
        with open(inputfile) as f:
            for id_, line in enumerate(f):
                line = line.lstrip('\t')
                if line.startswith('<w'):

                    s_udpos_content = re.findall('udpos=\"([^\"]*)\"', line)
                    s_prpos_content = re.findall('prpos=\"([^\"]*)\"', line)
                    s_uppos_content = re.findall('uppos=\"([^\"]*)\"', line)

                    incoherence = check_coherence(list_coherence, s_prpos_content[0], s_uppos_content[0], s_udpos_content[0])
                    if incoherence == True:
                        print('POS incoherence inside the line: '+str(id_+1))
                        print(line)
                        # incoherence_error.append('\n'.join(['POS incoherence inside the line: '+str(id_+1), line]))
                        error_cnt += 1

        if error_cnt !=0:
            sys.exit("Error in XML file, see comment above.")
    
    if lemma_select == "y":
        error_cnt = 0
        with open(inputfile) as f:
            for id_, line in enumerate(f):
                line = line.lstrip('\t')
                if line.startswith('<w'):

                    s_lemma_content = re.findall('lemma=\"([^\"]*)\"', line)
                    
                    if s_lemma_content==[]:
                        print('No lemma attribut inside the line: '+str(id_+1))
                        print(line)
                        error_cnt += 1
                    try:
                        if s_lemma_content[0] != "_" and s_lemma_content[0] != "":
                            pass
                        elif s_lemma_content[0] == "_":
                            print('Please check lemma attribut inside line: '+str(id_+1))
                            print(line)
                        elif s_lemma_content[0] == "":
                            print('Empty lemma attribut inside line: '+str(id_+1))
                            print(line)
                            error_cnt +=1
                    except:
                        pass

        if error_cnt !=0:
            sys.exit("Error in XML file, see comment above.")
    
    print("The file is valid")

def conversion_xml2conllu_group(inputfile, outputfile):
    
    # On importe le XML-TEI d'entrée et on le lit.
    tree = ET.parse(open(inputfile, encoding="utf-8"))
    root = tree.getroot()

    for group in root.findall('.//group'):
        group_id = group.get('n')

        outputfile_temp = outputfile.rstrip('.conllu')+'_'+group_id+'.conllu'

        # On ouvre le fichier de sortie
        with open(outputfile_temp, 'w', encoding="utf-8") as conll:

            for sentence in group.findall('.//s'):
                sent_id = sentence.get('sent_id')
                sent_len = sentence.get('len')
            
                conll.write('\n'+'# sent_id = '+ sent_id+'\n')
                conll.write('# sent_len = '+ sent_len+'\n')
                conll.write('# group = '+ group_id+'\n')

                for word in sentence:

                    if word.tag == 'w':
                        #On récupère les numéros de tokens
                        word_nb = word.get('n')                                                             

                        #On récupère les lemmes ; sinon, on laisse vide.

                        try:
                            dictlemma = {"lemma": word.get('lemma')}
                        except:
                            dictlemma = {"lemma": "_"}
                        if str(dictlemma["lemma"]) == "None":
                            lemma = "_"
                        else:    
                            lemma = str(dictlemma["lemma"])

                        #On récupère les udpos ; sinon, on laisse vide.

                        try:
                            dictudpos = {"udpos": word.get('udpos')}
                        except:
                            dictudpos = {"udpos": "_"}
                        if str(dictudpos["udpos"]) == "None":
                            udpos = "_"
                        else:    
                            udpos = str(dictudpos["udpos"])

                        #On récupère les uppos ; sinon, on laisse vide.

                        try:
                            dictuppos = {"uppos": word.get('uppos')}
                        except:
                            dictuppos = {"uppos": "_"}
                        if str(dictuppos["uppos"]) == "None":
                            uppos = "_"
                        else:    
                            uppos = str(dictuppos["uppos"])   

                        #On récupère les head ; sinon, on laisse vide.

                        try:
                            dicthead = {"head": word.get('head')}
                        except:
                            dicthead = {"head": "_"}
                        if str(dicthead["head"]) == "None":
                            head = "_"
                        else:    
                            head = str(dicthead["head"])

                        #On récupère les function ; sinon, on laisse vide.

                        try:
                            dictfunction = {"function": word.get('function')}
                        except:
                            dictfunction = {"function": "_"}
                        if str(dictfunction["function"]) == "None":
                            function = "_"
                        else:    
                            function = str(dictfunction["function"])

                        #On récupère les prpos ; sinon, on laisse vide.

                        try:
                            dictprpos = {"prpos": word.get('prpos')}
                        except:
                            dictprpos = {"prpos": "_"}
                        if str(dictprpos["prpos"]) == "None":
                            prpos = "_"
                        else:    
                            prpos = str(dictprpos["prpos"]).rstrip('\n')

                        #On récupère les join ; sinon, on laisse vide.

                        try:
                            dictjoin = {"join": word.get('join')}
                        except:
                            dictjoin = {"join": "_"}
                        if str(dictjoin["join"]) == "None":
                            join = "_"
                        else:    
                            join = str(dictjoin["join"]).rstrip('\n')

                        #On récupère le mot-forme. S'il y a des enfants, on concatène.

                        form = get_word_form(word)
                        #dev print(form)
                        mot = word_nb+"\t"+form.replace("\t", "").replace("\n", "")+"\t"+lemma+"\t"+udpos+"\t"+uppos+"\t_\t"+head+"\t"+function+"\t_\tjoin="+join+"|prpos="+prpos+"\n"          

                        strmot = str(mot)

                        #On écrit le fichier de sortie

                        conll.write(strmot)


def conversion_xml2conllu(inputfile, outputfile):
    # On ouvre le fichier de sortie
    with open(outputfile, 'w', encoding="utf-8") as conll:

    # On importe le XML-TEI d'entrée et on le lit.
        tree = ET.parse(open(inputfile, encoding="utf-8"))
        root = tree.getroot()

        # On donne au module XML le namespace de la TEI, sans préfixe car ce sera le seul.
        #ET.register_namespace('', "http://www.tei-c.org/ns/1.0")    

        #On boucle sur les balises w, en reprenant la hiérarchie, et on met en forme conll avec les balises
        # On crée un compteur pour les numéros de book
        for book in root.findall('.//div[@type="book"]'):
            book_nb = book.get('n')
            book_ch = int(book_nb)

            # On cible les chapter, et on récupère l'attribut n

            for chapter in book.findall('.//div[@type="chapter"]'):
                chapter_nb = chapter.get('n')
                chapter_ch = int(chapter_nb)

                    # On cible les sections, et on récupère l'attribut n

                for section in chapter.findall('.//div[@type="section"]'):
                    section_nb = section.get('n')
                    section_ch = int(section_nb)

                        #On cible les paragraphes, et on récupère l'attribut n

                    for para in section.findall('.//p'):
                        para_nb = para.get('n')
                        para_ch = int(para_nb)

                                #On cible les sentences, on récupère l'attribut n et on écrit l'identifiant de phrase.

                        for sentence in para.findall('.//s'):
                            sentence_nb = sentence.get('n')
                            sentence_ch = int(sentence_nb)

                            if book_ch == chapter_ch == section_ch == para_ch == sentence_ch == 1:
                                balise_sent = '# sent_id = '+book_nb+'-'+chapter_nb+'-'+section_nb+'-'+para_nb+'-'+sentence_nb+'\n'

                            else:
                                balise_sent = '\n# sent_id = '+book_nb+'-'+chapter_nb+'-'+section_nb+'-'+para_nb+'-'+sentence_nb+'\n'

                            conll.write(balise_sent)

                                    # On boucle sur les w. Si l'élément a des enfants, leur contenu est concaténé l'un à la suite des autres.

                            for word in sentence.findall('.//w'):

                                #On récupère les numéros de tokens
                                word_nb = word.get('n')                                                             
                                word_ch = int(word_nb)

                                #On récupère les lemmes ; sinon, on laisse vide.

                                try:
                                    dictlemma = {"lemma": word.get('lemma')}
                                except:
                                    dictlemma = {"lemma": "_"}
                                if str(dictlemma["lemma"]) == "None":
                                    lemma = "_"
                                else:    
                                    lemma = str(dictlemma["lemma"])

                                #On récupère les udpos ; sinon, on laisse vide.

                                try:
                                    dictudpos = {"udpos": word.get('udpos')}
                                except:
                                    dictudpos = {"udpos": "_"}
                                if str(dictudpos["udpos"]) == "None":
                                    udpos = "_"
                                else:    
                                    udpos = str(dictudpos["udpos"])

                                #On récupère les uppos ; sinon, on laisse vide.

                                try:
                                    dictuppos = {"uppos": word.get('uppos')}
                                except:
                                    dictuppos = {"uppos": "_"}
                                if str(dictuppos["uppos"]) == "None":
                                    uppos = "_"
                                else:    
                                    uppos = str(dictuppos["uppos"])   

                                #On récupère les head ; sinon, on laisse vide.

                                try:
                                    dicthead = {"head": word.get('head')}
                                except:
                                    dicthead = {"head": "_"}
                                if str(dicthead["head"]) == "None":
                                    head = "_"
                                else:    
                                    head = str(dicthead["head"])

                                #On récupère les function ; sinon, on laisse vide.

                                try:
                                    dictfunction = {"function": word.get('function')}
                                except:
                                    dictfunction = {"function": "_"}
                                if str(dictfunction["function"]) == "None":
                                    function = "_"
                                else:    
                                    function = str(dictfunction["function"])

                                #On récupère les prpos ; sinon, on laisse vide.

                                try:
                                    dictprpos = {"prpos": word.get('prpos')}
                                except:
                                    dictprpos = {"prpos": "_"}
                                if str(dictprpos["prpos"]) == "None":
                                    prpos = "_"
                                else:    
                                    prpos = str(dictprpos["prpos"]).rstrip('\n')

                                #On récupère les join ; sinon, on laisse vide.

                                try:
                                    dictjoin = {"join": word.get('join')}
                                except:
                                    dictjoin = {"join": "_"}
                                if str(dictjoin["join"]) == "None":
                                    join = "_"
                                else:    
                                    join = str(dictjoin["join"]).rstrip('\n')

                                #On récupère le mot-forme. S'il y a des enfants, on concatène.

                                form = get_word_form(word)
                                #dev print(form)
                                mot = word_nb+"\t"+form.replace("\t", "").replace("\n", "")+"\t"+lemma+"\t"+udpos+"\t"+uppos+"\t_\t"+head+"\t"+function+"\t_\tjoin="+join+"|prpos="+prpos+"\n"          

                                strmot = str(mot)

                                #On écrit le fichier de sortie

                                conll.write(strmot)

def conversion_conllu2xml(inputfile, outputfile):
    #on ouvre le fichier d'origine, et on construit une liste où chaque élément est une ligne du conll.

    conll = open(inputfile, encoding='utf-8')
    corpus = []
    for line in conll:
        corpus.append(line)
    
    #On parse le fichier conll en entrée, et on stocke les informations dans des variables

    sentence = {}
    words = []
    sentence_str = ""
        
    for line in corpus:
            
            #Si la ligne est un commentaire, il contient le X-PATH de la phrase. On récupère les infos.
            
        if line.startswith('#') == True:
            if 'sent_id' in line:
                if len(sentence.keys()) != 0:
                    sentence = {}
                print(line)
                sentence_str = re.search("\d+-\d+-\d+-\d+-\d+", line).group()
                num2 = sentence_str.split('-')
                '''
                sentence_str = re.search("\d+_\d+_\d+_\d+_\d+", line).group()
                num2 = sentence_str.split('_')
                '''
                sentence['book'] = num2[0]
                sentence['chapter'] = num2[1]
                sentence['section'] = num2[2]
                sentence['para'] = num2[3]
                sentence['sent'] = num2[4]

            #Si la ligne est vide, on passe.
            
        elif line.startswith('\n') == True:
            pass
        
            #Sinon, la ligne est un token. On récupère les informations de colonnes.
            
        else:
            
            info_token = line.split('\t')
            '''
            info_token[9] = info_token[9].rstrip('\n')
            misc_temp = info_token[9].split('|')
            misc = {}
            print(info_token[9])
            for id_, j in enumerate(misc_temp):
                misc_temp[id_] = misc_temp[id_].split('=')
                misc[misc_temp[id_][0].replace(' ', '')] = misc_temp[id_][1].replace(' ', '')
            
            if 'rend' in misc.keys():
                pass
            else:
                misc['rend'] = '_'
                            
            if 'prpos' in misc.keys():
                pass
            else:
                misc['prpos'] = '_'
            '''
            

            words.append({
                'book' : sentence['book'],
                'chapter' : sentence['chapter'],
                'section' : sentence['section'],
                'para' : sentence['para'],
                'sent' : sentence['sent'],
                'token_nb' : info_token[0],
                'token_word' : info_token[1],
                'token_lemma' : info_token[2],
                'token_ud' : info_token[3],
                'token_up' : info_token[4],
                'token_head' : info_token[6],
                'token_function' : info_token[7], 
                'misc' : info_token[9].rstrip('\n')
                                })

    #On écrit l'XML en remplissant les éléments avec les différentes variables

    #On génère l'élément racine "text"

    data = ET.Element('text') 

    #Le premier enfant de chaque structure est "1"
    '''
    book = "1"
    chapter = "1"
    section = "1"
    para = "1"
    sent = "1"
    '''
    book = "1"
    chapter = "1"
    section = "1"
    para = "1"
    sent = "1"
    #On construit les éléments.

    livre = ET.Element("div", attrib={'type':'book', 'n': book})
    chapitre = ET.Element("div", attrib={'type':'chapter', 'n':chapter})
    sect = ET.Element("div", attrib={'type':'section', 'n': section})
    parag = ET.Element("p", attrib={'n':para})
    phrase = ET.Element("s", attrib={'n':sent})

    for word in words:
        
        #On construit l'élément w avec les infos du conll
        mot = ET.Element('w', attrib={
            'n': word['token_nb'],
            'udpos': word['token_ud'],
            'uppos': word['token_up'],
            'lemma': word['token_lemma'],
            'head': word['token_head'],
            'function': word['token_function'],
            'misc': word['misc']
        })
        
        mot.text = word['token_word']
        
        #On reconstruit la structure jusqu'au niveau de la phrase.
        
        
        if word['book'] == book:
            if word['chapter'] == chapter:
                if word['section'] == section:
                    if word['para'] == para:
                        if word['sent'] == sent:
                            phrase.append(mot)
                        
                        else: #mot
                            parag.append(phrase)
                            sent = word['sent']
                            del phrase
                            phrase = ET.Element("s", attrib={'n':sent})
                            
                            phrase.append(mot)
                            
                    # On ferme les éléments progressivement pour garder la structure du XML.

                    else: #para
                        parag.append(phrase)
                        para = word['para']
                        del phrase
                        
                        sect.append(parag)
                        sent = word['sent']
                        del parag
                        
                        phrase = ET.Element("s", attrib={'n':sent})
                        parag = ET.Element("p", attrib={'n':para})
                        
                        phrase.append(mot)

                else: #section
                    parag.append(phrase)
                    para = word['para']
                    del phrase

                    sect.append(parag)
                    sent = word['sent']
                    del parag
                    
                    chapitre.append(sect)
                    section = word['section']
                    del sect
                    
                    phrase = ET.Element("s", attrib={'n':sent})
                    parag = ET.Element("p", attrib={'n':para})
                    sect = ET.Element("div", attrib={'type':'section', 'n': section})
                    
                    phrase.append(mot)

            else: #chapter
                parag.append(phrase)
                para = word['para']
                del phrase

                sect.append(parag)
                sent = word['sent']
                del parag

                chapitre.append(sect)
                section = word['section']
                del sect
                
                livre.append(chapitre)
                chapter = word['chapter']
                del chapitre
                
                phrase = ET.Element("s", attrib={'n':sent})
                parag = ET.Element("p", attrib={'n':para})
                sect = ET.Element("div", attrib={'type':'section', 'n':section})
                chapitre = ET.Element("div", attrib={'type':'chapter', 'n': chapter})
                
                phrase.append(mot)
                
        else: #chapter
            parag.append(phrase)
            para = word['para']
            del phrase
            
            sect.append(parag)
            sent = word['sent']
            del parag

            chapitre.append(sect)
            section = word['section']
            del sect

            livre.append(chapitre)
            chapter = word['chapter']
            del chapitre
            
            data.append(livre)
            book = word['book']
            del livre
            
            phrase = ET.Element("s", attrib={'n':sent})
            parag = ET.Element("p", attrib={'n': para})
            sect = ET.Element("div", attrib={'type':'section', 'n': section})
            chapitre = ET.Element("div", attrib={'type':'chapter', 'n': chapter})
            livre = ET.Element("div", attrib={'type':'book', 'n':book})
            
            phrase.append(mot)

    parag.append(phrase)
    sect.append(parag)
    chapitre.append(sect)
    livre.append(chapitre)
    data.append(livre)
    
    indent_xml(data)
    reorderAttrib(data)

    ET.ElementTree(data).write(outputfile, encoding="utf-8")

def synchronisation_xml(functionw, xmlw, compil, option):
    
    """
    Fonction permettant de comparer deux fichiers XML-TEI ayant la même numérotation des éléments structurant
    book/chapter/section/p/s/w et de reporter les attributs des éléments w du fichier cible vers les éléments
    w dans l'autre fichier, et de produire un nouvel xml.
    
    """

    #import xml.etree.ElementTree as ET
    from lxml import etree as ET
    
    coord={}
    #coord2={}
    #roots=[]
       
    # On importe le XML-TEI d'entrée avec les fonctions et on le lit.
    tree = ET.parse(open(functionw, encoding="utf-8"))
    root = tree.getroot()

#On cible les books, et on récupère l'attribut n

    for book in root.findall('.//div[@type="book"]'):
        book_nb = book.get('n')

    # On cible les chapter, et on récupère l'attribut n

        for chapter in book.findall('.//div[@type="chapter"]'):
            chapter_nb = chapter.get('n')

            # On cible les sections, et on récupère l'attribut n

            for section in chapter.findall('.//div[@type="section"]'):
                section_nb = section.get('n')


                #On cible les paragraphes, et on récupère l'attribut n

                for para in section.findall('.//p'):
                    para_nb = para.get('n')

                        #On cible les sentences, et on récupère l'attribut n

                    for sentence in para.findall('.//s'):
                        sentence_nb = sentence.get('n')

                            # On boucle sur les w

                        for word in sentence.findall('.//w'):
                            word_nb = word.get('n')

                                 # On nomme les coordonnées de la phrase

                            address = book_nb+"-"+chapter_nb+"-"+section_nb+"-"+para_nb+"-"+sentence_nb+"-"+word_nb
                            #address2 = book_nb+"-"+chapter_nb+"-"+section_nb+"-"+para_nb+"-"+sentence_nb+"-"+word_nb

                            # On cherche les attributs voulus, et on remplit les dictionnaires

                            coord[address] = word.attrib
                            #coord2[address2] = word.text
                            #roots.append(address)


   #XML sans fonction
                           
    # On importe le XML-TEI d'entrée et on le lit.
    tree2 = ET.parse(open(xmlw, encoding="utf-8"))
    root = tree2.getroot()

# On cible les book, et on récupère l'attribut n

    for book in root.findall('.//div[@type="book"]'):
        book_nb = book.get('n')

# On cible les chapter, et on récupère l'attribut n

        for chapter in book.findall('.//div[@type="chapter"]'):
            chapter_nb = chapter.get('n')

            # On cible les sections, et on récupère l'attribut n

            for section in chapter.findall('.//div[@type="section"]'):
                section_nb = section.get('n')

                #On cible les paragraphes, et on récupère l'attribut n

                for para in section.findall('.//p'):
                    para_nb = para.get('n')

                        #On cible les sentences, et on récupère l'attribut n

                    for sentence in para.findall('.//s'):
                        sentence_nb = sentence.get('n')

                            # On boucle sur les w

                        for word in sentence.findall('.//w'):
                            #dev print(word.text)
                            word_nb = word.get('n')
                                # On nomme les coordonnées de la phrase

                            address = book_nb+"-"+chapter_nb+"-"+section_nb+"-"+para_nb+"-"+sentence_nb+"-"+word_nb
                            #address2 = book_nb+"-"+chapter_nb+"-"+section_nb+"-"+para_nb+"-"+sentence_nb+"-"+word_nb

                            #coord[address]['lemma_src'] = word.get('lemma_src')

                            if option == 'reparse':

                                word.set('udpos', word.get('udpos'))
                                # word.set('retagging',  coord[address]['udpos'])
                                coord[address]['lemma'] = word.get('lemma')
                                word.set('lemma', word.get('lemma'))
                                word.set('head', coord[address]['head'])
                                word.set('function', coord[address]['function'])
                                word.set('prpos',  word.get('prpos'))
                                word.set('uppos', word.get('uppos'))

                                if word.get('join'):
                                    coord[address]['join'] = word.get('join')
                                else:
                                    coord[address]['join'] = '_'

                                word.set('join', coord[address]['join'])

                                word.attrib['n'] = word.attrib.pop('n')
                                word.attrib['head'] = word.attrib.pop('head')
                                word.attrib['function'] = word.attrib.pop('function')
                                word.attrib['udpos'] = word.attrib.pop('udpos')
                                word.attrib['prpos'] = word.attrib.pop('prpos')
                                word.attrib['uppos'] = word.attrib.pop('uppos')
                                # word.attrib['retagging'] = word.attrib.pop('retagging')
                                word.attrib['lemma'] = word.attrib.pop('lemma')

                                #word.attrib['lemma_src'] = word.attrib.pop('lemma_src')
                                word.attrib['join'] = word.attrib.pop('join')
                            
                            else:
                                word.set('udpos', coord[address]['udpos'])
                                word.set('head', coord[address]['head'])
                                word.set('function', coord[address]['function'])

                                if word.get('join'):
                                    coord[address]['join'] = word.get('join')
                                else:
                                    coord[address]['join'] = '_'

                                word.set('join', coord[address]['join'])

                                word.attrib['n'] = word.attrib.pop('n')
                                word.attrib['head'] = word.attrib.pop('head')
                                word.attrib['function'] = word.attrib.pop('function')
                                word.attrib['udpos'] = word.attrib.pop('udpos')
                                word.attrib['join'] = word.attrib.pop('join')
                            
                            #dev 
                            print(word.attrib)

    # On écrit le TEI obtenu dans le fichier spécifié en second paramètre.
    
    #tree2.write(compil, xml_declaration=False, encoding="utf-8")
    
    #ET.dump(tree)

    reorderAttrib(tree2)
    tree2.write(compil, pretty_print=True, encoding="utf-8")

def add_sent_id(inputfile, outputfile):

    # On importe le XML-TEI d'entrée avec les fonctions et on le lit.
    tree = ET.parse(open(inputfile, encoding="utf-8"))
    root = tree.getroot()

#On cible les books, et on récupère l'attribut n

    for book in root.findall('.//div[@type="book"]'):
        book_nb = book.get('n')

    # On cible les chapter, et on récupère l'attribut n

        for chapter in book.findall('.//div[@type="chapter"]'):
            chapter_nb = chapter.get('n')

            # On cible les sections, et on récupère l'attribut n

            for section in chapter.findall('.//div[@type="section"]'):
                section_nb = section.get('n')


                #On cible les paragraphes, et on récupère l'attribut n

                for para in section.findall('.//p'):
                    para_nb = para.get('n')

                        #On cible les sentences, et on récupère l'attribut n

                    for sentence in para.findall('.//s'):
                        sentence_nb = sentence.get('n')

                            # On boucle sur les w

                        sent_id = book_nb+"_"+chapter_nb+"_"+section_nb+"_"+para_nb+"_"+sentence_nb

                        sentence.set("sent_id", sent_id)
    
    ET.ElementTree(root).write(outputfile, encoding="utf-8")

### Lemmatisation/Conversion tagsets ##########################
def make_d_PRESTO(path_PRESTO):
    '''
    url = "https://unicloud.unicaen.fr/index.php/s/An5wqjdLHiPFwKt/download/dico_PRESTO_SIMPLE_10.01.23.dff"
    r = requests.get(url, allow_redirects=True)
    path_PRESTO = '/home/ziane212/crisco_work_ressources/test/presto.dff'
    open(path_PRESTO, 'wb').write(r.content)
    '''
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
    '''
    url = "https://unicloud.unicaen.fr/index.php/s/An5wqjdLHiPFwKt/download/dico_PRESTO_SIMPLE_10.01.23.dff"
    r = requests.get(url, allow_redirects=True)
    path_CorrTable = '/home/ziane212/crisco_work_ressources/test/corrTable.csv'
    open(path_CorrTable, 'wb').write(r.content)
    '''
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

def resolv_ambi(inputfile, outputfile):

    tree = ET.parse(open(inputfile, encoding="utf-8"))
    root = tree.getroot()

    l_function_AUX = ['aux', 'aux:pass', 'cop']
    l_function_VERB = ['root', 'ccomp', 'acl:relcl', 'parataxis']
    l_lemma_AUX = ['être', 'avoir']

    for id_, s in enumerate(root.findall('.//s')):
        
        for w in s.findall('.//w'):
            
            # classique
            if (w.get('uppos') ==  'VPP///VJ' or w.get('uppos') ==  'EPP///EJ' or w.get('uppos') ==  'APP///AJ') and w.get('function') in l_function_VERB :
                id_parent = w.get('n')
                var = False
                for w2 in root.findall('.//s')[id_]:
                    
                    if w2.get('head') == id_parent and w2.get('udpos') == 'AUX':
                        
                        var = True
                    
                    if w2.get('head') == id_parent and w2.get('udpos') == 'AUX' and w2.get('function') in l_function_AUX and w2.get('lemma') in l_lemma_AUX:
                        
                        if w.get('uppos') ==  'VPP///VJ':
                            w.set('uppos', 'VPP')
                            w.set('prpos', 'Ge')
                            w.set('ambiguite', 'standard1')
                        elif w.get('uppos') ==  'APP///AJ':
                            w.set('uppos', 'APP')
                            w.set('prpos', 'Ge')
                            w.set('ambiguite', 'standard1')
                        elif w.get('uppos') ==  'EPP///EJ':
                            w.set('uppos', 'EPP')
                            w.set('prpos', 'Ge')
                            w.set('ambiguite', 'standard1')
                    
                if var == False:
                    if w.get('uppos') ==  'VPP///VJ':
                        w.set('uppos', 'VJ')
                        w.set('prpos', 'Vvc')
                        w.set('ambiguite', 'standard2')
                    elif w.get('uppos') ==  'APP///AJ':
                        w.set('uppos', 'AJ')
                        w.set('prpos', 'Vuc')
                        w.set('ambiguite', 'standard2')
                    elif w.get('uppos') ==  'EPP///EJ':
                        w.set('uppos', 'EJ')
                        w.set('prpos', 'Vuc')
                        w.set('ambiguite', 'standard2')                    
            
            # doubles auxiliaires
            if w.get('uppos') ==  'APP///AJ' or w.get('uppos') ==  'EPP///EJ':
                
                id_parent = w.get('head')
                function_w = w.get('function')
                
                for w2 in root.findall('.//s')[id_]:
                    if w2.get('n') == id_parent:
                        udpos_parent = w2.get('udpos')
                        uppos_parent = w2.get('uppos')
                        
                        var = False
                        
                        for w3 in root.findall('.//s')[id_]:
                            if w3.get('head') == id_parent and w3.get('udpos') == 'AUX' and w3.get('lemma') in l_lemma_AUX:
                                
                                var = True
                                
                            if var == True:
                                
                                if w.get('uppos') ==  'APP///AJ':
                                    w.set('uppos', 'APP')
                                    w.set('prpos', 'Ge')
                                elif w.get('uppos') ==  'EPP///EJ':
                                    w.set('uppos', 'EPP')
                                    w.set('prpos', 'Ge')
                                
                                if udpos_parent == 'NOUN' or udpos_parent == 'ADJ':
                                    if function_w == 'cop':
                                        w.set('ambiguite', 'copule')
                                    else:
                                        w2.set('fiabilite', 'fonction')
                                
                                elif udpos_parent == 'VERB':
                                    if function_w == 'aux' or function_w == 'aux:pass' :
                                        w.set('ambiguite', 'auxiliaire')
                                    else:
                                        w2.set('fiabilite', 'fonction')
                                        
                                    if uppos_parent == 'VJ':
                                        w2.set('uppos', 'VPP')
                                        w2.set('prpos', 'Ge')
                                        w2.set('ambiguite', 'standard3')
                                
                                if w.get('ambiguite') == None:
                                    w.set('ambiguite', 'spe')
            
            # conj
            if (w.get('uppos') ==  'VPP///VJ' or w.get('uppos') ==  'APP///AJ' or w.get('uppos') ==  'EPP///EJ') and w.get('function') ==  'conj':
                
                head_parent = w.get('head')
                id_parent = w.get('n')

                for w2 in root.findall('.//s')[id_]:

                    if w2.get('head') == id_parent and (w2.get('function') == 'nsubj' or w2.get('function') == 'expl'):
                        for w3 in root.findall('.//s')[id_]:
                            if w3.get('head') == id_parent and w3.get('udpos') == 'AUX' and w3.get('function') in l_function_AUX and w3.get('lemma') in l_lemma_AUX:
                                b_spot_aux = True
                        
                        if b_spot_aux == False:
                            w.set('uppos', 'VJ')
                            w.set('prpos', 'Vvc')
                            w.set('ambiguite', 'subj')
                        else:                        
                            if w.get('lemma')=='être':
                                w.set('uppos', 'EPP')
                                w.set('prpos', 'Ge')
                            elif w.get('lemma')=='avoir':
                                w.set('uppos', 'APP')
                                w.set('prpos', 'Ge')
                            else:
                                w.set('uppos', 'VPP')
                                w.set('prpos', 'Ge')
                            w.set('ambiguite', 'subj')
                
                    elif w2.get('n') == head_parent and w2.get('udpos') == 'VERB' and w2.get('uppos') == 'VPP' :
                        id_parent = w2.get('n')
                        
                        for w3 in root.findall('.//s')[id_]:
                            if w3.get('head') == id_parent and w3.get('udpos') == 'AUX' and w3.get('function') in l_function_AUX and w3.get('lemma') in l_lemma_AUX:                   
                                if w.get('lemma')=='être':
                                    w.set('uppos', 'EPP')
                                    w.set('prpos', 'Ge')
                                elif w.get('lemma')=='avoir':
                                    w.set('uppos', 'APP')
                                    w.set('prpos', 'Ge')
                                else:
                                    w.set('uppos', 'VPP')
                                    w.set('prpos', 'Ge')
                                w.set('ambiguite', 'conj1')
                    
                    elif w2.get('n') == head_parent and w2.get('udpos') == 'VERB' and (w2.get('uppos') == 'VJ' or w2.get('uppos') == 'EJ' or w2.get('uppos') == 'AJ') :
                        if w.get('lemma')=='être':
                            w.set('uppos', 'EJ')
                            w.set('prpos', 'Vuc')
                        elif w.get('lemma')=='avoir':
                            w.set('uppos', 'AJ')
                            w.set('prpos', 'Vuc')
                        else:
                            w.set('uppos', 'VJ')
                            w.set('prpos', 'Vvc')
                        w.set('ambiguite', 'conj2')

            # xcomp
            if w.get('uppos') ==  'VPP///VJ' and w.get('function') ==  'xcomp':
                
                head_parent = w.get('head')
                id_parent = w.get('n')

                b_spot_aux = False

                for w2 in root.findall('.//s')[id_]:

                    if w2.get('head') == id_parent and w2.get('udpos') == 'AUX' and w2.get('lemma') in l_lemma_AUX:
                        b_spot_aux = True

                if b_spot_aux == False:
                    w.set('uppos', 'VX')
                    w.set('prpos', 'Vvn')
                    w.set('ambiguite', 'xcomp1')
                    
                elif b_spot_aux == True:
                    w.set('uppos', 'VPP')
                    w.set('prpos', 'Ge')
                    w.set('ambiguite', 'xcomp2')

            
            # advcl
            if (w.get('uppos') ==  'VPP///VJ' or w.get('uppos') ==  'APP///AJ' or w.get('uppos') ==  'EPP///EJ') and w.get('function') ==  'advcl':
                
                head_parent = w.get('head')
                id_parent = w.get('n')

                b_spot_aux = False

                for w2 in root.findall('.//s')[id_]:

                    if w2.get('head') == id_parent and w2.get('udpos') == 'AUX' and w2.get('lemma') in l_lemma_AUX:
                        b_spot_aux = True

                if b_spot_aux == False:
                    if w.get('lemma')=='être':
                        w.set('uppos', 'EJ')
                        w.set('prpos', 'Vuc')
                    elif w.get('lemma')=='avoir':
                        w.set('uppos', 'AJ')
                        w.set('prpos', 'Vuc')
                    else:
                        w.set('uppos', 'VJ')
                        w.set('prpos', 'Vvc')
                        w.set('ambiguite', 'advcl1')
                    
                elif b_spot_aux == True:
                    if w.get('lemma')=='être':
                        w.set('uppos', 'EPP')
                        w.set('prpos', 'Ge')
                    elif w.get('lemma')=='avoir':
                        w.set('uppos', 'APP')
                        w.set('prpos', 'Ge')
                    else:
                        w.set('uppos', 'VPP')
                        w.set('prpos', 'Ge')
                    w.set('ambiguite', 'advcl2')
            
            # acl
            # if w.get('uppos') ==  'VPP///VJ' and w.get('function') ==  'acl':
                
            #     id_parent = w.get('n')

            #     for w2 in root.findall('.//s')[id_]:

            #         if w2.get('head') == id_parent and w2.get('udpos') == 'AUX' and w2.get('lemma') in l_lemma_AUX:                
            #             w.set('uppos', 'VPP')
            #             w.set('prpos', 'Ge')
            #             w.set('ambiguite', 'acl')
            
            # Pr
            try:
                if w.get('prpos') ==  'Pr///Pt' and s.findall('.//w')[len(s)-1].text =='?':
                    w.set('prpos', 'Pt')
                    w.set('ambiguite', "PronType")
                elif w.get('prpos') ==  'Pr///Pt':
                    w.set('prpos', 'Pr')
                    w.set('ambiguite', "PronType")
            except IndexError:
                pass

    indent_xml(root)

    reorderAttrib(root)

    ET.ElementTree(root).write(outputfile, encoding="utf-8")

def annotNPL(inputfile, outputfile):

    tree = ET.parse(open(inputfile, encoding="utf-8"))
    root = tree.getroot()

    l_numSG = ['un']

    for id_, s in enumerate(root.findall('.//s')):
        
        for id_w, w in enumerate(s.findall('.//w')):
                
            if w.get('uppos') ==  'NCS' or w.get('uppos') ==  'NPRS':
                id_gov = w.get('n')
                
                for w2 in root.findall('.//s')[id_]:
                    
                    id_dep = w2.get('n')
                    
                    if w2.get('head') == id_gov and w2.get('function') == 'nummod' and id_gov > id_dep:
                        
                        if w.get('lemma') in l_numSG:
                            pass
                        else:
                            if w.get('uppos') ==  'NCS':
                                w.set('uppos', 'NCPL')
                                w.set('annot_PL', "nummod1")
                            if w.get('uppos') ==  'NPRS':
                                w.set('uppos', 'NPRPL')
                                w.set('annot_PL', "nummod1")                            
                    
                    if w2.get('head') == id_gov and w2.get('udpos')=='DET' and (w2.text.endswith('s') or w2.text.endswith('z') or w2.text.endswith('x')):                                                              
                        if w.get('uppos') ==  'NCS':
                            w.set('uppos', 'NCPL')
                            w.set('annot_PL', "nummod2")
                        if w.get('uppos') ==  'NPRS':
                            w.set('uppos', 'NPRPL')
                            w.set('annot_PL', "nummod2")

                    if w2.get('head') == id_gov and (w2.attrib['lemma']=='à+le' or w2.attrib['lemma']=='de+le') and (w2.text.endswith('s') or w2.text.endswith('z') or w2.text.endswith('x')):                                                              
                        if w.get('uppos') ==  'NCS':
                            w.set('uppos', 'NCPL')
                            w.set('annot_PL', "nummod3")
                        if w.get('uppos') ==  'NPRS':
                            w.set('uppos', 'NPRPL')
                            w.set('annot_PL', "nummod3")

    indent_xml(root)

    reorderAttrib(root)

    ET.ElementTree(root).write(outputfile, encoding="utf-8")

def convNoMatching(inputfile, outputfile):

    tree = ET.parse(open(inputfile, encoding="utf-8"))
    root = tree.getroot()
    l_lemma_AUX = ['être', 'avoir']
    l_MD = ["devoir", "pouvoir", "vouloir"]
    l_function_noConv = ['root', 'acl:relcl', 'advcl', 'ccomp']

    for id_, s in enumerate(root.findall('.//s')):
        
        for id_w, w in enumerate(s.findall('.//w')):
            
            if w.get('uppos') ==  '_' and w.get('prpos') ==  '_' and w.get('function') in l_function_noConv and w.get('udpos')=='VERB':
                id_parent = w.get('n')

                var = False
                for w2 in root.findall('.//s')[id_]:
                    
                    if w2.get('head') == id_parent and w2.get('udpos') == 'AUX':
                        var = True
                        lemma_AUX = w2.get('lemma') 
                    
                if var == False:
                    if w.get('function') == 'advcl':
                        pass
                    else:
                        if w.get('lemma')=='être':
                            w.set('uppos', 'EJ')
                            w.set('prpos', 'Vuc')
                        elif w.get('lemma')=='avoir':
                            w.set('uppos', 'AJ')
                            w.set('prpos', 'Vuc')
                        elif w.get('lemma') in l_MD:
                            w.set('uppos', 'MDJ')
                            w.set('prpos', 'Vvc')
                        else:
                            w.set('uppos', 'VJ')
                            w.set('prpos', 'Vvc')
                        w.set('convNoMatching', '1')
                
                elif var == True:
                    if lemma_AUX not in l_lemma_AUX:
                        if w.get('lemma')=='être':
                            w.set('uppos', 'EX')
                            w.set('prpos', 'Vun')
                        elif w.get('lemma')=='avoir':
                            w.set('uppos', 'AX')
                            w.set('prpos', 'Vun')
                        elif w.get('lemma') in l_MD:
                            w.set('uppos', 'MDX')
                            w.set('prpos', 'Ge')
                        else:
                            w.set('uppos', 'VX')
                            w.set('prpos', 'Vvn')
                        w.set('convNoMatching', '2')
                    else:
                        if w.get('lemma')=='être':
                            w.set('uppos', 'EPP')
                            w.set('prpos', 'Ge')
                        elif w.get('lemma')=='avoir':
                            w.set('uppos', 'APP')
                            w.set('prpos', 'Ge')
                        elif w.get('lemma') in l_MD:
                            w.set('uppos', 'MDPP')
                            w.set('prpos', 'Ge')
                        else:
                            w.set('uppos', 'VPP')
                            w.set('prpos', 'Ge')
                    
                        w.set('convNoMatching', '3')

    indent_xml(root)

    reorderAttrib(root)

    ET.ElementTree(root).write(outputfile, encoding="utf-8")



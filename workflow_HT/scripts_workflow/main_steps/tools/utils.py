import sys, getopt
import xml.etree.ElementTree as ET
import copy
from tqdm import tqdm
import re

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

    import xml.etree.ElementTree as ET
    
    # On importe le XML-TEI d'entrée et on le lit.
    tree = ET.parse(inputfile)
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
    ET.ElementTree(root).write(outputfile, encoding="utf-8")

def conversion_xml2conllu(inputfile, outputfile):
    # On ouvre le fichier de sortie
    with open(outputfile, 'w', encoding="utf8") as conll:

    # On importe le XML-TEI d'entrée et on le lit.
        tree = ET.parse(inputfile)
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
                            book_ch = 1
                            book_nb = "1"
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

                                form = ""
                                if len(list(word))!=0:
                                    if list(word)[0].tag == 'choice':
                                        form = list(word)[0][1].text

                                    else:

                                        for child in word.iter():
                                            if child.text:
                                                form += child.text
                                            if child.tail:
                                                form += child.tail
                                else:
                                    form = word.text
                                #dev 
                                print(form)
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
            for id_, j in enumerate(misc_temp):
                misc_temp[id_] = misc_temp[id_].split('=')
                misc[misc_temp[id_][0].replace(' ', '')] = misc_temp[id_][1].replace(' ', '')
            
            if 'incoherence' in misc.keys():
                pass
            else:
                misc['incoherence'] = '_'
                
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
                'token_function' : info_token[7]
                                })

    #On écrit l'XML en remplissant les éléments avec les différentes variables

    #On génère l'élément racine "text"

    data = ET.Element('text') 

    #Le premier enfant de chaque structure est "1"

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
            sect = ET.Element("div", attrib={'type':section})
            chapitre = ET.Element("div", attrib={'type':'chapter', 'n': chapter})
            livre = ET.Element("div", attrib={'type':'chapter', 'n':book})
            
            phrase.append(mot)

    parag.append(phrase)
    sect.append(parag)
    chapitre.append(sect)
    livre.append(chapitre)
    data.append(livre)
    
    indent_xml(data)

    ET.ElementTree(data).write(outputfile, encoding="utf-8")

def synchronisation_xml(functionw, xmlw, compil):
    
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
                            word_nb = word.get('n')
                                # On nomme les coordonnées de la phrase

                            address = book_nb+"-"+chapter_nb+"-"+section_nb+"-"+para_nb+"-"+sentence_nb+"-"+word_nb
                            #address2 = book_nb+"-"+chapter_nb+"-"+section_nb+"-"+para_nb+"-"+sentence_nb+"-"+word_nb

                            #coord[address]['lemma_src'] = word.get('lemma_src')

                            word.set('udpos', coord[address]['udpos'])
                            
                            #coord[address]['lemma'] = word.get('lemma')
                            word.set('lemma', coord[address]['lemma'])

                            word.set('head', coord[address]['head'])

                            word.set('function', coord[address]['function'])

                            if word.get('join'):
                                coord[address]['join'] = word.get('join')
                            else:
                                coord[address]['join'] = '_'

                            word.attrib['n'] = word.attrib.pop('n')
                            word.attrib['udpos'] = word.attrib.pop('udpos')
                            #word.attrib['lemma'] = word.attrib.pop('lemma')
                            word.attrib['head'] = word.attrib.pop('head')
                            word.attrib['function'] = word.attrib.pop('function')
                            #word.attrib['lemma_src'] = word.attrib.pop('lemma_src')
                            #word.attrib['join'] = word.attrib.pop('join')
                            #word.attrib['prpos'] = word.attrib.pop('prpos')
                            #word.attrib['uppos'] = word.attrib.pop('uppos')
                            #word.attrib['retagging'] = word.attrib.pop('retagging')
                            #dev print(word.attrib)

                            '''
                            if address in coord.keys():
                                if word.get('join'):
                                    coord[address]['join'] = word.get('join')
                                else:
                                    coord[address]['join'] = '_'

                                if word.get('incoherence'):
                                    coord[address]['incoherence'] = word.get('incoherence')
                                else:
                                    coord[address]['incoherence'] = '_'

                                if word.get('NoMatchingPresto'):
                                    coord[address]['NoMatchingPresto'] = word.get('NoMatchingPresto')
                                else:
                                    coord[address]['NoMatchingPresto'] = '_'

                                if word.get('NoConvUPenn'):
                                    coord[address]['NoConvUPenn'] = word.get('NoConvUPenn')
                                else:
                                    coord[address]['NoConvUPenn'] = '_'
                            '''


                            '''
                            if word.get('udpos'):
                                coord[address]['udpos'] = word.get('udpos')
                            else:
                                coord[address]['udpos'] = '_'

                            if word.get('head'):
                                coord[address]['head'] = word.get('head')
                            else:
                                coord[address]['head'] = '_'

                            if word.get('function'):
                                coord[address]['function'] = word.get('function')
                            else:
                                coord[address]['function'] = '_'

                            '''    
                            #word.attrib = coord[address]

                            #if address2 in coord2.keys():
                                #word.text = coord2[address2]

    # On écrit le TEI obtenu dans le fichier spécifié en second paramètre.
    
    #tree2.write(compil, xml_declaration=False, encoding="utf-8")
    
    #ET.dump(tree)
    tree2.write(compil, pretty_print=True, encoding="utf-8")

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


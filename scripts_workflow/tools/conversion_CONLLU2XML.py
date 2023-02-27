import sys, getopt
import xml.etree.ElementTree as ET
import re
from xml.dom import minidom 
import os

def main(argv):
   global inputfile
   global outputfile
   inputfile = ''
   outputfile = ''
   opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   for opt, arg in opts:
      if opt == '-h':
         print ('conversion_XML2CONLLU.py -i <inputfile_path> -o <outputfile_path>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print ('Input file is ', inputfile)
   print ('Output file is ', outputfile)

def indent(elem, level=0, more_sibs=False):
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
            indent(kid, level+1, count < num_kids - 1)
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

def conversion(inputfile, outputfile):
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
                '''
                sentence_str = re.search("\d+-\d+-\d+-\d+-\d+", line).group()
                num2 = sentence_str.split('-')
                '''
                sentence_str = re.search("\d+_\d+_\d+_\d+_\d+", line).group()
                num2 = sentence_str.split('_')

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
    
    indent(data)

    ET.ElementTree(data).write(outputfile, encoding="utf-8")

if __name__ == "__main__":
   main(sys.argv[1:])
   conversion(inputfile, outputfile)
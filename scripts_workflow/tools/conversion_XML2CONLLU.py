import sys, getopt
import xml.etree.ElementTree as ET
import re

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

def conversion(inputfile, outputfile):
    # On ouvre le fichier de sortie
    with open(outputfile, 'w', encoding="utf8") as conll:

    # On importe le XML-TEI d'entrée et on le lit.
        tree = ET.parse(inputfile)
        root = tree.getroot()

        # On donne au module XML le namespace de la TEI, sans préfixe car ce sera le seul.
        #ET.register_namespace('', "http://www.tei-c.org/ns/1.0")    

        #On boucle sur les balises w, en reprenant la hiérarchie, et on met en forme conll avec les balises
        '''               
        # On crée un compteur pour les numéros de book
        for book in root.findall('.//div[@type="book"]'):
            book_nb = book.get('n')
            book_ch = int(book_nb)
        '''    

        # On cible les chapter, et on récupère l'attribut n

        for chapter in root.findall('.//div[@type="chapter"]'):
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
                            #dev print(form)
                            mot = word_nb+"\t"+form.replace("\t", "").replace("\n", "")+"\t"+lemma+"\t"+udpos+"\t"+uppos+"\t_\t"+head+"\t"+function+"\t_\tjoin="+join+"|prpos="+prpos+"\n"          

                            strmot = str(mot)

                            #On écrit le fichier de sortie

                            conll.write(strmot)

                
if __name__ == "__main__":
   main(sys.argv[1:])
   conversion(inputfile, outputfile)
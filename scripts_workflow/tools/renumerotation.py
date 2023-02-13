import sys, getopt

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

def id_tokens_in_tei(chemin_entree, chemin_sortie):
    
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
    tree = ET.parse(chemin_entree)
    root = tree.getroot()
    
    # On donne au module XML le namespace de la TEI, sans préfixe car ce sera le seul.
    #ET.register_namespace('', "http://www.tei-c.org/ns/1.0")    
    
    #On crée un compteur pour les numéros de book
    '''
    # On crée un compteur pour les numéros de chapter
    for counter_book, book in enumerate(root.findall(".//div[@type='book']"), 1):
        if book.get('n'):
            del book.attrib['n']
        book.set('n', str(counter_book))
    '''
    # On crée un compteur pour les numéros de chapter
    for counter_chapter, chapter in enumerate(root.findall(".//div[@type='chapter']"), 1):
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
    tree.write(chemin_sortie, xml_declaration=False, encoding="utf-8")
    tree = ET.parse(open(outputfile, encoding='utf-8'))
    root = tree.getroot()
    indent(root)
    ET.ElementTree(root).write(outputfile, encoding="utf-8")
                
if __name__ == "__main__":
   main(sys.argv[1:])
   id_tokens_in_tei(inputfile, outputfile)

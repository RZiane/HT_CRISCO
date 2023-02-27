from __future__ import annotations

from tkinter import *
from tkinter import filedialog

import customtkinter

import re
import xml.etree.ElementTree as ET
import os
import copy

#os.system('Xvfb :1 -screen 0 1600x1200x16  &')    # create virtual display with size 1600x1200 and 16 bit color. Color can be changed to 24 or 8
os.environ['DISPLAY']=':1.0'    # tell X clients to use our virtual DISPLAY :1.0

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

def onClick_punct():
    CheckVar1, CheckVar2 = punct_settings()

def select_all_boxes():
    CheckVar1.set(1)
    CheckVar2.set(1)
    CheckVar3.set(1)
    CheckVar4.set(1)
    CheckVar5.set(1)
    CheckVar6.set(1)


def punct_settings():
    
    global fenetre_options_punct
    fenetre_options_punct = Toplevel()
    fenetre_options_punct.title("Punctuation Settings")
    fenetre_options_punct.geometry("320x240")
    fenetre_options_punct.minsize(320, 240)

    global CheckVar1
    global CheckVar2
    global CheckVar3
    global CheckVar4
    global CheckVar5
    global CheckVar6
    global CheckVar7

    CheckVar1 = IntVar()
    CheckVar2 = IntVar()
    CheckVar3 = IntVar()
    CheckVar4 = IntVar()
    CheckVar5 = IntVar()
    CheckVar6 = IntVar()
    CheckVar7 = IntVar()

    C1 = customtkinter.CTkCheckBox(fenetre_options_punct, text = " . (full stop)", variable = CheckVar1, \
                     onvalue = 1, offvalue = 0)

    C2 = customtkinter.CTkCheckBox(fenetre_options_punct, text = " ; (semi-colon)", variable = CheckVar2, \
                     onvalue = 1, offvalue = 0)

    C3 = customtkinter.CTkCheckBox(fenetre_options_punct, text = " ? (question mark)", variable = CheckVar3, \
                     onvalue = 1, offvalue = 0)

    C4 = customtkinter.CTkCheckBox(fenetre_options_punct, text = " ! (exclamation mark)", variable = CheckVar4, \
                     onvalue = 1, offvalue = 0)

    C5 = customtkinter.CTkCheckBox(fenetre_options_punct, text = " : (colon)", variable = CheckVar5, \
                     onvalue = 1, offvalue = 0)
    
    C6 = customtkinter.CTkCheckBox(fenetre_options_punct, text = " ... (ellipsis)", variable = CheckVar6, \
                     onvalue = 1, offvalue = 0)

    C7 = customtkinter.CTkCheckBox(fenetre_options_punct, text = "Select all punctuations", variable = CheckVar7, \
                     command=select_all_boxes, onvalue = 1, offvalue = 0)


    empty = customtkinter.CTkLabel(master=fenetre_options_punct, 
                        text="")
    empty.pack()

    C7.pack()

    C1.pack()
    C2.pack()
    C3.pack()
    C4.pack()
    C5.pack()
    C6.pack()
    
    
    bouton_set_options_punct = customtkinter.CTkButton(master=fenetre_options_punct, text="SET OPTIONS", command=set_options_punct)
    
    bouton_set_options_punct.pack()
        
    return(CheckVar1, CheckVar2)

def set_options_punct():

    global list_ponct_fortes
    point = ('.', CheckVar1.get())
    point_virgule = (';', CheckVar2.get())
    point_interrogation = ('?', CheckVar3.get())
    point_exclamation = ('!', CheckVar4.get())
    deux_points = (':', CheckVar5.get())
    points_suspension = ('...', CheckVar6.get())
    points_suspension2 = ('…', CheckVar6.get())
    
    all_puncts = ('all', CheckVar7.get())
    
    if all_puncts[1]==1:
        list_ponct_fortes = [('.', 1), (';', 1), ('?', 1), ('!', 1), (':', 1), ('...', 1), ('…', 1)]
    else:
        list_ponct_fortes = [point, point_virgule, point_interrogation, point_exclamation, deux_points, points_suspension, points_suspension2]
    
    fenetre_options_punct.destroy()

def len_settings():
    
    global fenetre_options_len
    fenetre_options_len = Toplevel()
    fenetre_options_len.title("Long sentences length")
    fenetre_options_len.geometry("400x120")
    fenetre_options_len.minsize(400, 120)

    global entry
    empty = customtkinter.CTkLabel(master=fenetre_options_len, 
                        text="")
    entry = customtkinter.CTkEntry(master=fenetre_options_len, width=3)
    label_entry1 = customtkinter.CTkLabel(master=fenetre_options_len, 
                        text="'Too-long' sentence starts at")
    label_entry2 = customtkinter.CTkLabel(master=fenetre_options_len, 
                        text="tokens.")
    empty.grid(row=0,column=0)                    
    label_entry1.grid(row=1,column=0)
    #label_entry1.pack()
    entry.grid(row=1,column=1)
    #entry.pack()
    label_entry2.grid(row=1,column=2)
    #label_entry2.pack()
    
    bouton_set_options_len = customtkinter.CTkButton(master=fenetre_options_len, text="SET OPTIONS", command=set_options_len)
    bouton_set_options_len.grid(row=3, columnspan=3)
    #bouton_set_options_len.pack(side=BOTTOM)

def set_options_len():

    global len_sent_option
    len_sent_option = entry.get()

    fenetre_options_len.destroy()

def build_len_sent_option():
    global len_sent_option_var
    len_sent_option_var = int(len_sent_option)
    return len_sent_option_var

def extract_stats():
    
    import statistics
    
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

def extract_lg_sents():
        
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

def upload_path():
    global source_path
    source_path = str(source)
    return source_path

def browseFile():
    global source
    source = filedialog.askopenfilename(initialdir="/",
                                        title="Select a File",
                                        filetypes=(("all files",
                                                    "*.*"),
                                                   ("Text files",
                                                    "*.txt*")))
    
    source_path = upload_path()

    var_msg = "This file is uploaded:\n"+source_path+""

    label_upload = customtkinter.CTkLabel(master=frame, text=var_msg)

    label_upload.pack()

    download_insert_frame.pack()
    label_download.pack()
    label_download2.pack()
    bouton_option_punct.pack()
    bouton_download.pack()
    
def saveFile():
    global dir_file
    dir_file = '/'.join(source.split('/')[:len(source.split('/'))-1])+'/'
        
    global cible
    cible = filedialog.asksaveasfilename(initialdir=dir_file,
                                         title="Select a File",
                                         filetypes=(("eXtensible Markup Language",
                                                     "*.xml*"),
                                                    ("all files",
                                                     "*.*")))
                                                     
    cible = cible.rstrip('.xml')+'.xml'
    
    # ouverture fichier d'entrée (source récupérée dans browseFile)
    f = open(source, encoding='utf-8')
    file = []
    for i in f:
        file.append(i)

    f.close()

    # Prétraitement Rouillé

    file = ''.join(file)
    file = re.sub("#### 1 ####\n\n", '', file)
    file = re.sub("\n####\s\d*\s####\n\n", '', file)
    file = file.split('\n\n')
    #file = ''.join(file)
    
    print(file)
    
    file2 = []
    for i in file:

        i = re.sub('-\n', '', i)
        i = re.sub('\n', ' ', i)

        # nombre latin
        m = re.finditer('\.?([MIJVXLCDmijvxlcd\s]+\.*)\.', i)
        for x in m:
            sub = x[0].replace('.', '#1')
            i = i.replace(x[0], sub)
        '''
        m = re.finditer('(?![MIJVXLCDmijvxlcd])\s*\.', i)
        for x in m:
            sub = x[0].replace('.', '#1')
            i = i.replace(x[0], sub)
        '''
        # nombre arabe
        m = re.finditer('([0-9]+\.\s[^A-Z])', i)
        for x in m:
            sub = x[0].replace('.', '#1')
            i = i.replace(x[0], sub)
        
        # abbreviation
        m = re.finditer('(\s[a-z]{1,2}\.\s[^A-Z])', i)
        for x in m:
            sub = x[0].replace('.', '#1')
            i = i.replace(x[0], sub)

        # choices
        m = re.finditer('<choice((?!choice).)*</choice>', i)
        for x in m:
            sub = x[0].replace(' ', '%')
            i = i.replace(x[0], sub)

        # hi
        m = re.finditer('<hi((?!hi).)*</hi>', i)
        for x in m:
            sub = x[0].replace(' ', '%')
            i = i.replace(x[0], sub)

        i = re.sub(':', ' :', i)
        i = re.sub('\?', ' ?', i)
        i = re.sub('\!', ' !', i)
        i = i.rstrip(' ').lstrip(' ')
        
        file2.append(i)

    # traitement
    corpus = []

    list_tokenisation = ['l', 'd', 'n', 'i', 's'] # lettre q et qu à intégrer ?
    list_substitution = [('v','u'), ('u','v'), ('i','j'), ('j', 'i')]
    list_spec_char = ['ſ']
    list_punct = [';', ',', '.', ':', '!', '?', '.»', '. ', '! ', '? ', '.++']

    '''
    # recupération des métadonnées sur le fichier et ajout dans la liste de travail
    header = file[0].split('.')
    list_header = []
    list_header.append('Author = ' + header[0])
    list_header.append('Date = ' + header[1])
    list_header.append('Title = ' + header[2])
    list_header.append('Source = ' + header[3])
    list_header.append('Pages = ' + header[4])
    #corpus.append(list_header)
    '''
    sent_cnt = 0
    print(list_ponct_fortes)
    global punct_forte_selec
    try:
        punct_forte_selec = []
        for punct_forte in list_ponct_fortes:
            if punct_forte[1]==1:
                punct_forte_selec.append('\\'+punct_forte[0])
    except NameError:
        punct_forte_selec = []

    if punct_forte_selec == []:
        regex_split_sents = r'\s*(\S.{1,}?(?:[0-9a-zàáâäçèéêëîïôöùúûüÿ\»\)\]\s]\.\s?\»?\"?|$))(?=(?:\s+[&A-ZÀÁÂÄÇÈÉÊÌÍÎÏÒÓÔÖÙÚ])|$)'
    else:
        if len(punct_forte_selec)==1 and punct_forte_selec[0] == '\...':
            regex_split_sents = r'\s*(\S.{1,}?(?:[0-9a-zàáâäçèéêëîïôöùúûüÿ\»\)\]\s\.]\.\s?\»?\"?|$)(?=(?:\s+[&A-ZÀÁÂÄÇÈÉÊÌÍÎÏÒÓÔÖÙÚa-zàáâäçèéêëîïôöùúûüÿ])|$))'
        elif '\...' in punct_forte_selec and '\.' not in punct_forte_selec:
            punct_forte_selec.remove('\...')
            segmenteur = ''.join(punct_forte_selec)
            regex_split_sents = r'\s*(\S.{1,}?(?:[0-9a-zàáâäçèéêëîïôöùúûüÿ\»\)\]\s](?:['+segmenteur+r']|\.{3})\s?\»?\"?|$)(?=(?:\s+[&A-ZÀÁÂÄÇÈÉÊÌÍÎÏÒÓÔÖÙÚa-zàáâäçèéêëîïôöùúûüÿ])|$))'
        elif '\...' in punct_forte_selec and '\.' in punct_forte_selec and len(punct_forte_selec)>2:
            punct_forte_selec.remove('\...')
            segmenteur = ''.join(punct_forte_selec)
            regex_split_sents = r'\s*(\S.{1,}?(?:[0-9a-zàáâäçèéêëîïôöùúûüÿ\»\)\]\s\.](?:['+segmenteur+r']|\.)\s?\»?\"?|$)(?=(?:\s+[&A-ZÀÁÂÄÇÈÉÊÌÍÎÏÒÓÔÖÙÚa-zàáâäçèéêëîïôöùúûüÿ])|$))'
        elif '\...' not in punct_forte_selec:
            segmenteur = ''.join(punct_forte_selec)
            regex_split_sents = r'\s*(\S.{1,}?(?:[0-9a-zàáâäçèéêëîïôöùúûüÿ\»\)\]\s](?:['+segmenteur+r'])\s?\»?\"?|$)(?=(?:\s+[&A-ZÀÁÂÄÇÈÉÊÌÍÎÏÒÓÔÖÙÚa-zàáâäçèéêëîïôöùúûüÿ])|$))'
        else:
            segmenteur = ''.join(punct_forte_selec)
            regex_split_sents = r'\s*(\S.{1,}?(?:[0-9a-zàáâäçèéêëîïôöùúûüÿ\»\)\]\s\.](?:['+segmenteur+r"])\s?\»?\"?|$))(?=(?:\s+[&A-ZÀÁÂÄÇÈÉÊÌÍÎÏÒÓÔÖÙÚ]|$))"
    print(regex_split_sents) 
    
    # édition de la liste de travail avec la segmentation souhaitée (chapitre/paragraphe/phrase/token)  
    for i in file2:

        # gestion du niveau chapitre
        if i == '\n':
            continue

        # gestion du niveau paragraphe
        else:

            list_chap = []
            list_para = []
            
            if i.startswith('<head>'):
                list_para.append(i)
                print("head/ ", i)
            else:
                para = re.split(regex_split_sents, i)
                print("para: ", i)

                # gestion du niveau phrase
                for S in para:
                    sent_cnt+=1
                    if S == '\n' or S == '' or S == '\n.':
                        continue

                    # gestion du niveau token & tokenisation
                    sent = re.split('(?<=\s)|(?<=\')|(?<=’)|(?<= ́)|(?<=ʹ)|(?<=,)', S) # tokenisation de base (par espace, appos, virgule)
                    
                    if '' in sent:
                        sent.remove('')

                    #dev print(sent_cnt)
                    #dev print(sent)

                    for i, token in enumerate(sent):
                        sent[i] = token.rstrip(' ')

                    for id_token, token in enumerate(sent):
                        ## Tokenisation des ponctuations
                        # ciblage les tokens qui contiennent de la ponctuation 
                        var_id = sent.index(token)

                        if len(sent)==var_id+1:
                            if token.endswith('#1'):
                                token = re.sub("#1",".",token)
                        punct_token = [(token, punct) for punct in list_punct if token.endswith(punct)]

                        # TRES IMPORTANT permet d'éviter les nouveaux tokens de punctuation ajoutés
                        #  sinon ça boucle à l'infini car le token fini par une punct

                        if punct_token != []:
                            if token.startswith(punct_token[0][1]):
                                pass

                            elif re.match('([a-z]{1,2}\.)[;,:]?', punct_token[0][0]):

                                if token.endswith(tuple([";",",",":"])):
                                    if punct_token != []: 
                                        ntoken = token.rstrip(punct_token[0][1])
                                        sent[id_token] = ntoken
                                        if len(sent)==id_token+1:
                                            sent.append(punct_token[0][1])
                                        else:
                                            sent.insert(id_token+1, punct_token[0][1])

                                elif len(sent)==id_token+1:
                                    ntoken = sent[id_token].rstrip(sent[id_token][len(sent[id_token])-1])
                                    sent[id_token] = ntoken
                                    sent.append(token[len(token)-1])
                                else:
                                    pass

                            else:
                                if token in list_punct:             
                                    pass
                                elif punct_token != []: 
                                    ntoken = token.rstrip(punct_token[0][1])
                                    sent[id_token] = ntoken
                                    if len(sent)==id_token+1:
                                        sent.append(punct_token[0][1])
                                    else:
                                        sent.insert(id_token+1, punct_token[0][1])

                    for token in sent:
                        if '</hi>' in token:
                            id_token = sent.index(token)
                            processed_hi = []
                            # sub caractère spé
                            token = re.sub('\<\/hi\>', '', token)

                            if '<hi_rend="superscript">' in token:
                                processed_token = re.sub('\<hi_rend\=\"superscript\"\>', '', token)
                                processed_token = processed_token.split('_')
                                attrib = '@rend=superscript'
                                for part_hi in processed_token:
                                    #processed_hi.append(part_hi+attrib+'_'+part_hi[len(part_hi)-7])
                                    processed_hi.append(part_hi+attrib)

                            elif '<hi_rend="italic">' in token:
                                processed_token = re.sub('\<hi_rend\=\"italic\"\>', '', token)
                                processed_token = processed_token.split('_')
                                attrib = '@rend=italic'
                                for part_hi in processed_token:
                                    processed_hi.append(part_hi+attrib)

                            sent[id_token] = '_'.join(processed_hi)
                    
                    sent = "_".join(sent).split("_")

                    ### dev ########################################################################################################
                    # gestion des caractères spéciaux

                    '''            
                    # gestion des lettres "inversées" u,v & i,j            
                    for token in sent:   
                        if token[0] not in dict_PRESTO.keys(): # test si le token est dans la liste presto
                            for letter in list_substitution:
                                if letter[0] in token:
                                    sub_token = re.sub(r''+re.escape(letter[0])+'', ''+re.escape(letter[1])+'', token[0])
                                    if sub_token in dict_PRESTO.keys():
                                        #token = letter + "\'" + x
                                        sent[sent.index(token)] = [sub_token, token[1]]
                                        print('£££')
                                        #écriture 
                                        print(subtoken)
                                        print(token)


                    for token in sent:
                        if "#1" in token[0] and "#1" in token[1]:
                            sent[sent.index(token)] = [re.sub(r"#1","\'",token[0]), re.sub(r"#1","\'",token[1])]

                        if "#2" in token[0] and "#2" in token[1]:
                            sent[sent.index(token)] = [re.sub(r"#2","\-",token[0]), re.sub(r"#2","\-",token[1])]

                        # v en u
                        # u en v
                        # i en j
                        # j en i

                    ################################################################################################################
                    '''

                    #dev print(sent)
                    for token in sent:
                        if "#1" in token:
                            sent[sent.index(token)] = re.sub(r"#1",".",token)
                        if "#2" in token:
                            sent[sent.index(token)] = re.sub(r"#2",".",token)
                        if "#3" in token:
                            sent[sent.index(token)] = re.sub(r"#3",".",token)
                        '''
                        if "#2" in token:
                            sent[sent.index(token)] = re.sub(r"#2","[...]",token)
                        '''
                    '''
                    for token in sent:
                        if "#1" in token:
                            sent[sent.index(token)] = re.sub(r"#1","[?]",token)    
                        if "#2" in token:
                            sent[sent.index(token)] = re.sub(r"#2","[...?]",token)
                        if "#3" in token:
                            sent[sent.index(token)] = re.sub(r"#3","[??]",token)
                        if "#4" in token:
                            sent[sent.index(token)] = re.sub(r"#4","[--]",token)
                    '''    

                    for token in sent:
                        sent[sent.index(token)] = token.rstrip(" ")

                        if token == '' :
                            sent.remove(token)

                    #dev print(sent)
                    #dev print('')
                    #sent = [i for i in sent if i != ('','')] #suppression des vides 

                    list_para.append(sent)

            corpus.append(list_para)
    
    # écriture du xml à partir de la liste de travail
    ID_chap = 0
    with open(cible, "w", encoding="utf-8") as out:
        out.write('<body>\n')
        ID_chap += 1
        ID_para = 0
        for para in corpus:
            if type(para) == list:
                if para==[]:
                    pass
                else:
                    ID_para += 1
                    ID_sent = 0
                    if type(para[0])==str:
                        if para[0].startswith('<head>'):

                            para[0] = para[0].replace('#1', '.')
                            out.write(para[0])
                            ID_para -= 1
                    else:
                        out.write('<p n="' + str(ID_para) + '">\n')
                        for sent in para:

                            ID_sent += 1                        
                            out.write('<s n="' + str(ID_sent) + '">\n')
                            ID_token = 0
                            for token in sent:

                                if '&' in token:
                                    token = [re.sub(r"&","&amp;",token_) for token_ in token][0]

                                if '<choice' in token:
                                    token = re.sub(r"%"," ",token)

                                if '<hi' in token:
                                    token = re.sub(r"%"," ",token)

                                #dev print(token)
                                ID_token += 1
                                out.write('<w n="' + str(ID_token) + '">')
                                out.write(token)
                                out.write('</w>\n')
                            out.write('</s>\n')
                        out.write('</p>\n')
        out.write('</body>\n')

    tree = ET.parse(open(cible, encoding='utf-8'))
    root = tree.getroot()
    
    root = build_div(root, 'section')
    root = build_div(root, 'chapter')
    root = build_div(root, 'book')
    indent(root)
    ET.ElementTree(root).write(cible, encoding="utf-8")

    label_close.pack()
    bouton_option_len.pack()
    bouton_stats.pack()
    bouton_extract_lg_sents.pack()


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

fenetre = customtkinter.CTk()

fenetre.title("Text to XML")
fenetre.geometry("1080x480")
fenetre.minsize(480, 360)

label_title = customtkinter.CTkLabel(master=fenetre, text="Convert your .txt file into .xml")
label_title.pack(side="top")

frame = customtkinter.CTkFrame(master=fenetre)
frame.pack(expand=YES)

upload_insert_frame = customtkinter.CTkFrame(master=frame)
upload_insert_frame.pack()

width = 400
height = 200

label_upload = customtkinter.CTkLabel(master=upload_insert_frame, text="Click on the Upload button to select your .txt file")
label_upload.pack()

bouton_upload = customtkinter.CTkButton(master=upload_insert_frame, text="UPLOAD", command=browseFile)
bouton_upload.pack()

download_insert_frame = customtkinter.CTkFrame(master=frame)

label_download = customtkinter.CTkLabel(master=download_insert_frame, 
                        text="Click on the Download button to process your .txt file.")
label_download2 = customtkinter.CTkLabel(master=download_insert_frame, 
                        text="By default, sentences will be segmented by full stop;\n alternatively, you can define strong punctuation marks for sentence segmentation\nby clicking on the button below.")

bouton_option_punct = customtkinter.CTkButton(master=download_insert_frame, text="Define punctuation settings", command=onClick_punct)

bouton_download = customtkinter.CTkButton(master=download_insert_frame, text="DOWNLOAD", command=saveFile)

label_close = customtkinter.CTkLabel(master=download_insert_frame,
                    text="The conversion is complete.\nYou can close the window or convert another file.\nYou can extract stats on sentence length that will appear in the command line and/or download a text file\ncontaining information on the length of individual sentences, with sentences considered too long indicated.\nBy default, a sentence above 80 tokens is considered too long,\nbut you can change the number of tokens by clicking on the button below.")

bouton_option_len = customtkinter.CTkButton(master=download_insert_frame, text='Define "too-long" sentence', command=len_settings)

bouton_stats = customtkinter.CTkButton(master=download_insert_frame, text="EXTRACT STATS", command=extract_stats)

bouton_extract_lg_sents = customtkinter.CTkButton(master=download_insert_frame, text="DOWNLOAD TEXT FILE WITH SENTENCES LENGTH", command=extract_lg_sents)

label_txt_file_downloaded = customtkinter.CTkLabel(master=download_insert_frame, text="Text file downloaded")

fenetre.mainloop()

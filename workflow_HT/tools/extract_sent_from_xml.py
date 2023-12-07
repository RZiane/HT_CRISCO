import sys
from lxml import etree as ET
from utils import def_args, indent_xml, add_sent_id
import statistics

global ns_map
ns_map = {'tei': 'http://www.tei-c.org/ns/1.0'}
   
def extract_lg(inputfile, outputfile):

    tree = ET.parse(open(inputfile, encoding='utf-8'))
        
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
        
        if len_sent > 80:
            x = str(nb_sent)+' \ len: '+str(len_sent)+' \ Long= Yes \ '+'sent_id='+sent.attrib['sent_id']+'\n'+' '.join(text_sent)
            list_sents.append(x)
        else:
            x = str(nb_sent)+' \ len: '+str(len_sent)+'\n'+' '.join(text_sent)
            list_sents.append(x)                
        
    outputfile_txt = outputfile.rstrip('.xml')+'.txt'

    with open(outputfile_txt, "w", encoding="utf-8") as out:
        for i in list_sents:
            out.write(i)
            out.write('\n')
            out.write('\n')

def sort_by_length(sent):
    return int(sent.get('len', 0))

def order_sent_size(inputfile, outputfile):

    add_sent_id(inputfile, inputfile)

    tree = ET.parse(open(inputfile, encoding='utf-8'))    

    text = ET.Element('text')
    group_1 = ET.Element('group', n='1')
    group_2 = ET.Element('group', n='2')
    group_3 = ET.Element('group', n='3')
    group_4 = ET.Element('group', n='4')
    group_5 = ET.Element('group', n='5')
    group_6 = ET.Element('group', n='6')
    group_7 = ET.Element('group', n='7')
    group_8 = ET.Element('group', n='8')
    group_9 = ET.Element('group', n='9')
    group_10 = ET.Element('group', n='10')
    group_11 = ET.Element('group', n='11')

    for sent in tree.findall('.//s'):
        len_sent = 0
        for w in sent.findall('.//w'):
            len_sent += 1
        
        sent.set('len', str(len(sent)))

        if len_sent < 10:
            group_1.append(sent)
            group_1[:] = sorted(group_1, key=sort_by_length)
        elif len_sent > 10 and len_sent < 20:
            group_2.append(sent)
            group_2[:] = sorted(group_2, key=sort_by_length)
        elif len_sent > 20 and len_sent < 30:
            group_3.append(sent)
            group_3[:] = sorted(group_3, key=sort_by_length)
        elif len_sent > 30 and len_sent < 40:
            group_4.append(sent)
            group_4[:] = sorted(group_4, key=sort_by_length)
        elif len_sent > 40 and len_sent < 50:
            group_5.append(sent)
            group_5[:] = sorted(group_5, key=sort_by_length)
        elif len_sent > 50 and len_sent < 60:
            group_6.append(sent)
            group_6[:] = sorted(group_6, key=sort_by_length)
        elif len_sent > 60 and len_sent < 70:
            group_7.append(sent)
            group_7[:] = sorted(group_7, key=sort_by_length)
        elif len_sent > 70 and len_sent < 80:
            group_8.append(sent)
            group_8[:] = sorted(group_8, key=sort_by_length)
        elif len_sent > 80 and len_sent < 90:
            group_9.append(sent)
            group_9[:] = sorted(group_9, key=sort_by_length)
        elif len_sent > 90 and len_sent < 100:
            group_10.append(sent)
            group_10[:] = sorted(group_10, key=sort_by_length)
        elif len_sent > 100:
            group_11.append(sent)
            group_11[:] = sorted(group_11, key=sort_by_length)

    group_1.set('len', str(len(group_1)))
    text.append(group_1)

    group_2.set('len', str(len(group_2)))
    text.append(group_2)

    group_3.set('len', str(len(group_3)))
    text.append(group_3)

    group_4.set('len', str(len(group_4)))
    text.append(group_4)

    group_5.set('len', str(len(group_5)))
    text.append(group_5)

    group_6.set('len', str(len(group_6)))
    text.append(group_6)

    group_7.set('len', str(len(group_7)))
    text.append(group_7)

    group_8.set('len', str(len(group_8)))
    text.append(group_8)

    group_9.set('len', str(len(group_9)))
    text.append(group_9)

    group_10.set('len', str(len(group_10)))
    text.append(group_10)

    group_11.set('len', str(len(group_11)))
    text.append(group_11)

    # tree_out.append(text)
    indent_xml(text)
    ET.ElementTree(text).write(outputfile, pretty_print=True, encoding="utf-8")

def extract_stats(inputfile):
    
    tree = ET.parse(open(inputfile, encoding='utf-8'))
    
    list_len = []
    nb_sent = 0
    
    for sent in tree.findall('.//s'):
        len_sent = 0
        nb_sent += 1
        for w in sent.findall('.//w'):
            len_sent += 1
        
        if len_sent != 1:
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
            
    print('Nb_longs_sentences: '+ str(cnt_lg)+' / total : '+str(nb_sent)+' sentences' )
    #print("Après découpe au point-virgule dans les phrases trop longues: ")
    print("\ttotal mean: ", statistics.mean(list_len))
    print("\ttotal median: ", statistics.median(list_len))
    if cnt_lg != 0:    
        print("\ttoo long sentences mean: ", statistics.mean(list_len_lg))
        print("\ttoo long sentences median: ", statistics.median(list_len_lg))
        print("\tmax size long sentence: ", sorted(list_len_lg)[len(list_len_lg)-1])
    else:
        print('\tNo long sentences')

if __name__ == "__main__":
   inputfile, outputfile = def_args(sys.argv[1:])
   extract_lg(inputfile, outputfile)
   order_sent_size(inputfile, outputfile)
   extract_stats(inputfile)

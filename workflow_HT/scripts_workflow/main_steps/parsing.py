from tkinter import *
from tkinter import filedialog
from hopsparser import parser
import os
from tools.utils import conversion_xml2conllu, conversion_conllu2xml, synchronisation_xml

def parsefile(input_path, output_path, model_path):
    parser.parse(
            in_file=input_path,
            model_path=model_path,
            out_file=output_path
        )
    
def parse():
    try:
        temp_path
    except NameError:
        temp_path = []

    if temp_path != []:

        path = os.path.join(temp_path, 'temp_folder')
        try:
            os.makedirs(path)
        except:
            pass

        filename = input_path.split('/')[len(input_path.split('/'))-1].split('.')[0]

        input_conllu_tempfile = path+filename+'_input_temp.conllu'
        output_conllu_tempfile =  path+filename+'_output_temp.conllu'
        output_xml_tempfile =  path+filename+'_temp.xml'

        conversion_xml2conllu(input_path, input_conllu_tempfile)

        print('Parsing...')
        parsefile(input_conllu_tempfile, output_conllu_tempfile, model_path)
        print('Parsing done')
        conversion_conllu2xml(output_conllu_tempfile, output_xml_tempfile)

        synchronisation_xml(output_xml_tempfile, input_path, output_path)
        print('Conversion done')

    else:
        input_conllu_tempfile = input_path.rstrip('.xml')+'_input_temp.conllu'
        output_conllu_tempfile = input_path.rstrip('.xml')+'_output_temp.conllu'
        output_xml_tempfile = input_path.rstrip('.xml')+'_temp.conllu'
        conversion_xml2conllu(input_path, input_conllu_tempfile)

        print('Parsing...')
        parsefile(input_conllu_tempfile, output_conllu_tempfile, model_path)
        print('Parsing done')
        conversion_conllu2xml(output_conllu_tempfile, output_xml_tempfile)

        synchronisation_xml(output_xml_tempfile, input_path, output_path)
        print('Conversion done')
        
        os.remove(input_conllu_tempfile)
        os.remove(output_conllu_tempfile)
        os.remove(output_xml_tempfile)
        

def open_parsing():
    global fenetre_options_parsing
    fenetre_options_parsing = Toplevel()
    fenetre_options_parsing.title("Parsing settings")
    fenetre_options_parsing.geometry("240x120")
    fenetre_options_parsing.minsize(240, 120)
    fenetre_options_parsing.config(bg="white")

    bouton_path_temp = Button(fenetre_options_parsing, text="SELECT TEMP FILE FOLDER PATH",
                       command=browseTempFile, fg="#4065A4", bg="white")
    bouton_path_temp.pack()

    bouton_parse = Button(fenetre_options_parsing, text="PARSE",
                       command=parse, fg="#4065A4", bg="white")
    
    bouton_parse.pack()


def make_path(source):
    global source_path
    source_path = str(source)

    global dir_file
    dir_file = '/'.join(source.split('/')[:len(source.split('/'))-1])+'/'

    return source_path

def browseTempFile():
    global label_upload_temp
    try:
        label_upload_temp.destroy()
    except:
        pass

    source = filedialog.askdirectory(initialdir=dir_file)

    source_path = make_path(source)

    if source_path != '':
        var_msg = "This temporary files folder is selected:\n"+source_path+""
        
        label_upload_temp = Label(frame,
                            text=var_msg,                       
                            font=("Ubuntu", 10), fg="black", bg="white")

        label_upload_temp.pack()
    
    global temp_path
    temp_path = source_path

def browseFile_input():
    global label_upload_input
    try:
        label_upload_input.destroy()
    except:
        pass

    source = filedialog.askopenfilename(initialdir="/",
                                        title="Select a File",
                                        filetypes=[("eXtensible Markup Language","*.xml*")])
    source_path = make_path(source)

    if source_path != '':
        var_msg = "This file is uploaded:\n"+source_path+""

        label_upload_input = Label(frame,
                            text=var_msg,                       
                            font=("Ubuntu", 10), fg="black", bg="white")

        label_upload_input.pack()
    
    global input_path
    input_path = source_path

def browseFile_output():
    global label_upload_output
    try:
        label_upload_output.destroy()
    except:
        pass

    cible = filedialog.asksaveasfilename(initialdir=dir_file,
                                         title="Select a File",
                                         filetypes=[("eXtensible Markup Language","*.xml*")])
                                                     
    cible = cible.rstrip('.xml')+'.xml'

    cible_path = make_path(cible)

    if cible_path != '':
        var_msg = "Output file will save at:\n"+cible_path+""

        label_upload_output = Label(frame,
                            text=var_msg,                       
                            font=("Ubuntu", 10), fg="black", bg="white")

        label_upload_output.pack()
    
    global output_path
    output_path = cible_path

def browseFile_model():
    global label_upload_model
    try:
        label_upload_model.destroy()
    except:
        pass

    source = filedialog.askdirectory(initialdir="/")

    source_path = make_path(source)

    if source_path != '':
        var_msg = "This model is selected:\n"+source_path+""
        
        label_upload_model = Label(frame,
                            text=var_msg,                       
                            font=("Ubuntu", 10), fg="black", bg="white")

        label_upload_model.pack()
    
    global model_path
    model_path = source_path

fenetre = Tk()

fenetre.title("File parsing")
fenetre.geometry("1080x520")
fenetre.minsize(1080, 520)
fenetre.config(bg="white")

label_title = Label(fenetre, text="Add a syntactic analysis to your xml file",
                    font=("Ubuntu", 24), fg="black", bg="white")
label_title.pack(side="top")

frame = Frame(fenetre, bg="white")
frame.pack(expand=YES)

bouton_upload_inputfile = Button(frame, text="UPLOAD INPUT FILE",
                       command=browseFile_input, fg="#4065A4", bg="white")
bouton_upload_inputfile.pack()

bouton_upload_outputfile = Button(frame, text="UPLOAD OUTPUT FILE",
                       command=browseFile_output, fg="#4065A4", bg="white")
bouton_upload_outputfile.pack()

bouton_upload_modelpath = Button(frame, text="UPLOAD MODEL PATH",
                       command=browseFile_model, fg="#4065A4", bg="white")
bouton_upload_modelpath.pack()

bouton_open_parse = Button(frame, text="PARSE",
                       command=open_parsing, fg="#4065A4", bg="white")
bouton_open_parse.pack()

fenetre.mainloop()

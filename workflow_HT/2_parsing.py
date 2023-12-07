from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import time
from hopsparser import parser
import os
from tools.utils import conversion_xml2conllu, conversion_conllu2xml, synchronisation_xml, renum_xml, drop_head

def parsefile(input_path, output_path, model_path):
    parser.parse(
            in_file=input_path,
            model_path=model_path,
            out_file=output_path
        )
    
def parse(mode='parse'):
    pb.pack()
    for i in range(5):
        fenetre_options_parsing.update_idletasks()
        pb['value'] += 10
        time.sleep(1)

    try:
        if temp_path is not None:

            path = os.path.join(temp_path, 'temp_folder')

            os.makedirs(path, exist_ok=True)

            print(path)

            filename = input_path.split('/')[len(input_path.split('/'))-1].split('.')[0]

            input_conllu_tempfile = path+'/'+filename+'_input_temp.conllu'
            output_conllu_tempfile =  path+'/'+filename+'_output_temp.conllu'
            output_xml_tempfile =  path+'/'+filename+'_temp.xml'
            
            renum_xml(input_path, input_path)
            if mode == 'reparse':
                drop_head(input_path, input_path)

            conversion_xml2conllu(input_path, input_conllu_tempfile)

            print('Parsing...')
            parsefile(input_conllu_tempfile, output_conllu_tempfile, model_path)
            print('Parsing done')
            conversion_conllu2xml(output_conllu_tempfile, output_xml_tempfile)

            synchronisation_xml(output_xml_tempfile, input_path, output_path, mode)
            print('Conversion done')
            pb.destroy()

    except NameError:
        input_conllu_tempfile = input_path.rstrip('.xml')+'_input_temp.conllu'
        output_conllu_tempfile = input_path.rstrip('.xml')+'_output_temp.conllu'
        output_xml_tempfile = input_path.rstrip('.xml')+'_temp.conllu'

        renum_xml(input_path, input_path)
        if mode == 'reparse':
            drop_head(input_path, input_path)

        conversion_xml2conllu(input_path, input_conllu_tempfile)

        print('Parsing...')
        parsefile(input_conllu_tempfile, output_conllu_tempfile, model_path)
        print('Parsing done')
        conversion_conllu2xml(output_conllu_tempfile, output_xml_tempfile)

        synchronisation_xml(output_xml_tempfile, input_path, output_path, mode)
        print('Conversion done')
        pb.destroy()
        
        os.remove(input_conllu_tempfile)
        os.remove(output_conllu_tempfile)
        os.remove(output_xml_tempfile)
        
    fenetre_options_parsing.destroy()
        

def open_parsing():
    global fenetre_options_parsing
    fenetre_options_parsing = Toplevel()
    fenetre_options_parsing.title("Parsing settings")
    fenetre_options_parsing.geometry("240x120")
    fenetre_options_parsing.minsize(240, 120)
    fenetre_options_parsing.config(bg="white")

    # progressbar
    global pb
    pb = ttk.Progressbar(
        fenetre_options_parsing,
        orient='horizontal',
        mode='indeterminate',
        length=280
    )

    bouton_path_temp = Button(fenetre_options_parsing, text="SELECT TEMP FILE FOLDER PATH",
                       command=browseTempFile, fg="#4065A4", bg="white")
    bouton_path_temp.pack()

    bouton_parse = Button(fenetre_options_parsing, text="PARSE",
                       command=parse, fg="#4065A4", bg="white")
    
    bouton_parse.pack()
    

def make_path(source):
    global source_path
    source_path = str(source)

    return source_path

def browseFile_input():
    global label_upload_input
    try:
        label_upload_input.destroy()
        bouton_upload_outputfile.destroy()
    except:
        pass

    source = filedialog.askopenfilename(initialdir="/",
                                        title="Select an input file",
                                        filetypes=[("eXtensible Markup Language","*.xml*")])
    source_path = make_path(source)

    if source_path != '':
        var_msg = "This file is uploaded:\n"+source_path+""

        label_upload_input = Label(upload_frame,
                            text=var_msg,                       
                            font=("Ubuntu", 10), fg="black", bg="white")

        label_upload_input.pack()

        output_frame.pack()
        label_output.pack()

        bouton_upload_outputfile = Button(output_frame, text="UPLOAD OUTPUT FILE",
                       command=browseFile_output, fg="#4065A4", bg="white")
        bouton_upload_outputfile.pack()

    global input_path
    input_path = source_path

    global dir_file
    dir_file = '/'.join(source.split('/')[:len(source.split('/'))-1])+'/'

def browseFile_output():
    global label_upload_output
    try:
        label_upload_output.destroy()
        bouton_upload_modelpath.destroy()
    except:
        pass

    cible = filedialog.asksaveasfilename(initialdir=dir_file,
                                         title="Name your output file",
                                         filetypes=[("eXtensible Markup Language","*.xml*")])
                                                     
    cible = cible.rstrip('.xml')+'.xml'

    cible_path = make_path(cible)

    if cible_path != '':
        var_msg = "Output file will save at:\n"+cible_path+""

        label_upload_output = Label(output_frame,
                            text=var_msg,                       
                            font=("Ubuntu", 10), fg="black", bg="white")

        label_upload_output.pack()

        model_frame.pack()
        label_model.pack()
        bouton_upload_modelpath = Button(model_frame, text="UPLOAD MODEL PATH",
                       command=browseFile_model, fg="#4065A4", bg="white")
        bouton_upload_modelpath.pack()
    
    global output_path
    output_path = cible_path

def browseFile_model():
    global label_upload_model
    try:
        label_upload_model.destroy()
        bouton_open_parse.destroy()
    except:
        pass

    source = filedialog.askdirectory(initialdir="/",
                                    title="Select your model folder")

    source_path = make_path(source)

    if source_path != '':
        var_msg = "This model is selected:\n"+source_path+""
        
        label_upload_model = Label(model_frame,
                            text=var_msg,                       
                            font=("Ubuntu", 10), fg="black", bg="white")

        label_upload_model.pack()

        parse_frame.pack()
        label_parse.pack()

        bouton_open_parse = Button(parse_frame, text="PARSE",
                       command=open_parsing, fg="#4065A4", bg="white")
        bouton_open_parse.pack()
    
    global model_path
    model_path = source_path

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
        
        label_upload_temp = Label(parse_frame,
                            text=var_msg,                       
                            font=("Ubuntu", 10), fg="black", bg="white")

        label_upload_temp.pack()
    
    global temp_path
    temp_path = source_path

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

global upload_frame
upload_frame = Frame(frame, bg="white")
upload_frame.pack()

label_upload = Label(upload_frame, text="Click on the Upload button to select your .xml input file",
                   font=("Ubuntu", 18), fg="black", bg="white")
label_upload.pack()

bouton_upload_inputfile = Button(upload_frame, text="UPLOAD",
                       command=browseFile_input, fg="#4065A4", bg="white")
bouton_upload_inputfile.pack()

global output_frame
output_frame = Frame(frame, bg="white")

label_output = Label(output_frame, text="Click on the Output file button to name your output file",
                   font=("Ubuntu", 18), fg="black", bg="white")

global model_frame
model_frame = Frame(frame, bg="white")

label_model = Label(model_frame, text="Click on the Model selection button to select your model folder",
                   font=("Ubuntu", 18), fg="black", bg="white")

global parse_frame
parse_frame = Frame(frame, bg="white")

label_parse = Label(parse_frame, text="Click on the Parsing button to open the parsing window",
                   font=("Ubuntu", 18), fg="black", bg="white")

fenetre.mainloop()

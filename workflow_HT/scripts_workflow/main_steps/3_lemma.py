from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import time
from tools.utils import renum_xml, make_d_CorrTable, make_d_PRESTO
from lemmatisation import process_lemmatisation

import threading
    

def make_path(source):
    global source_path
    source_path = str(source)

    return source_path

def browseFile_input():
    global label_upload_input
    try:
        label_upload_input.destroy()
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
        '''
        model_frame.pack()
        label_model.pack()
        bouton_upload_modelpath = Button(model_frame, text="UPLOAD MODEL PATH",
                       command=browseFile_model, fg="#4065A4", bg="white")
        bouton_upload_modelpath.pack()
        '''
        lemmatisation_frame.pack()
        label_lemmatisation.pack()
        bouton_lemmatisation = Button(lemmatisation_frame, text="LEMMATISATION",
                       command=lemmatisation, fg="#4065A4", bg="white")

        bouton_lemmatisation.pack()

    global output_path
    output_path = cible_path

'''
def browseFile_model():
    global label_upload_model
    try:
        label_upload_model.destroy()
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
'''
def run_progressBar():
    global fenetre_loading
    fenetre_loading = Toplevel()
    fenetre_loading.title("Loading")
    fenetre_loading.geometry("240x120")
    fenetre_loading.minsize(240, 120)
    fenetre_loading.config(bg="white")
    
    # progressbar
    global pb
    pb = ttk.Progressbar(
        fenetre_loading,
        orient='horizontal',
        mode='indeterminate',
        length=280
    )

    pb.pack()
    for i in range(5):
        fenetre_loading.update_idletasks()
        pb['value'] += 10
        time.sleep(1)
    

def lemmatisation():

    path_PRESTO = "C:/Users/yagam/Desktop/crisco_ressources/dico_PRESTO_SIMPLE_08.03.23.dff"
    path_CorrTable = "C:/Users/yagam/Desktop/crisco_ressources/MICLE_CorrTable_27-02-23.csv"

    run_progressBar()
    pb.update_idletasks()
    #lemmatisation_frame.update_idletasks()
    print("Processing dictionnary...")
    d_CorrTable = make_d_CorrTable(path_CorrTable)
    d_PRESTO = make_d_PRESTO(path_PRESTO)
    print("Processing file...")
    process_lemmatisation(input_path, output_path, d_CorrTable, d_PRESTO)
    print('Lemmatisation done')

fenetre = Tk()

fenetre.title("File lemmatisation")
fenetre.geometry("1080x520")
fenetre.minsize(1080, 520)
fenetre.config(bg="white")

label_title = Label(fenetre, text="Lemmatize your xml file",
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
'''
global model_frame
model_frame = Frame(frame, bg="white")

label_model = Label(model_frame, text="Click on the Model selection button to select your model folder",
                   font=("Ubuntu", 18), fg="black", bg="white")
'''
global lemmatisation_frame
lemmatisation_frame= Frame(frame, bg="white")

label_lemmatisation = Label(lemmatisation_frame, text="Click on the following button to lemmatize your file",
                   font=("Ubuntu", 18), fg="black", bg="white")

#Code for multithreading
t1 = threading.Thread(target=lemmatisation)

fenetre.mainloop()

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
        
        dict_frame.pack()
        label_dict.pack()
        bouton_upload_dict = Button(dict_frame, text="BROWSE DICTIONNARY",
                       command=browseFile_dict, fg="#4065A4", bg="white")
        bouton_upload_dict.pack()
        
    global output_path
    output_path = cible_path


def browseFile_dict():
    global label_upload_dict
    try:
        label_upload_dict.destroy()
    except:
        pass

    source = filedialog.askopenfilename(initialdir="/",
                                        title="Select an dictionnary file")

    source_path = make_path(source)

    if source_path != '':
        var_msg = "This dictionnary is selected:\n"+source_path+""
        
        label_upload_dict = Label(dict_frame,
                            text=var_msg,                       
                            font=("Ubuntu", 10), fg="black", bg="white")

        label_upload_dict.pack()

        convTable_frame.pack()
        label_convTable.pack()

        bouton_upload_convTable = Button(convTable_frame, text="BROWSE CONVERSION TABLE",
                       command=browseFile_convTable, fg="#4065A4", bg="white")
        bouton_upload_convTable.pack()
    
    global dict_path
    dict_path = source_path

def browseFile_convTable():
    global label_upload_convTable
    try:
        label_upload_convTable.destroy()
    except:
        pass

    source = filedialog.askopenfilename(initialdir="/",
                                        title="Select an conversion table file")

    source_path = make_path(source)

    if source_path != '':
        var_msg = "This convertion table is selected:\n"+source_path+""
        
        label_upload_convTable = Label(convTable_frame,
                            text=var_msg,                       
                            font=("Ubuntu", 10), fg="black", bg="white")

        label_upload_convTable.pack()

        lemmatisation_frame.pack()
        label_lemmatisation.pack()
        bouton_lemmatisation = Button(lemmatisation_frame, text="LEMMATISATION",
                       command=lemmatisation, fg="#4065A4", bg="white")

        bouton_lemmatisation.pack()
    
    global convTable_path
    convTable_path = source_path

def update_progress(value):
    pb["value"] = value
    fenetre.update()

def run_progressBar():
    '''
    global fenetre_loading
    fenetre_loading = Toplevel()
    fenetre_loading.title("Loading")
    fenetre_loading.geometry("240x120")
    fenetre_loading.minsize(240, 120)
    fenetre_loading.config(bg="white")
    


    pb.pack()
    for i in range(5):
        fenetre_loading.update_idletasks()
        pb['value'] += 10
        time.sleep(1)
    '''
    
    # create a progress bar and start the animation
    pbar = ttk.Progressbar(lemmatisation_frame, orient='horizontal', length=300, mode='indeterminate')
    pbar.place(relx=0.5, rely=0.5, anchor='c')
    pbar.start()

    var = StringVar() # hold the result from Classifyall()
    # execute Classifyall() in a child thread
    threading.Thread(target=lemmatisation, args=(var,)).start()
    # wait for the child thread to complete
    #tx.wait_variable(var)
    fenetre.update()

    pbar.destroy()
    #tx.insert(END, var.get())
    

def lemmatisation():
    try:
        label_lemmatisation_done.destroy()
    except:
        pass
    #run_progressBar()
    #pb.update_idletasks()
    #lemmatisation_frame.update_idletasks()

    # progressbar
    global pb
    pb = ttk.Progressbar(
        lemmatisation_frame,
        orient='horizontal',
        mode='indeterminate',
        length=280
    )

    pb.pack()
    time.sleep(2)
    fenetre.update()

    update_progress(0)
    time.sleep(2)
    print("Processing dictionnary...")

    d_CorrTable = make_d_CorrTable(convTable_path)
    update_progress(30)
    time.sleep(2)

    d_PRESTO = make_d_PRESTO(dict_path)
    update_progress(60)
    time.sleep(2)

    print("Processing file...")
    process_lemmatisation(input_path, output_path, d_CorrTable, d_PRESTO)
    update_progress(100)

    print('Lemmatisation done')
    label_lemmatisation_done.pack()

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

global dict_frame
dict_frame = Frame(frame, bg="white")

label_dict = Label(dict_frame, text="Click on the following button to select your dictionnary file",
                   font=("Ubuntu", 18), fg="black", bg="white")

global convTable_frame
convTable_frame = Frame(frame, bg="white")

label_convTable = Label(convTable_frame, text="Click on the following button to select your convertion table file",
                   font=("Ubuntu", 18), fg="black", bg="white")

global lemmatisation_frame
lemmatisation_frame= Frame(frame, bg="white")

label_lemmatisation = Label(lemmatisation_frame, text="Click on the following button to lemmatize your file",
                   font=("Ubuntu", 18), fg="black", bg="white")

label_lemmatisation_done = Label(lemmatisation_frame, text="The lemmatisation is complete.\nYou can close the window or lemmatise another file.",
                   font=("Ubuntu", 18), fg="black", bg="white")

#Code for multithreading
#tx = threading.Thread(target=lemmatisation)

fenetre.mainloop()

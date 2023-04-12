from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import time
from tools.utils import make_d_CorrTable, make_d_PRESTO
from tools.conversion_Tagsets import process_conversion    

def make_path(source):
    global source_path
    source_path = str(source)

    return source_path

def browseFile_input():
    global label_upload_input
    global bouton_upload_outputfile
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
    global bouton_upload_dict
    try:
        label_upload_output.destroy()
        bouton_upload_dict.destroy()
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
    global bouton_upload_convTable
    try:
        label_upload_dict.destroy()
        bouton_upload_convTable.destroy()
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
    global bouton_convTagsets
    try:
        label_upload_convTable.destroy()
        bouton_convTagsets.destroy()
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

        convTagsets_frame.pack()
        label_convTagsets.pack()
        bouton_convTagsets = Button(convTagsets_frame, text="TAGSET CONVERSION",
                       command=convTagset, fg="#4065A4", bg="white")

        bouton_convTagsets.pack()
    
    global convTable_path
    convTable_path = source_path

def update_progress(value):
    pb["value"] = value
    fenetre.update()

def convTagset():
    try:
        label_convTagsets_done.destroy()
    except:
        pass

    # progressbar
    global pb
    pb = ttk.Progressbar(
        convTagsets_frame,
        orient='horizontal',
        mode='determinate',
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
    process_conversion(input_path, output_path, d_CorrTable, d_PRESTO)
    update_progress(100)

    print('ConvTagsets done')
    pb.destroy()

    label_convTagsets_done = Label(convTagsets_frame, text="The conversion is complete.\nYou can close the window or convert another file.",
                   font=("Ubuntu", 18), fg="black", bg="white")
    label_convTagsets_done.pack()

fenetre = Tk()

fenetre.title("File tagsets conversion")
fenetre.geometry("1080x520")
fenetre.minsize(1080, 520)
fenetre.config(bg="white")

label_title = Label(fenetre, text="Convert the tagset on your xml file",
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

global convTagsets_frame
convTagsets_frame= Frame(frame, bg="white")

label_convTagsets = Label(convTagsets_frame, text="Click on the following button to convert the tagset on your file",
                   font=("Ubuntu", 18), fg="black", bg="white")

fenetre.mainloop()

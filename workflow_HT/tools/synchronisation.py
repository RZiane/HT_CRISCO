import sys
from utils import def_args,synchronisation_xml
                
if __name__ == "__main__":
    inputfile, tempfile, outputfile = def_args(sys.argv[1:])
    synchronisation_xml('/home/ziane212/projects/data/crisco/terrien/temp_folder/1578_Terrien_convTagset_postprocess_temp.xml', 
                        '/home/ziane212/projects/data/crisco/terrien/1578_Terrien_convTagset_postprocess.xml', 
                        '/home/ziane212/projects/data/crisco/terrien/1578_Terrien_reparsed.xml',
                        'reparse')
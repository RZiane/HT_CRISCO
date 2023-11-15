import sys
from utils import def_args,synchronisation_xml
                
if __name__ == "__main__":
    # inputfile, tempfile, outputfile = def_args(sys.argv[1:])
    synchronisation_xml('/home/ziane212/Téléchargements/temp_folder/Rome_II_fr25_resolvAmbi_RevNR_temp.xml', 
                        '/home/ziane212/Téléchargements/Rome_II_fr25_resolvAmbi_RevNR.xml', 
                        '/home/ziane212/Téléchargements/temp_folder/Rome_II_fr25_reparsed.xml',
                        'reparse')
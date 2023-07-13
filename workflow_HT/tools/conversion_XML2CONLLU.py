import sys
from utils import def_args, conversion_xml2conllu
                
if __name__ == "__main__":
    inputfile, outputfile = def_args(sys.argv[1:])
    conversion_xml2conllu(inputfile, outputfile)
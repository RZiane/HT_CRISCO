import sys
from utils import def_args, conversion_xml2conllu_group
                
if __name__ == "__main__":
    inputfile, outputfile = def_args(sys.argv[1:])
    conversion_xml2conllu_group(inputfile, outputfile)
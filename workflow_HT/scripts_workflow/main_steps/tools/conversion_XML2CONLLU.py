import sys, getopt
from tools.utils import def_args
from tools.utils import conversion_xml2conllu
                
if __name__ == "__main__":
    inputfile, outputfile = def_args(sys.argv[1:])
    conversion_xml2conllu(inputfile, outputfile)
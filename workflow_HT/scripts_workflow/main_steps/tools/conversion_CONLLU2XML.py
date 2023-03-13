import sys, getopt
from utils import indent_xml
from utils import conversion_conllu2xml
from utils import def_args

if __name__ == "__main__":
    inputfile, outputfile = def_args(sys.argv[1:])
    conversion_conllu2xml(inputfile, outputfile)
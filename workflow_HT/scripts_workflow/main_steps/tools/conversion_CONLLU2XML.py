import sys, getopt
from tools.utils import indent_xml
from tools.utils import conversion_conllu2xml
from tools.utils import def_args

if __name__ == "__main__":
    inputfile, outputfile = def_args(sys.argv[1:])
    conversion_conllu2xml(inputfile, outputfile)
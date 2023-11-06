import sys
from utils import valid_xml, def_args

if __name__ == "__main__":
   inputfile, outputfile = def_args(sys.argv[1:])
   valid_xml(inputfile)
   

import sys
from utils import renum_xml,def_args
                
if __name__ == "__main__":
   inputfile, outputfile = def_args(sys.argv[1:])
   renum_xml(inputfile, outputfile)

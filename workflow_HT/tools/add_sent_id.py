import sys
from utils import add_sent_id,def_args
                
if __name__ == "__main__":
   inputfile, outputfile = def_args(sys.argv[1:])
   add_sent_id(inputfile, outputfile)

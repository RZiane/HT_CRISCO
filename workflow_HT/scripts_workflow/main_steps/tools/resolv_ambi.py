import sys, getopt
from utils import resolv_ambi
                
if __name__ == "__main__":
   inputfile, outputfile = def_args(sys.argv[1:])
   resolv_ambi(inputfile, outputfile)           
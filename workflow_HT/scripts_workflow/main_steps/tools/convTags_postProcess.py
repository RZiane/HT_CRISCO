import sys, getopt
from utils import resolv_ambi
from utils import convNoMatching
from utils import annotNPL
from utils import def_args

if __name__ == "__main__":
   inputfile, outputfile = def_args(sys.argv[1:])
   print('Post processing...')
   resolv_ambi(inputfile, outputfile)
   convNoMatching(outputfile, outputfile)   
   annotNPL(outputfile, outputfile)
   print('Post processing is done')       

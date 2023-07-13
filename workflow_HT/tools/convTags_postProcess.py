import sys
from utils import def_args, resolv_ambi,convNoMatching, annotNPL

if __name__ == "__main__":
   inputfile, outputfile = def_args(sys.argv[1:])
   print('Post processing...')
   resolv_ambi(inputfile, outputfile)
   convNoMatching(outputfile, outputfile)   
   annotNPL(outputfile, outputfile)
   print('Post processing is done')       

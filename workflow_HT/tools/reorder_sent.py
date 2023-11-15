import sys
from utils import def_args
from extract_sent_from_xml import order_sent_size
                
if __name__ == "__main__":
   inputfile, outputfile = def_args(sys.argv[1:])
   order_sent_size(inputfile, outputfile)

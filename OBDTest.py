import argparse
 
 
# Initialize parser
parser = argparse.ArgumentParser()
# Adding source argument
parser.add_argument("-s", "--Source", help = "[OBD, AssettoCorsa] Input data Source (Assetto Corsa Competizione also works)", default = "OBD")
# Read arguments from command line
args = parser.parse_args()
if args.Source:
    print("Mode: "+str(args.Source))
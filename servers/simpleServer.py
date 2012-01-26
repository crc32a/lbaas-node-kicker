from util import printf,fprintf
import util
import sys
import os


def usage(prog):
    printf("Usage is %s <imageId> <flavorId> <serverName> <skelPath>\n",prog)
    printf("\n")
    printf("Build a cloud server based on credentials supplited in the\n")
    printf("auth_headers.db. Use the getauth script to populate the\n")
    printf(".db file\n")

def buildServer(imageId,flavorId,name,skelPath):
    pass

if __name__ == "__main__":
    prog = os.path.basename(sys.argv[0])
    if len(sys.argv)<

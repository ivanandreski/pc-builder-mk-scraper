import sys
from setec import scrape

def anhoch():
    print("Anhoch")

def setec():
    scrape()

def ddstore():
    print("DDStore")

if __name__ == '__main__':
    try:
        globals()[sys.argv[1]]()
    except:
        print("Argument is invalid")
        print("Available arguments: anhoch, setec, ddstore")
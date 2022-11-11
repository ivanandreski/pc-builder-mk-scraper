import sys
from setec import setec_scrape
from ddstore import ddstore_scrape

def anhoch():
    print("Anhoch")

def setec():
    setec_scrape()

def ddstore():
    ddstore_scrape()

if __name__ == '__main__':
    try:
        globals()[sys.argv[1]]()
    except:
        print("Argument is invalid")
        print("Available arguments: anhoch, setec, ddstore")
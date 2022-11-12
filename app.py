import sys
from setec import setec_scrape
from ddstore import ddstore_scrape
from anhoch import anhoch_scrape

def anhoch():
    anhoch_scrape()

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
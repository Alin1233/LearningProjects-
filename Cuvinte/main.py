import requests
import pprint
from bs4 import BeautifulSoup
import sys
import time

def main():
    start = time.time()


    #optiunea de a printa cuvinte 
    if sys.argv[1] == "c":
        nrWords = sys.argv[2]
        i = 0
        while i < int(nrWords):
            cuvant = getWord()
            printWord(cuvant)
            i = i + 1

    #afiseaza timpul de executare
    end = time.time()
    end = end - start
    end = "{:.2f}".format(end)
    print("\n")
    print(f"Runtime of the program is {end}")
        

    

#cerere catre https://ro.wiktionary.org/ se cauta cuvand pana cand este de origine romana
def getWord():
    URL = 'https://ro.wiktionary.org/wiki/Special:Aleatoriu'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    while soup.find(id = 'română') == None:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
    return soup



#afiseaza cuvantu;
def printWord(cuvant):
    results = cuvant.find(id='firstHeading')
    print(" ",results.text.strip(),end = '')
    


if __name__ == "__main__":
    main()















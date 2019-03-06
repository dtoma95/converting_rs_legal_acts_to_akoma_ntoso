import io
import json
import os

metapodaci = io.open("../../scraping/test.txt", mode="r", encoding="utf-8")
lista = metapodaci.readlines()
#metapodaci.close()


fajlovi = os.listdir("../aktovi_html")

list2 = []
for fajl in fajlovi:
    raz = 9-len(fajl)
    #print(raz, "0"*raz+fajl)
    list2.append("0"*raz+fajl)
list2.sort()
print(len(list2))


parovi = io.open("../metadata.csv", mode="w", encoding="utf-8")
parovi.write(lista[0].strip()+"#filename\n")

lista = lista[1:]

for i in range(0, len(lista)):
    reci = lista[i].split("#")
    naziv = reci[0]
    vrsta = reci[4]
    fixname = list2[i]
    while fixname[0]=="0":
        fixname = fixname[1:]

    parovi.write(lista[i].strip() + "#"+fixname+"\n")

    continue
    f = io.open('../aktovi_html/' + fixname, mode="r", encoding="utf-8")
    stringo = f.read()
    f.close()

    if(vrsta == "Аутентично/Обавезно тумачење"):
        f = io.open('Аутентично-Обавезно тумачење/' + fixname, mode="w", encoding="utf-8")
        f.write(stringo)
        f.close()
    else:
        try:
            f = io.open(vrsta + '/' + fixname, mode="w", encoding="utf-8")
            f.write(stringo)
            f.close()
        except:
            print(vrsta)

parovi.close()
stani = ["1160.html", "1575.html", "908.html", "2348.html", "318.html", "3062.html"]


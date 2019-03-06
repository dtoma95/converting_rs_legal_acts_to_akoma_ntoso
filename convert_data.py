import io
import os
import xml.etree.ElementTree as ET

import preprocessing.remove_html
import preprocessing.init_akoma
import form_akoma.structure

from form_akoma.AkomaBuilder import AkomaBuilder
from reasoner.BasicReasoner import BasicReasoner

if __name__ == "__main__":
    nastavi = "2126.html"
    idemo = False
    stani = ["1160.html", "1575.html", "908.html", "2348.html", "318.html", "3062.html"]
    for fajl in os.listdir("data/aktovi_html"):
        if(fajl == nastavi):
            idemo=True
        if not idemo:
            continue
        if fajl in stani:
            continue
        print(fajl)
        stringo = preprocessing.remove_html.preprocessing("data/aktovi_html/"+fajl)
        akoma_root = preprocessing.init_akoma.init_xml("act")

        #break

        f = io.open('data/aktovi_raw/' +fajl, mode="w", encoding="utf-8")
        f.write(stringo)
        f.close()

        html_root = ET.fromstring("<article>" + stringo + "</article>")
        #form_akoma.structure.fill_body(akoma_root, html_root)

        builder = AkomaBuilder(akoma_root)
        reasoner = BasicReasoner(html_root, builder)
        reasoner.start()
        break
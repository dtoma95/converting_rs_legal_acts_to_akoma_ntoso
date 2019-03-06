import xml.etree.ElementTree as ET


def check_above(clan):
    clan.itersiblings(preceding=True)


def fill_body(akoma_root, html_root):
    current_clan = 1

    for paragraph in html_root:
        if(paragraph.text == None):
            continue
        if paragraph.text.strip() == "Члан " + str(current_clan) + ".":
            print(paragraph.text)
            current_clan+=1

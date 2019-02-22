import xml.etree.ElementTree as ET
import re

def trash(stringo):
    #tree = ET.parse('../aktovi/1.html')
    #print(stringo)
    stringo = close_html_token("meta", stringo)
    stringo = close_html_token("link", stringo)
    stringo = close_html_token("img", stringo)
    stringo = close_html_token_exact("col", stringo)
    stringo = add_fake_root_node(stringo)
    #print(stringo)
    root = ET.fromstring(stringo)

    #for child in root:
     #   print(child.tag, child.attrib)

def add_fake_root_node(stringo):
    return u"<article>" + stringo + u"</article>"

def close_html_token(token, stringo):
    m = re.search('(<'+token+')(.*?)(>)', stringo)
    if m:
        return stringo[:m.end()] + u"</"+token+">" + stringo[m.end():]
    return stringo


def close_html_token_exact(token, stringo):
    m = re.search('(<'+token+'>)', stringo)
    if m:
        return stringo[:m.end()] + u"</"+token+">" + stringo[m.end():]
    return stringo
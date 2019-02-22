import io
import re

def strip_html(stringo):
    shorter = 0
    for m in re.finditer('(<(.|\n)*?>)', stringo):
        #retval = "" + stringo
        if not exeption_tag(m.group()):
            stringo = stringo[:m.start()-shorter] + stringo[m.end()-shorter:]
            shorter +=m.end()-m.start()

    return stringo

def exeption_tag(substring):
    exepted_tag = ["table", "tbody", "tr", "td", "img"]
    for t in exepted_tag:
        if(re.match("<\/?"+t+"(.|\n)*?>", substring)!= None):
            return True
    return False


def preprocessing(filename):
    f = io.open(filename, mode="r", encoding="utf-8")
    #f = open(filename, "r")
    stringo = f.read()
    stringo = strip_html(stringo)
    return stringo


if __name__ == "__main__":
    for i in range(1, 200):
        print(i)
        stringo = preprocessing('../aktovi/' +str(i)+'.html')
        f = io.open('../aktovi_raw/' +str(i)+'.txt', mode="w", encoding="utf-8")
        f.write(stringo)
        f.close()
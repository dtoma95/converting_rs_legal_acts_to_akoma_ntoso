import xml.etree.ElementTree as ET
import io

SOURCE = "#somebody"#"#pravno-informacioni-sistem"
def identification(metadata):
	base = ET.Element("identification", {"source": SOURCE})
	base.append(frbrwork(metadata.date, metadata.version, metadata.author))
	base.append(frbrexpression(metadata.date, metadata.version, metadata.editor))
	base.append(frbrmanifestation(metadata.date, metadata.version, metadata.editor))

def frbrwork(date, version, author):
    base = ET.Element("FRBRWork")
    base.append(ET.Element("FRBRthis", {"value": "/rs/act/"+date+"/"+version+"/main"}))
    base.append(ET.Element("FRBRuri", {"value": "/rs/act/" + date + "/" + version}))
    base.append(ET.Element("FRBRdate", {"date": date, "name": "Generation"}))
    base.append(ET.Element("FRBRauthor", {"href": "#"+author, "as": "#author"}))
    base.append(ET.Element("FRBRcountry", {"value": "rs"}))
    return base


def frbrexpression(date, version, editor):
	base = ET.Element("FRBRExpression")

	base.append(ET.Element("FRBRthis", {"value": "/rs/act/" + date + "/" + version + +"/srp@/main"}))
	base.append(ET.Element("FRBRuri", {"value": "/rs/act/" + date + "/" + version+"srp@"}))
	base.append(ET.Element("FRBRdate", {"date": date, "name": "Generation"}))
	base.append(ET.Element("FRBRauthor", {"href": "#" + editor, "as": "#editor"}))
	base.append(ET.Element("FRBRlanguage", {"language": "srp"}))

	return base


def frbrmanifestation(date, version, editor):
	base = ET.Element("FRBRManifestation")

	base.append(ET.Element("FRBRthis", {"value": "/rs/act/" + date + "/" + version + +"/srp@/main.xml"}))
	base.append(ET.Element("FRBRuri", {"value": "/rs/act/" + date + "/" + version+"srp@.akn"}))
	base.append(ET.Element("FRBRdate", {"date": date, "name": "Generation"}))
	base.append(ET.Element("FRBRauthor", {"href": "#" + editor, "as": "#editor"}))
	base.append(ET.Element("FRBRformat", {"value": "xml"}))

	return base

def publication(date, journal, number):
	base = ET.Element("publication", {"date": date, "name": journal.lower(), "showAs": journal, "number": number})
	return base
"""
	[{"id": "vrsta", value: "Zakon"},
	{"id": "oblast", ...},
	{"id": "grupa", ...}
	]
"""
def clssification(clssifications):
	base = ET.Element("classification", {"source": SOURCE })
	for dict in clssifications:
		newk = ET.Element("keyword", {"id": dict["id"], "value": dict["value"].lower(), "showAs":dict["value"]})
		base.append(newk)
	return base
"""
	[{"id": "usvajanje", date: "2018-12-21"},
	{"id": "stupanje na snagu", date: "2018-12-21"},
	"id": "primena", date: "2018-12-21"},
	]
"""
def workflow(workflows):
	base = ET.Element("workflow", {"source": SOURCE })
	for dict in workflows:
		newk = ET.Element("step", {"id": dict["id"], "date": dict["date"]})
		base.append(newk)
	return base

class Metadata():
		"""
	    0 Назив прописа
		1 ELI
		2 Напомена издавача
		3 Додатне информације
		4 Врста прописа
		5 Доносилац
		6 Област
		7 Група
		8 Датум усвајања
		9 Гласило и датум објављивања
		10 Датум ступања на снагу основног текста
		11 Датум примене
		12 Правни претходник
		13 Издавач
		14 filename
		"""
	def __init__(self, list):
		self.act_name = list[0]
		self.eli = list[1]
		self.napomena_izdavaca = list[2]
		self.dodatne_informacije = list[3]
		self.vrsta_propisa = list[4]
		self.donosilac = list[5]
		self.oblast = list[6]
		self.grupa = list[7]
		self.datum_usvajanja = self.convert_date(list[8]) #datum
		self.glasilo_i_datum = list[9]
		self.datum_stupanja = self.convert_date(list[10]) #datum
		self.datum_primene = self.convert_date(list[11]) #datum
		self.pravni_prethodnik = list[12]
		self.izdavac = list[13]
		self.filename = list[14]

	def convert_date(self, date):
		if date == "":
			return ""
		els = date.split(".")
		return els[2]+"-"+els[1]+"-"+els[0]


PREFIX = "{http://www.akomantoso.org/2.0}"

def akoma_ntsoso_metadata(filename, akomaroot):
	meta = list(akomaroot)[0].find(PREFIX + "meta")
	csv = io.open("../metadata.csv", mode="w", encoding="utf-8")
	metainfo = None
	for line in csv.readlines():
		values = line.split("#")
		if filename == values[14]:
			metainfo = Metadata(values)

	meta.append(identification({"date": metainfo.datum_usvajanja, "version": "1", "author": "#somebody", "editor":"#somebody"}))
	meta.append(publication())
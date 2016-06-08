from lxml import etree
import mongodb

cont = 250001
col = mongodb.get_db("52.208.8.144", 8080, "ranking")
docs = []
print("parseando archivo3")
tree1 = etree.parse('Sabi_Export_3.xml')
root1 = tree1.getroot()
print("codigo listo")
for record in root1:
    for item in record:
        if item.get("field") == "NAME":
            docs.append({'_id':cont, 'Nombre': item.text})
            cont += 1
for i in range(0, len(docs)/1000):
    j = i*1000
    docs2 = docs[j:j+1000]
    col.insert(docs2)
print("finalizado parseo")


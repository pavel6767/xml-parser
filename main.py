"""
<ns:CabinClass
	- Type (Seat, Kitchen, Bathroom, etc)
    - <ns:RowInfo <ns:SeatInfo <ns:Features> text()
	- Seat id (17A, 18A)
    - <ns:RowInfo <ns:SeatInfo <ns:Summary SeatNumber
	- Seat price
    - <ns:RowInfo <ns:SeatInfo <ns:Service <ns:Fee Amount
	- Cabin class
    - <ns:RowInfo CabinType
	- Availability
    - <ns:RowInfo <ns:SeatInfo <ns:Summary AvailableInd
  - And any other properties you might find interesting or useful.
    -

CabinClass [0]
  RowInfo [2]
    SeatInfo [4]
    SeatInfo [4]
CabinClass [1]
  RowInfo [27] 7 - 39
    SeatInfo []
"""

from lxml import etree
import json

# result = []
# tree = etree.parse('OTA_AirSeatMapRS.xml')

# cabin = tree.xpath('//ns:CabinClass', namespaces={
#   'ns': 'http://www.opentravel.org/OTA/2003/05/common/'
#   })

# for c in cabin[0]:
#   print "---", etree.QName(c).localname, "---"
#   for c1 in c[0]:
#     print etree.QName(c1).localname

class ParseXML:
  def __init__(self, source, target):
    self.data = []
    self.source = source
    self.target = target

  def main(self):
    tree = etree.parse(self.source)
    # refactor to not hardcode ns string
    cabin = tree.xpath('//ns:CabinClass', namespaces={
      'ns': 'http://www.opentravel.org/OTA/2003/05/common/'
      })

    for cabinClass in cabin:
      new_cabin = []
      for row in cabinClass:
        new_row = {'cabinType': row.attrib['CabinType']}
        for e in row:
            if etree.QName(e).localname == 'Characteristics':
              print "\n", e.text ,"\n"
              new_row[]
            else:
              print e
        new_cabin.append(new_row)
      self.data.append(new_cabin)
    self.saveJson()

  def saveJson(self):
    with open(self.target, 'w') as outfile:
      json.dump(self.data, outfile)

parser = ParseXML('OTA_AirSeatMapRS.xml', 'OTA_AirSeatMapRS.json')
parser.main()

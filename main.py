"""
<ns:CabinClass
	[x] Type (Seat, Kitchen, Bathroom, etc)
    - <ns:RowInfo <ns:SeatInfo <ns:Features> text()
	[x] Seat id (17A, 18A)
    - <ns:RowInfo <ns:SeatInfo <ns:Summary SeatNumber
	[x] Seat price
    - <ns:RowInfo <ns:SeatInfo <ns:Service <ns:Fee Amount
	[x] Cabin class
    - <ns:RowInfo CabinType
	[x] Availability
    - <ns:RowInfo <ns:SeatInfo <ns:Summary AvailableInd
  - And any other properties you might find interesting or useful.
    -

"""

from lxml import etree
import json

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

    SEATS = {
      'Aisle': True,
      'Center': True,
      'Window': True
    }

    for cabinClass in cabin:
      new_cabin = []
      for row in cabinClass:
        new_row = {
          'cabinType': row.attrib['CabinType'],
          'seatLayout': cabinClass.attrib['Layout'],
          'seats': []}
        for e in row:
            if etree.QName(e).localname == 'Characteristics':
              new_row['rowType'] = e.text
            else:
              new_seat = {}
              for seat_child in e:
                if etree.QName(seat_child).localname == 'Summary':
                  new_seat['available'] = bool(seat_child.attrib['AvailableInd'] == 'true')
                  new_seat['seatId'] = seat_child.attrib['SeatNumber']
                elif etree.QName(seat_child).localname == 'Features':
                  if seat_child.text in SEATS.keys():
                    new_seat['position'] = seat_child.text
                elif etree.QName(seat_child).localname == 'Service':
                  new_seat['price'] = int(seat_child[0].attrib['Amount'])
              new_row['seats'].append(new_seat)
        new_cabin.append(new_row)
      self.data.append(new_cabin)
    self.saveJson()

  def saveJson(self):
    with open(self.target, 'w') as outfile:
      json.dump(self.data, outfile)

parser = ParseXML('OTA_AirSeatMapRS.xml', 'OTA_AirSeatMapRS.json')
parser.main()

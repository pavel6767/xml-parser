from lxml import etree
import json

class ParseXML:
  def __init__(self, source, target):
    self.data = {'cabins': {}}
    self.source = source
    self.target = target

  def main(self):
    tree = etree.parse(self.source)
    # TODO modularize this
    regexpNS = "http://exslt.org/regular-expressions"
    namespaces = {
    'ns': 'http://www.opentravel.org/OTA/2003/05/common/',
    're':regexpNS
    }


    cabins = tree.xpath('//ns:CabinClass',namespaces=namespaces)
    for cabin in cabins:
      # build cabin types
      cabinType = cabin.xpath('./ns:RowInfo[1]/@CabinType',namespaces=namespaces)[0]
      self.data['cabins'][cabinType] = {
        'layout': cabin.attrib['Layout'],
        'seats': []
      }

    # build seats
    seats = tree.xpath('//ns:SeatInfo',namespaces=namespaces)
    for seat in seats:
      summary = seat.xpath('./ns:Summary',namespaces=namespaces)

      # base info
      new_seat = {
        'exitRow': bool(seat.attrib['ExitRowInd'] == 'true'),
        'available': bool(seat.xpath('./ns:Summary/@AvailableInd',namespaces=namespaces)[0] == 'true'),
        'seatId': seat.xpath('./ns:Summary/@SeatNumber',namespaces=namespaces)[0]
      }

      # type
      seat_positions = ["Window", "Center", "Aisle"] # extract-var
      seatsRegex = "^"+'|'.join(seat_positions)+"$"
      query = "./ns:Features[re:test(text(), $seatsRegex)]/text()"
      seatType = seat.xpath(query, seatsRegex=seatsRegex,namespaces=namespaces)

      if seatType:
        new_seat['type'] = seatType[0]
      else:
        seatType = new_seat['type'] = seat.xpath('.//ns:Features/@extension',namespaces=namespaces)[0]


      # price
      price = seat.xpath('.//ns:Fee/@Amount',namespaces=namespaces)
      if price:
        new_seat['price'] = price[0]

      cabinType = seat.xpath('./parent::ns:RowInfo/@CabinType',namespaces=namespaces)[0]
      self.data['cabins'][cabinType]['seats'].append(new_seat)

    self.saveJson()

  def getPath(self,query):
    print "hi"

  def saveJson(self):
    with open(self.target, 'w') as outfile:
      json.dump(self.data, outfile)

parser = ParseXML('OTA_AirSeatMapRS.xml', 'xpath.json')
parser.main()
# TODO regex to get all namespaces
# config class for input

from lxml import etree
import json

class ParseXML:
  data = {'cabins': {}}

  def __init__(self, source, target, tagRef):
    self.tagRef = {
      'cabin': tagRef['cabin'],
      'row': tagRef['row'],
      'seat': tagRef['seat'],
      'seatSummary': tagRef['seatSummary'],
      'features': tagRef['features'],
      'fee': tagRef['fee']
    }
    self.tree = etree.parse(source)
    self.target = target
    self.namespaces = {
    'ns': 'http://www.opentravel.org/OTA/2003/05/common/',
    're': 'http://exslt.org/regular-expressions'
    }

  def main(self):
    self.buildCabins()
    self.buildSeats()
    self.saveJson()

  def buildCabins(self):
    cabins = self.getPath(self.tree,'//{self.tagRef[cabin]}'.format(**locals()))
    for cabin in cabins:
      # build cabin types
      cabinType = self.getPath(cabin,'./{self.tagRef[row]}[1]/@CabinType'.format(**locals()))[0]
      self.data['cabins'][cabinType] = {
        'layout': cabin.attrib['Layout'],
        'seats': []
      }

  def buildSeats(self):
    # build seats
    seats = self.getPath(self.tree,'//{self.tagRef[seat]}'.format(**locals()))
    for seat in seats:
      summary = self.getPath(seat,'./{self.tagRef[seatSummary]}'.format(**locals()))

      # base info
      new_seat = {
        'exitRow': bool(seat.attrib['ExitRowInd'] == 'true'),
        'available': bool(self.getPath(seat,'./{self.tagRef[seatSummary]}/@AvailableInd'.format(**locals()))[0] == 'true'),
        'seatId': self.getPath(seat,'./{self.tagRef[seatSummary]}/@SeatNumber'.format(**locals()))[0]
      }

      # type
      seat_positions = ["Window", "Center", "Aisle"]
      seatsRegex = "^"+'|'.join(seat_positions)+"$"
      query = "./{self.tagRef[features]}[re:test(text(), $regex)]/text()".format(**locals())
      seatType = self.getPath(seat,query, seatsRegex)

      if seatType:
        new_seat['type'] = seatType[0]
      else:
        new_seat['type'] = self.getPath(seat,'.//{self.tagRef[features]}/@extension'.format(**locals()))[0]

      # price
      price = self.getPath(seat,'.//{self.tagRef[fee]}/@Amount'.format(**locals()))
      if price:
        new_seat['price'] = price[0]

      cabinType = self.getPath(seat,'./parent::{self.tagRef[row]}/@CabinType'.format(**locals()))[0]
      self.data['cabins'][cabinType]['seats'].append(new_seat)

  def getPath(self,element,query, regex = None):
    return element.xpath(query, regex=regex,namespaces=self.namespaces)

  def saveJson(self):
    with open(self.target, 'w') as outfile:
      json.dump(self.data, outfile)



source = 'OTA_AirSeatMapRS.xml'
target = 'xpath.json'
tagRef = {
  'cabin': 'ns:CabinClass',
  'row': 'ns:RowInfo',
  'seat': 'ns:SeatInfo',
  'seatSummary': 'ns:Summary',
  'features': 'ns:Features',
  'fee': 'ns:Fee'
}

parser = ParseXML(source, target, tagRef)
parser.main()

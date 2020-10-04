from lxml import etree
import json
tagRef = {
  'cabin': 'ns:CabinClass'
}
class ParseXML:
  data = {'cabins': {}}

  def __init__(self, source, target):
    # self.tagRef = {
    #   'cabin': tagRef.cabin,

    # }
    self.tree = etree.parse(source)
    self.target = target
    self.namespaces = {
    'ns': 'http://www.opentravel.org/OTA/2003/05/common/',
    're': 'http://exslt.org/regular-expressions'
    }

  def main(self):
    self.buildCabins()
    self.buildSeats()
    print 'success'
    # self.saveJson()

  def buildCabins(self):
    # cabins = self.getPath(tree,'//{self.tagRef[cabin]}'.format(**locals()))
    cabins = self.getPath(self.tree,'//ns:CabinClass')
    for cabin in cabins:
      # build cabin types
      cabinType = self.getPath(cabin,'./ns:RowInfo[1]/@CabinType')[0]
      self.data['cabins'][cabinType] = {
        'layout': cabin.attrib['Layout'],
        'seats': []
      }
  def buildSeats(self):
    # build seats
    seats = self.getPath(self.tree,'//ns:SeatInfo')
    for seat in seats:
      summary = self.getPath(seat,'./ns:Summary')

      # base info
      new_seat = {
        'exitRow': bool(seat.attrib['ExitRowInd'] == 'true'),
        'available': bool(self.getPath(seat,'./ns:Summary/@AvailableInd')[0] == 'true'),
        'seatId': self.getPath(seat,'./ns:Summary/@SeatNumber')[0]
      }

      # type
      seat_positions = ["Window", "Center", "Aisle"]
      seatsRegex = "^"+'|'.join(seat_positions)+"$"
      query = "./ns:Features[re:test(text(), $regex)]/text()"
      seatType = self.getPath(seat,query, seatsRegex)

      if seatType:
        new_seat['type'] = seatType[0]
      else:
        new_seat['type'] = self.getPath(seat,'.//ns:Features/@extension')[0]

      # price
      price = self.getPath(seat,'.//ns:Fee/@Amount')
      if price:
        new_seat['price'] = price[0]

      cabinType = self.getPath(seat,'./parent::ns:RowInfo/@CabinType')[0]
      self.data['cabins'][cabinType]['seats'].append(new_seat)

  def getPath(self,element,query, regex = None):
    return element.xpath(query, regex=regex,namespaces=self.namespaces)

  def saveJson(self):
    with open(self.target, 'w') as outfile:
      json.dump(self.data, outfile)

parser = ParseXML('OTA_AirSeatMapRS.xml', 'xpath.json')
parser.main()
# TODO regex to get all namespaces
# config class for input

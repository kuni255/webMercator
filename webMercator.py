import math

class TwebMercator:

  def __init__(self, zoomID):
    # radius of WGS84/GRS80
    self.R = 63781370
    self.L = 2.0 * self.R * math.pi
    self.maxLat = 85.051128779807 / 180.0 * math.pi

    self.pxTileWidth = 256

    self.eachDirectionTileNum = -1;
    self.tileWidth = -1
    self.lenPerPx = -1;

    self.updatezoomID(zoomID)
  
  def updatezoomID(self, zoomID):
    self.zoomID = zoomID
    self.eachDirectionTileNum = 2**self.zoomID
    self.tileWidth = self.L / self.eachDirectionTileNum
    self.lenPerPx = self.tileWidth / self.pxTileWidth
  
  def latlng2xyOnMap(self, lat, lng):
    # radius of WGS84/GRS80
    lam0 = 0.0
    pi = math.pi
    
    # convert to radian
    lat = lat / 180.0 * pi
    lng = lng / 180.0 * pi
    
    x = self.R * (lng - lam0) + self.L/2.0
    y0 = self.L/4.0 - ( self.R * math.log(math.tan( pi / 4.0 + self.maxLat / 2.0 )) )
    y  = self.L/4.0 - ( self.R * math.log(math.tan( pi / 4.0 + lat    / 2.0 )) )
    y = y - y0
  
    return x,y
  
  def getTileNum(self, x, y):
    xTileNum = x // self.tileWidth
    yTileNum = y // self.tileWidth
    return int(xTileNum), int(yTileNum)
  
  def xy2pxpyInTile(self, x, y):
    xTileNum, yTileNum = self.getTileNum(x, y)
    xInTile = x - xTileNum * self.tileWidth
    yInTile = y - yTileNum * self.tileWidth
    px = int(xInTile // self.lenPerPx)
    py = int(yInTile // self.lenPerPx)
    return px, py

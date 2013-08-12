import math

# radius of WGS84/GRS80
R = 63781370
L = 2.0 * R * math.pi
maxLat = 85.051128779807 / 180.0 * math.pi 

def latlng2xyOnMap(lat, lng):
  # radius of WGS84/GRS80
  lam0 = 0.0
  pi = math.pi
  
  # convert to radian
  lat = lat / 180.0 * pi
  lng = lng / 180.0 * pi
  
  x = R * (lng - lam0) + L/2.0
  y0 = L/4.0 - ( R * math.log(math.tan( pi / 4.0 + maxLat / 2.0 )) )
  y  = L/4.0 - ( R * math.log(math.tan( pi / 4.0 + lat    / 2.0 )) )
  y = y - y0

  return x,y

def getTileNum(zoomID, x, y):
  eachDirectionTileNum = 2**zoomID
  tileWidth = L / eachDirectionTileNum
  xTileNum = x // tileWidth
  yTileNum = y // tileWidth
  return xTileNum, yTileNum

Web Mercator
==================
 
These are routines about Web Mercator.
These routines provide way for getting
satellite image where nourth and east area.

DESCRIPTION
-----------
These are routines about Web Mercator
familiar with cyberjapandata.gsi.jp.
You can get a satellite image where 
north and east area by using these 
routines which requests images to 
cyberjapandata.jsi.jp.

HOW TO USE
-----------
Getting python code by  

      git clone https://github.com/kuni255/webMercator.git  

And getting satellite image by  

    python satelliteImage.py --NW latSW,lngNW --SE latSE,lngSE -o out.jpg
You can get image by specifying 2 points (North-West, Sourth-East) position 
of rectangular area you want.
Ex.  

    python satelliteImage.py --NW 35.581101,139.657319 --SE 35.573484,139.668739 -o out.jpg

If you want to know how to use the module, you should reference sample.py.
Or you can run following.  

    python sample.py

And, You can get map by changing attributes. For more information,
Please reference a following document.
http://portal.cyberjapan.jp/portalsite/docs/data/26Jul2012_haikei.pdf

REQUIREMENT
-----------
These routines require following modules.
* request
* Image

SEE ALSO
--------
http://portal.cyberjapan.jp/portalsite/kiyaku/index.html

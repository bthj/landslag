# coding=ISO-8859-1

## Copyright (c) 2008, Kapil Thangavelu <kapil.foss@gmail.com>
## All rights reserved.

## Redistribution and  use in  source and binary  forms, with  or without
## modification, are permitted provided that the following conditions are
## met:

## Redistributions of source code must retain the above copyright
## notice, this list of conditions and the following disclaimer.
## Redistributions in binary form must reproduce the above copyright
## notice, this list of conditions and the following disclaimer in the
## documentation and/or other materials provided with the
## distribution. The names of its authors/contributors may be used to
## endorse or promote products derived from this software without
## specific prior written permission.

## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
## FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
## COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
## INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
## (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
## SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
## HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
## STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
## ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
## OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Implements a Deep Zoom / Seadragon Composer in Python

For use with the seajax viewer

reversed from the excellent blog description at

 http://gashi.ch/blog/inside-deep-zoom-2 
 from Daniel Gasienica

incidentally he's got an updated version of this script that supports collections
thats included in the openzoom project

http://code.google.com/p/open-zoom/source/browse/trunk/src/main/python/deepzoom/deepzoom.py
 
Author: Kapil Thangavelu
Date: 11/29/2008
License: BSD

Modified by bthj.is to handle glob patterns and to create thumb and medium sized previews
http://code.google.com/p/landslag/source/browse/trunk/landslag/src/alaska/tileCutter/seadragon.py
"""

import math, os, optparse, sys, glob, logging
from PIL import Image

xml_template = '''\
<?xml version="1.0" encoding="UTF-8"?>
<Image TileSize="%(tile_size)s" Overlap="%(overlap)s" Format="%(format)s"
       xmlns="http://schemas.microsoft.com/deepzoom/2008">
       <Size Width="%(width)s" Height="%(height)s"/>
</Image>       
'''

html_template = '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>

<head>
<title>Seadragon Ajax</title>
<script type="text/javascript" src="http://seadragon.com/ajax/0.8/seadragon-min.js"></script>           
<script type="text/javascript">
    var viewer = null;
    function init() {
        viewer = new Seadragon.Viewer("container");
        viewer.openDzi("generated_images/%(name)s.dzi");
    }
    Seadragon.Utils.addEvent(window, "load", init);
</script>
<style type="text/css">
body {
    margin: 0px;
}
#container {
    width: 800px;
    height: 600px;
    background-color: Black;
}
a {
    font-family: Verdana;
    font-size: small;
    text-decoration: none;
    background-color: #F0F0F0;
    line-height: 24px;
    color: #253649;
}
.style1 {
    background-color: #FAF8B6;
}
.style2 {
    font-size: small;
    font-family: Verdana;
}
.style3 {
    border: 1px solid #F5F270;
}
.style4 {
    color: #444304;
    background-color: #F5F270;
}
</style>
</head>

<body>
<span style="font-size: large; font-family: Verdana; background-color: #F0F0F0;">%(name)s</span>

<div id="container">
</div>
<ul>
    <li>
        Til að súmma:
        <ul>
            <li>smella á ( + ) ( - ) takkana</li>
            <li>smella og shift-smella á myndflötinn</li>
            <li>snúa músarhjólinu með bendilinn yfir myndinni</li>
        </ul>
    </li>
    <li>Þriðji hnappurinn (mynd af húsi) birtir heildarmyndina (þægilegt þegar komið í djúpt súmm)</li>
    <li>Með fjórða hnappnum má fá myndina til að fylla út í gluggann.</li>
</ul>
</body>
</html>
'''

filter_map = {
    'cubic' : Image.CUBIC,
    'bilinear' : Image.BILINEAR,
    'bicubic' : Image.BICUBIC,
    'nearest' : Image.NEAREST,
    'antialias' : Image.ANTIALIAS,
    }


class PyramidComposer( object ):
    
    def __init__( self, image, tile_size=256.0, overlap=1, format="png", filter=None):

        self.image = image
        self.tile_size = tile_size
        self.overlap = overlap
        self.format = format
        self.width, self.height = self.image.size
        self._levels = None
        self.filter = filter

    @property
    def levels( self ):
        """ number of levels in an image pyramid """
        if self._levels is not None:
            return self._levels
        self._levels = int( math.ceil( math.log( max( (self.width, self.height) ), 2) ) )
        return self._levels

    def getLevelDimensions( self, level ):
        assert level <= self.levels and level >= 0, "Invalid Pyramid Level"
        scale = self.getLevelScale( level )
        return math.ceil( self.width * scale) , math.ceil( self.height * scale )

    def getLevelScale( self, level ):
        #print math.pow( 0.5, self.levels - level )
        return 1.0 / (1 << ( self.levels - level ) )

    def getLevelRowCol( self, level ):
        w, h = self.getLevelDimensions( level )
        return ( math.ceil( w / self.tile_size ),  math.ceil( h / self.tile_size )  )
    
    def getTileBox( self, level, column, row ):
        """ return a bounding box (x1,y1,x2,y2)"""
        # find start position for current tile
        
        # python's ternary operator doesn't like zero as true condition result
        # ie. True and 0 or 1 -> returns 1        
        if not column:
            px = 0
        else:
            px = self.tile_size * column - self.overlap
        if not row:
            py = 0
        else:
            py = self.tile_size * row - self.overlap

        # scaled dimensions for this level
        dsw, dsh = self.getLevelDimensions( level )
        
        # find the dimension of the tile, adjust for no overlap data on top and left edges
        sx = self.tile_size + ( column == 0 and 1 or 2 ) * self.overlap
        sy = self.tile_size + ( row == 0 and 1 or 2 ) * self.overlap
        
        # adjust size for single-tile levels where the image size is smaller
        # than the regular tile size, and for tiles on the bottom and right
        # edges that would exceed the image bounds        
        sx = min( sx, dsw-px )
        sy = min( sy, dsh-py )
        
        return px, py, px+sx, py+sy

    def getLevelImage( self, level ):

        w, h = self.getLevelDimensions( level )
        w, h = int(w), int(h)

        # don't transform to what we already have
        if self.width == w and self.height == h: 
            return self.image
        
        if not self.filter:
            return self.image.resize( (w,h) )
        return self.image.resize( (w,h), self.filter)
    
    
    def iterTiles( self, level ):
        col, row = self.getLevelRowCol( level )
        for w in range( 0, int( col ) ):
            for h in range( 0, int( row ) ):
                yield (w,h), ( self.getTileBox( level, w, h ) )

    def __len__( self ):
        return self.levels
    
    def save( self, parent_directory, name ):
        if not os.path.exists( os.path.join( parent_directory+"/generated_images", "%s.dzi"%(name)) ):
            ensure( os.path.join( ensure( expand( parent_directory ) ), "generated_images" ) )
            dir_path = ensure( os.path.join( ensure( expand( parent_directory ) ), "generated_images/%s_files"%name ) )
    
            # store images
            for n in range( self.levels + 1 ):
                level_dir = ensure( os.path.join( dir_path, str( n ) ) )
                level_image = self.getLevelImage( n )
                for ( col, row), box in self.iterTiles( n ):
                    tile = level_image.crop( map(int, box) )
                    tile_path = os.path.join( level_dir, "%s_%s.%s"%( col, row, self.format ) )
                    tile_file = open( tile_path, 'wb+')
                    tile.save( tile_file )
    
            # store dzi file
            fh = open( os.path.join( parent_directory+"/generated_images", "%s.dzi"%(name)), 'w+' )
            fh.write( xml_template%( self.__dict__ ) )
            fh.close()
            
            # write html file for preview
            fh = open( os.path.join( parent_directory, "%s.html"%(name)), 'w+' )
            fh.write( html_template%{'name':name} )
            fh.close()

    def info( self ):
        for n in range( self.levels +1 ):
            print "Level", n, self.getLevelDimensions( n ), self.getLevelScale( n ), self.getLevelRowCol( n )
            for (col, row ), box in self.iterTiles( n ):
                if n > self.levels*.75  and n < self.levels*.95:
                    print  "  ", "%s/%s_%s"%(n, col, row ), box 

class ImageResizer( object ):
    def __init__(self, img_size=128, format="jpg", filter=None):
        self.size = img_size, img_size
        self.format = format
        self.filter = filter
        
    def save( self, image, parent_directory, name ):
        self.dir_path = ensure( expand( parent_directory ) )
        image.thumbnail(self.size, Image.ANTIALIAS)
        image.save( os.path.join(self.dir_path, name) + ".jpg", "JPEG")
        
def expand( d):
    return os.path.abspath( os.path.expanduser( os.path.expandvars( d ) ) )

def ensure( d ):
    if not os.path.exists( d ):
        os.mkdir( d )
    return d

def main( ):
    parser = optparse.OptionParser(usage = "usage: %prog [options] filename")
    parser.add_option('-s', '--tile-size', dest = "size", type="int",
                      default=256, help = 'The tile height/width')
    parser.add_option('-q', '--quality', dest="quality", type="int",
                      help = 'Set the quality level of the image')
    parser.add_option('-f', '--format', dest="format",
                      default="jpg", help = 'Set the Image Format (jpg or png)')
#    parser.add_option('-n', '--name', dest="name", help = 'Set the name of the output directory/dzi')
    parser.add_option('-p', '--path', dest="path", help = 'Set the path of the output directory/dzi')
    parser.add_option('-t', '--transform', dest="transform", default="antialias",
                      help = 'Type of Transform (bicubic, nearest, antialias, bilinear')
    parser.add_option('-d', '--debug', dest="debug", action="store_true", default=False,
                      help = 'Output debug information relating to box makeup')
    parser.add_option('-g', '--glob', dest='glob', action='store_true', default=False, 
                      help = 'glob the given file path')
    parser.add_option('-m', '--mode', dest="mode", default=False, 
                      help = "Specify what type of image to render: thumb, medium or dzi - all types are renderd if mode is not given.")

    (options, args ) = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)
    image_path = expand( args[0] )
    
    
    
    if options.glob:
        if len( glob.glob(image_path) ) < 1:
            print  "No files found that match the given pattern", image_path
            sys.exit(1)
        else:
            image_paths = glob.glob(image_path)
    else:
        if not os.path.exists( image_path ):
            print  "Invalid File", image_path
            sys.exit(1)
        else:
            image_paths = [image_path]
        
    if options.transform and options.transform in filter_map:
        options.transform = filter_map[ options.transform ]

    if not options.path:
        options.path = os.path.dirname( image_paths[0] )
    ensure( options.path )        

    LOG_FILENAME = options.path+'/error.log'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)
    
    thumb = ImageResizer( img_size=128, format=options.format, filter=options.transform )
    medium = ImageResizer( img_size=512, format=options.format, filter=options.transform )
    for img_path in image_paths:
        try:
            name = os.path.splitext( os.path.basename( img_path ) )[0]
            img = Image.open( img_path )
            composer = PyramidComposer( img, tile_size=options.size, format=options.format, filter=options.transform )
        
            if options.debug:
                composer.info()
                sys.exit()
        
            if options.mode:
                if options.mode == 'dzi':
                    composer.save( options.path+'/dzi', name )
                if options.mode == 'medium':
                    medium.save( img, options.path+'/medium', name )
                if options.mode == 'thumb':
                    thumb.save( img, options.path+'/thumb', name )
            else:
                composer.save( options.path+'/dzi', name )
                    
                medium.save( img, options.path+'/medium', name )
                
                thumb.save( img, options.path+'/thumb', name )
        except:
            logging.error('error processing ' + name)
    
if __name__ == '__main__':
    main()
    

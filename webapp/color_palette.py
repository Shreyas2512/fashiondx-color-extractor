import sys
sys.path.append('../core')
from fdx_color_extractor import FdxColorExtractor
from PIL import Image


class ColorPalette(object):
    """
    A wrapper class on top of FdxColorExtractor

    Methods
    -------
    save_palette() : creates and saves 60x30 images of given color
    """
    def __init__(self, image, swatch):
        """

        :param image: dictionary
            contains name of the image, path of the image on local disk
        :param swatch: boolean
            true indicates image is a swatch image
        """
        self.name = image['image_name']
        self.image_url = '.'.join(image['image_url'].split('.')[1:])
        self.colors = FdxColorExtractor(image['image_url'], swatch).extract().fdx_colors
        self.save_palette()

    def save_palette(self):
        for color in self.colors:
            color = color.__dict__
            rgb = color['rgb']
            im = Image.new("RGB", (60, 30), color=(rgb[0], rgb[1],rgb[2]))
            im.save("./static/"+str(rgb[0])+"_"+str(rgb[1])+"_"+str(rgb[2])+".png")
            color['path'] = "/static/"+str(rgb[0])+"_"+str(rgb[1])+"_"+str(rgb[2])+".png"

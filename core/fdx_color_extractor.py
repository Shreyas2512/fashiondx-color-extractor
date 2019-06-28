from fdx_color import FdxColor
from colorthief import ColorThief
from algolia_color_extractor import ImageToColor
import numpy as np
import cv2, os


class FdxColorExtractor(object):
    """
    fdx color extractor main class
    methods
        extract()
            fills the fdx_colors array with FdxColor objects
        algolia()
            helper method for extract to get FdxColor object from algolia color extractor package
    """

    def __init__(self, image_path, is_swatch):
        """
            Parameters
            ----------
            image_path : str
                Path of the image
            is_swatch : boolean
                True indicates image is a swatch and vice versa
            fdx_colors : list of objects of type FdxColors
        """
        self.image_path = image_path
        self.is_swatch = is_swatch
        self.fdx_colors = []

    def extract(self):
        """
        If the image is swatch extract method uses colorthief and FdxColor to fill the fdx_colors
        else the  method uses algolia helper method to fill the fdx_colors list

        Returns
        -------
        self : FdxColorExtractorObject
        """
        if self.is_swatch:
            colors = ColorThief(self.image_path).get_palette(color_count=5, quality=1)
            for color in colors:
                self.fdx_colors.append(FdxColor(color['rgb'], color['pixel_percent']))
        else:
            colors = self.algolia()
            for color in colors:
                self.fdx_colors.append(FdxColor(color))
        return self

    def algolia(self):
        """
        Helper method to call algolia color extractor package to get rgb values of colors in the color palette

        Returns
        -------
        list of lists with each list containing r,g,b values for each color in color palette
        """
        img = cv2.imread(self.image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        npz = np.load('./color_names.npz')
        dominant_color = ImageToColor(
            npz['samples'],
            npz['labels'],
            settings={
                'selector': {'strategy': 'largest'},
                'cluster': {'min_k': 3, 'max_k': 10},
                'resize': {'crop': 0.85}
            }
        ).get(img)

        color_palette = ImageToColor(
            npz['samples'],
            npz['labels'],
            settings={
                'selector': {'strategy': 'ratio', 'ratio.threshold': 0.25},
                'cluster': {'min_k': 3, 'max_k': 10},
                'resize': {'crop': 0.85}
            }
        ).get(img)
        np.insert(color_palette, 0, dominant_color[0])
        return np.ndarray.tolist(color_palette)

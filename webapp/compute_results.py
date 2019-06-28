from color_palette import ColorPalette
from PIL import Image


def compute_results(images, swatch):
    """

    :param images: dictionary
        contains name and path of the image
    :param swatch: boolean

    :return: list
        list of of objects of type ColorPalette
    """
    results = []
    for image in images:
        results.append(ColorPalette(image, swatch).__dict__)
    return results
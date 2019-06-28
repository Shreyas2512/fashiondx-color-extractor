""" Takes rgb and pixel_percent and calculates hsl, tone, tags for saturation and lightness
"""


class FdxColor(object):
    """
        FdxColor class for calculating hsl values and hsl tags for each color having rgb value

        Methods
        -------
        get_tone(rgb) : calculates hue tag based on rgb values
        get_s_tag(rgb) : calculates saturation tag on rgb values
        get_l_tag(rgb) : calculates lightness tag based on rgb values
        rgb_to_hsl(rgb) : converts rgb values to hsl values
    """

    def __init__(self, rgb, pixel_percent=None):
        """

        :param rgb: list containing r,g,b values
        :param pixel_percent: percent of the total pixels in the image
        """
        self.rgb = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
        if pixel_percent:
            self.pixel_percent = round(pixel_percent, 2)
        else:
            self.pixel_percent = pixel_percent
        self.hsl = FdxColor.rgb_to_hsl(rgb)
        self.tone = FdxColor.get_tone(rgb)
        self.s_tag = FdxColor.get_s_tag(self.hsl[1])
        self.l_tag = FdxColor.get_l_tag(self.hsl[2])


    @staticmethod
    def get_tone(rgb):
        """

        :param rgb: tuple containing r,g,b values
        :return: str hue tag
        """
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        tone = None
        if r <= 10 and g <= 10 and b <= 10:
            tone = 'neutral_black'
        elif r >= 250 and g >= 250 and b >= 250:
            tone = 'neutral_white'
        elif abs(r - g) <= 10 and abs(g - b) <= 10 and abs(b - r) <= 10:
            tone = 'neutral_grey'
        elif r > g > b:
            tone = 'neutral_brown'
        elif r > g and r > b:
            tone = 'warm'
        elif (g > r and g > b) or (abs(r - g) <= 10 or abs(g - b) <= 10 or abs(b - r) <= 10):
            tone = 'medium_warm'
        elif b > r and b > g:
            tone = 'cool'
        return tone


    @staticmethod
    def get_s_tag(s):
        """

        :param s: int
            saturation value
        :return: str
            saturation tag
        """
        s_tag = None
        if s > 60:
            s_tag = "bright"
        elif 40 <= s <= 60:
            s_tag = "medium_bright"
        elif 25 <= s < 40:
            s_tag = "medium_muted"
        elif s < 25:
            s_tag = "muted"
        return s_tag


    @staticmethod
    def get_l_tag(l):
        """

        :param l: int
            lightness value  in hsl
        :return: str
            lightness tag
        """
        l_tag = None
        if l < 25:
            l_tag = "very_dark"
        elif 25 <= l < 40:
            l_tag = "dark"
        elif 40 <= l <= 60:
            l_tag = "medium_dark"
        elif 60 < l <= 75:
            l_tag = "light"
        elif l > 75:
            l_tag = "very_light"
        return l_tag



    @staticmethod
    def rgb_to_hsl(rgb):
        """

        :param rgb: tuple
            contains  r,g,b values
        :return: int,int, int
            returns hue, saturation, lightness values
        """
        r = (float(rgb[0])) / 255
        g = (float(rgb[1])) / 255
        b = (float(rgb[2])) / 255
        M = max(r, g, b)
        m = min(r, g, b)
        l = (M + m) / 2
        c = M - m
        h = 0
        if c == 0:
            h = 0
        elif r == M:
            h = ((g - b) / c) % 6
        elif g == M:
            h = ((b - r) / c) + 2
        else:
            h = ((r - g) / c) + 4
        h = h * 60
        s = 0
        if l != 1 and l != 0:
            s = c / (1 - abs((2 * l) - 1))
        return round(h), round(s * 100), round(l * 100)

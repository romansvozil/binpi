import binpi


class Pixel:
    red = binpi.UByte()
    green = binpi.UByte()
    blue = binpi.UByte()
    alpha = binpi.UByte()

    def __init__(self, red=0, green=0, blue=0, alpha=255):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha


class Image:
    width = binpi.UInt()
    height = binpi.UInt()
    pixels = binpi.List(Pixel, size=lambda i: i.width * i.height)
    # pixels = binpi.List(binpi.UByte(), size=lambda i: i.width * i.height * 4)  # 60* faster than the version with pixels

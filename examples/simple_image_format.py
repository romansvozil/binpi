import binpi


class Pixel:
    red = binpi.LEUByte()
    green = binpi.LEUByte()
    blue = binpi.LEUByte()
    alpha = binpi.LEUByte()

    def __init__(self, red=0, green=0, blue=0, alpha=255):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha


class Image:
    width = binpi.LEUInt()
    height = binpi.LEUInt()
    pixels = binpi.List(Pixel, size=lambda i: i.width * i.height)

from simple_image_format import *


if __name__ == "__main__":
    data = Image()
    data.width = 40
    data.height = 40
    data.image_type = ImageType.SomeType
    data.pixels = [Pixel(
        round((i % data.width) / data.width * 255),
        round((i % data.width) / data.width * 255),
        round((i % data.width) / data.width * 255),
    ) for i in range(data.width * data.height)]

    writer = binpi.FileWriter("../data/image.simple_image_format")
    binpi.serialize(data, writer=writer)

from simple_image_format import *

if __name__ == "__main__":
    reader = binpi.FileReader("../data/image.simple_image_format")
    data: Image = binpi.deserialize(Image, reader=reader)

    print(f"{data.width=}"
          f"{data.height=}"
          f"{data.image_type=}")

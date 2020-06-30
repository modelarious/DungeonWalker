from PIL import Image


# def crop(infile,height,width):
#     im = Image.open(infile)
#     imgwidth, imgheight = im.size
#     for i in range(imgheight//height):
#         for j in range(imgwidth//width):
#             box = (j*width, i*height, (j+1)*width, (i+1)*height)
#             yield im.crop(box)

def get_stairs_one(image):
    top = 387
    left = 13
    grid_size = 24
    return crop_square_image(image, top, left, grid_size)

def get_stairs_two(image):
    

def crop_square_image(im, top, left, grid_size):
    right = left + grid_size
    bottom = top + grid_size
    box = (left, top, right, bottom)
    return im.crop(box)

    

infile = "assets/tilesets/stairs.png"
with Image.open(infile) as i:
    stairs1 = get_stairs_one(i)
    stairs1.show()
from PIL import Image
import os

buffer = []

WIDTH = 128
HEIGHT = 64

outputString = "#include \"aniBuf.h\"\n\nconst unsigned char bufferAnimation["

def drawPixel(x, y, colour):
    global buffer
    byteNum = int((y*(WIDTH/8)) + int(x/8))
    # print(byteNum)
    bitNum = x % 8
    actualByte = buffer[byteNum]
    if (colour == 1):
        actualByte = actualByte | (1 << (7-bitNum))
    else:
        actualByte = actualByte & (~(1 << (7-bitNum)))

    buffer[byteNum] = actualByte


files = os.listdir("./frames")

outputString += str(len(files))

outputString += "][1024]={\n"

for file in files:
    outputString += "{"
    buffer = []
    for i in range(0, 1024):
        buffer.append(0)
    im = Image.open(os.path.join("./frames/", file))
    im = im.convert('RGBA')
    px = im.load()
    pix = list(im.getdata())

    for i in range(0, 64):
        for j in range(0, 64):
            #print("Orig ", str(i), " ", str(j))
            if (px[i, j][0] < 250 and px[i, j][1] < 250 and px[i, j][2] < 250):
                # ADJUST PARAMETERS BELOW FOR X AND Y OFFSET
                drawPixel(i + 32, j + 0, 1)

    for i in range(0, 1024):
        outputString += str(buffer[i])
        if (i != 1023):
            outputString += ", "
    outputString += "},\n"

outputString = outputString[:-1]  # remove comma from last one

outputString += "\n};"

f = open("./aniBuf.c", "w")
f.write(outputString)
f.close()

from PIL import Image
from PIL import GifImagePlugin
buffer = []

WIDTH = 128
HEIGHT = 64

fileName = "./fingerprint.gif"

outputString = "#include \""

outputString += fileName[2:-3]+"h"

outputString += "\"\n\nconst unsigned char bufferAnimation["


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


imageObject = Image.open(fileName)

print(imageObject.is_animated)
print(imageObject.n_frames)

outputString += str(imageObject.n_frames)


outputString += "][1024]={\n"

for frameNum in range(0, imageObject.n_frames):
    outputString += "{"
    buffer = []
    for i in range(0, 1024):
        buffer.append(0)
    imageObject.seek(frameNum)
    im = imageObject.convert('RGBA')
    # im.show()
    px = im.load()

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

f = open(fileName[:-3]+"c", "w")
f.write(outputString)
f.close()


hFileContent = "extern const unsigned char bufferAnimation ["
hFileContent += str(imageObject.n_frames)
hFileContent+="][1024];"

f=open(fileName[:-3]+"h", "w")
f.write(hFileContent)
f.close()


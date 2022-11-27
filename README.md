# OLED Animations With an ESP32 Using Arduino Core

## Examples
Examples taken from [lordicon.com](lordicon.com)

![Alarm Clock](https://raw.githubusercontent.com/A223D/oledAnimationsESP32Arduino/main/examples/myAlarm.gif)
![Book](https://github.com/A223D/oledAnimationsESP32Arduino/raw/main/examples/myBook.gif)![Confetti](https://github.com/A223D/oledAnimationsESP32Arduino/raw/main/examples/myConfetti.gif)
![Confetti](https://github.com/A223D/oledAnimationsESP32Arduino/raw/main/examples/myFingerprint.gif)
## Important Note
Due to the way the Arduino core and the Adafruit libraries work, all the animations will be slightly slower than their original counterparts. A way around this is speeding up the GIF using online utilities like [ezgif.com](https://ezgif.com/).

To make GIF run faster/at their original speed, [visit my other project on OLED animations using ESP-IDF](https://github.com/A223D/oledAnimationsESP-IDF).

## Introduction & Requirements
This project details how to create animations on OLED screens like SSD1306/SSD1315 etc. This project uses Adafruit's GFX libraries to abstract away the low-level display-specific processes as much as possible.

For a deep dive into SSD1306/SSD1315 low level functions, [visit my other project on OLED animations using ESP-IDF](https://github.com/A223D/oledAnimationsESP-IDF).

The requirements for this project are:
* An ESP32
> A basic Arduino (like Uno or Nano) would not be a good board to use, since animation frames require a large amount of storage space. For example, a 128x64 monochrome screen (like the SSD1306/SSD1315) contains 8192 pixels, which can be either white or black, and hence can be thought of as a bit(either 0 or 1). 8192 bits = 1024 bytes = 1 kiloByte per frame of animation. So a 30 frame long animation would take up 30 kB of space just to store. An Atmega328 based board like the Uno rev3 has 32kB of flash, which stores both your program and frames. A Nano 33 BLE will probably be fine though, since has 1MB of flash.

* An OLED screen for which an Adafruit Library exists. A commonly used OLED screen is the SSD1306. 
> Note: This project was built with a monochrome OLED display, but can be modified with some effort to support colour OLED displays.
* The Arduino IDE or some other equivalent setup(Platform IO etc.), with the following ESP32 board installed, along with the following libraries:
	* Adafruit GFX
	* Display-specific Adafruit library
* A basic understanding of the I2C protocol. [Here is a refresher](https://learn.sparkfun.com/tutorials/i2c/all), if required.
	* You must know the I2C address of your screen. If it is unknown, use the `WireScan`	example sketch to find it. `WireScan` can be found in File menu in Examples->Wire (under `Examples for the ESP32 Dev Module`). The default I2C pins for the ESP32 are:
	

	| Description   | Pin|
	| :-----------: | :-----------: |
	|SDA   					|    21    |
	| SCL   				| 22        |

> Warning: **Make sure to use 3.3v for I2C**
* A standard Python installation with Python Imaging Library installed
	* Can be done by executing the following command in your terminal equivalent: `pip3 install pillow`

## Project Goals & Architecture
We will be
1. Procuring gif files.
2. Splitting and saving frames as 2D arrays with Python.
3. Linking the file to our main sketch
4. Displaying these frames on the screen using Adafruit library functions.

## How to Use this Project

1. Download this repository, and place any new gif files in the same directory. 
> Make sure the Arduino IDE is closed, as it creates issues if a file is edited outside it. 
2. You will have to change the target gif in the `img2frames.py` script, and delete any previous `.c` or `.h` file, otherwise Arduino experiences issues. 
3. Run the `img2frames.py` script to create the new header file and file content all the frames as 2D arrays.
> Make sure there are no .c or .h files apart from the ones just created.
4. Open up the Arduino IDE, and change the 4rd `#include` directive to the .h file just created.
5. Running the Python script also outputs the number of frames in the GIF. Put this number in the condition part of the `for` loop in the Arduino sketch. If you  cannot find this number, it is also present in the .h file, beside 1024. 
6. Then you upload the sketch and reset the micro-controller if needed. 

## Required Theory
The Adafruit GFX function `drawBitmap` takes a an array of bytes, with each set bit representing a pixel which is on, and each clear bit representing a pixel which is off. 

Read more about it here: [AdafruitGFX Bitmaps](https://learn.adafruit.com/adafruit-gfx-graphics-library/graphics-primitives#bitmaps-2002806)

Each byte(or group of 8 pixels) is placed in order horizontally starting with the first row of pixels on the screen, till the each row is filled.

## Procuring and Preparing Animations
For the sake of this tutorial, we will be procuring animation from Lordicon.com, a provider of a useful variety of animated icons. 

1. Go to [lordicon.com](lordicon.com) and click `Explore library`. Select a category. For monochrome OLED displays, I would recommend the `Wired Outline`, `System Outline`, or `System Solid` collections, as they look the cleanest. 

2. Select `Free icons` to filter out the paid icons, select any one out of the free ones. Some animations have multiple colours, and motion types. Select your favourite one. 

> Since my display is monochrome, I have created my Python script(which converts the image frames to c-style 2D arrays) to replace all colours except white with the primary colour of my display(white). To clarify, any non-white colours in the image will show up as white on my screen, and any white colour in the image will be assumed to be background and show up as black on my screen. 

3. Click the green button with `GIF` in it to open a configuration box. Since the animation is square, and my screen size is 128x64, I'm going to resize to 64px. Resize according to your screen size.
> If you have a colour screen, you can adjust the colours of the animation as well by clicking the right-facing icon under the icon preview. The main thing to make sure of is that the final animation will fit on your screen.

4. Download the .gif file and save on it on your PC.

## Splitting and Saving Frames as C-style 2D Arrays

In this section, we will use a Python script to split the frames of our gif file and save them as 2 C-style 2D Arrays. 

The first part of the script:
```python
from PIL import Image
buffer = []

WIDTH = 128
HEIGHT = 64

fileName = "./alarm.gif"
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
```
This part initialize the buffer for a frame, declares variable for the width and height of the screen, declares the target gif file, and begins the .c file that will store all the frames. 

We also create the `drawPixel` function, which takes 0-indexed coordinates, and a colour(1 or 0), and sets or clears a bit accordingly. This is used to create a frame in the `buffer` list, which consists of 1024 bytes. We first find the byte number and bit number in the byte. Then that byte is read from the `buffer` list and the specific bit is cleared or set. Then the modified byte is places back into `buffer`. This function is used later on. 

After that, we open the gif file, check if it is animated, and print the number of frames. We add that to the output frame file, and start the 2D array.

The next part of the script is as follows:
```python
for  frameNum  in  range(0, imageObject.n_frames):
	outputString += "{"
	buffer = []
	for i in range(0, 1024):
		buffer.append(0)
	imageObject.seek(frameNum)
	im = imageObject.convert('RGBA')
	# im.show()
	px = im.load()
	for  i  in  range(0, 64):
		for  j  in  range(0, 64):
		#print("Orig ", str(i), " ", str(j))
			if (px[i, j][0] < 250  and  px[i, j][1] < 250  and  px[i, j][2] < 250):
				# ADJUST PARAMETERS BELOW FOR X AND Y OFFSET
				drawPixel(i + 32, j + 0, 1)
	for  i  in  range(0, 1024):
		outputString += str(buffer[i])
		if (i != 1023):
			outputString += ", "
		outputString += "},\n"

outputString = outputString[:-1] # remove comma from last one
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
```



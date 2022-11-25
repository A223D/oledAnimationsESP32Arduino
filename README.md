# OLED Animations With an ESP32 Using Arduino Core

## Examples
Examples taken from [lordicon.com](lordicon.com)

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
2. Converting them to frames using Python.
3. Storing them in a separate file as a 2D array.
4. Linking the file to our main sketch
5. Displaying these frames on the screen using Adafruit library functions.

## Procuring and Preparing Animations
For the sake of this tutorial, we will be procuring animation from Lordicon.com, a provider of a useful variety of animated icons. 

1. Go to [lordicon.com](lordicon.com) and click `Explore library`. Select a category. For monochrome OLED displays, I would recommend the `Wired Outline`, `System Outline`, or `System Solid` collections, as they look the cleanest. 

2. Select `Free icons` to filter out the paid icons, select any one out of the free ones. Some animations have multiple colours, and motion types. Select your favourite one. 

> Since my display is monochrome, I have created my Python script(which converts the image frames to c-style 2D arrays) to replace all colours except white with the primary colour of my display(white). To clarify, any non-white colours in the image will show up as white on my screen, and any white colour in the image will be assumed to be background and show up as black on my screen. 

3. Click the green button with `GIF` in it to open a configuration box. Since the animation is square, and my screen size is 128x64, I'm going to resize to 64px. Resize according to your screen size.
> If you have a colour screen, you can adjust the colours of the animation as well by clicking the right-facing icon under the icon preview. The main thing to make sure of is that the final animation will fit on your screen.

4. Download the .gif file and save on it on your PC.

## Splitting Frames

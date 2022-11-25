# OLED Animations With an ESP32 Using Arduino Core

## Examples
Examples taken from [lordicon.com](lordicon.com)

## Introduction & Requirements
This project details how to create animations on OLED screens like SSD1306/SSD1315 etc. This project uses Adafruit's GFX libraries to abstract away the low-level display-specific processes as much as possible.

For a deep dive into SSD1306/SSD1315 low level functions, [visit my other project on OLED animations using ESP-IDF](https://github.com/A223D/oledAnimationsESP-IDF).

The requirements for this project are:
* An ESP32
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

## Preparing Animations

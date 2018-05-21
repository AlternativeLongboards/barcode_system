# ALTERNATIVE BARCODE SYSTEM
## Since 2016 Alternative Longboards Company use system for production management based on tracking boards serial number (board_ID) during production and order/shipping operations. All barcode system hardware and software based on free/open-source solutions.

## OVERVIEW

### "Why company need it?"
It gives a lot of advantage, such as: 
+ helping with production planning/management
+ gives chance to see production process and number in real time
+ helps with order and shipping management
+ collect data for the future analysis (production efficent, errors etc.)

### "How it works in basic?"

Each board on first production step gets unique number (board_ID) represented by barcode. On each production step there is standalone working station (barcode scanner connected to Arduino with USB shield with Raspberry Pi) with which we scan barcode, and all metadata related to board_ID are stored in database (MongoDB) . Collected data are process and show on Node-RED dashboard.

### "How working station look like"

Here is general station overview
![im1](https://github.com/AlternativeLongboards/barcode_system/blob/master/DOCS/barcode_working_station_overview.jpg)

+ 1 MONITOR         - standard 15" LCD monitor
+ 2 CASE            - standard electric metal case 300x300x200 IP 66 holding **Arduino with USB shield, Raspbery Pi**, power supplies,                           ventilation, wifi antennas.
+ 3 FRAME           - construction created from 30x30 metal profiles, welded. Technical drawning available 
+ 4 KEYBOARD/mouse  - standard wireless keyboard/mouse setup

### "How many working station are in company?"

There is six working stations inside production area. 

**One for each production step:**
+ preparing room (where all materials for each board are collected, putting together and stored in one piece called "sandwitch")
+ pressing room (where all materials from one "sandwitch" are soacked with epoxy resing and press to form board)
+ cutting room (where pressed board are cut off)
+ sanding room
+ finishing room (where board get final touch, stickers and are prepared to shipping)

**Last one for creating/shipping orders:**
+ shipping room

### "How working station collect barcodes"

Each working station got wireless barcode scanner which is connected to USB Shield (working with Arduino UNO). If scanner get barcode send it to Arduino. Arduino tempoarary holds scanned data. Between scanner and Arduino there is one-way communication. Raspberry Pi using serial port within set period of time asks Arduino about new data. In case of new data available ask for sending collected barcode. Raspberry Pi after recivice new data prepare data frame with metadata about collected barcode and send it to proper collections in MongoDB database. 

### "How barcode system network works"

Working station got static IP adress in local wireless network. Each station connect to MongoDB on server (also with static IP). There is also option for sending message on each working station. All information are displaed using Node-RED Dashboard (running on server).

![im2](https://github.com/AlternativeLongboards/barcode_system/blob/master/DOCS/barcode_working_station_network.jpg)

Node RED Flow overview:

![im3](https://github.com/AlternativeLongboards/barcode_system/blob/master/DOCS/node_red_barcode_station.jpg)


### "What kind of information are collected on working station"

Working station to each scanned barcode add metadata such as:

+ timestamp
+ production step
+ worker name
+ comment (if avaiable)

Working station for creating orders collects data:

+ buyer/customer data 
+ amount of order boards per model
+ timestamp
+ comment (if available)

Working station for sending orders collects data:

+ serial numbers of boards added to package
+ timestamp
+ comment (if available)

## INSTALLATION

``` gitclone https://github.com/AlternativeLongboards/barcode_system ```

## HARDWARE REQUITRMENTS

+ Rasbperry Pi (recommended). You can use clone but it can cause some trouble with PySerial (not recommended for OrangePi family)
+ Arduino UNO (recommended). You can use clone, it was tested without any problems
+ strong wifi antenna
+ Arduino USB shield like: **https://store.arduino.cc/arduino-usb-host-shield**
+ 12 V power supply for Arduino and ventillator
+ 5 V power supplu for SBC (RaspberryPi) at least 2 A
+ standard computer 12V 120x120 ventillator
+ tandard wireless keyboard/mouse setup with monitor


## SOFTWARE REQUITRMENTS

+ Rasbian OS (recommended)
+ Python 3.5 or higher
+ PyMongo module (Python)
+ Kivy module (Python)
+ PySerial module (Python)
+ some time to configure




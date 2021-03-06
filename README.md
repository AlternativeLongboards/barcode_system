# ALTERNATIVE BARCODE SYSTEM
## Since 2016 Alternative Longboards Company has been using system for production management based on board’ s tracking serial number (board_ID) during their production and then implementation of orders  including shipping operations. It is worth mentioning that all barcode hardware and software system  are based on free and open-source solutions.

## OVERVIEW

### **"Why does the company need it?"**

It has a lot of advantages, such as:
+ helps with a production planning and its management,
+ gives a chance to see a production process in real time
+ helps with orders and shipping management,
+ collects data for the future analysis (production efficiency, errors etc.)

### **"How does it work in basic?"**

During the first step of production each board gets its unique number (board_ID) represented by barcode. On every production step there is a standalone working station (barcode scanner is connected to Arduino with a USB shield with a Raspberry Pi) thanks to which the Company can scan barcodes and all metadata related to board_ID that are stored in a database (MongoDB). Collected data are processed and shown on NodeRED dashboard.

**MongoDB and NodeRED are running on standalone local server**

### **"How does the working station look like"**

Here is a general station overview:
![im1](https://github.com/AlternativeLongboards/barcode_system/blob/master/DOCS/barcode_working_station_overview.jpg)

+ 1 MONITOR         - standard 15" LCD monitor
+ 2 CASE            - standard electric metal case 300x300x200 IP 66 holding **Arduino with USB shield, Raspbery Pi**, power supplies,                           ventilation, wifi antennas.
+ 3 FRAME           - welded construction is created from 30x30 metal profiles; technical drawning is available 
                      barcode_working_station_frame_dimensions.PDF
+ 4 KEYBOARD/mouse  - standard wireless keyboard/mouse setup.

### **"How many working stations are in the Company?"**

There are six working stations inside the production area (**one for every production step**):

+ preparing room (where all materials for every board are collected, put together and stored in one piece called "sandwitch"),
+ pressing room (where all materials from one "sandwitch" are soacked with epoxy resing and pressed to form a board),
+ cutting room (where pressed boards are cut off),
+ finishing room (where boards get final touch, stickers and are prepared for the shipping),
+ shipping room (where orders wait, ready for the shipment). 

### **"How does working station collect the barcodes?"**

Every working station is provided with wireless barcode scanner which is connected to USB Shield (working with Arduino UNO). If scanner gets barcode it sends it to Arduino. Arduino temporarily holds a scanned data. Between scanner and Arduino there is only one-way communication. Raspberry Pi using serial port within set period of time asks Arduino about new data. In case of new data available Raspberry Pi asks to send collected barcodes. After receiving the new data Raspberry Pi prepares data frame with metadata about collected barcodes in order to to send it to proper collections in a MongoDB database.

### **"How does barcode system network work?"**

Working station gets static IP address in local wireless network. Each station connects with the MongoDB server (also with static IP). There is also an option of sending message by each working station. All this information is displaed using NodeRED Dashboard (running on server).

![im2](https://github.com/AlternativeLongboards/barcode_system/blob/master/DOCS/barcode_working_station_network.jpg)

### **"How does NodeRED and NodeRED dashboard work in basic"**

Using NodeRED server display information about collected barcodes such as:

+ how many boards are on each production step (for each model)
+ how many boards are ready to ship (for each model)
+ how many orders are made (for each model)

![im3](https://github.com/AlternativeLongboards/barcode_system/blob/master/DOCS/barcode_node_red_production.jpg)

**file with flow - [NODE_RED_WORKFLOW]production.txt**

about acitivity on working station:

+ actual worker active on workstation
+ last scanned data
+ flow chart from past 2 hours of activity

Using NodeRED You can send message on each work station

![im4](https://github.com/AlternativeLongboards/barcode_system/blob/master/DOCS/barcode_node_red_stations.jpg)

**file with flow - [NODE_RED_WORKFLOW]working_station.txt**

see board ID history

![im5](https://github.com/AlternativeLongboards/barcode_system/blob/master/DOCS/barcode_node_red_production_history.jpg)

**file with flow - [NODE_RED_WORKFLOW]ID_history.txt**

and current orders info for each model

![im5](https://github.com/AlternativeLongboards/barcode_system/blob/master/DOCS/barcode_node_red_orders.jpg)

**file with flow - [NODE_RED_WORKFLOW]orders.txt**

### **"What kind of information is collected on working station?"**

To every scanned barcode working stations add metadata such as:

+ timestamp
+ production step
+ worker name
+ comment (if avaiable)

Working station for creating orders collects data like:

+ buyer/customer data 
+ amount of order boards per model
+ timestamp
+ comment (if available)

Working station for sending orders collects data like:

+ serial numbers of boards added to package
+ timestamp
+ comment (if available)

## INSTALLATION

``` gitclone https://github.com/AlternativeLongboards/barcode_system ```

**Configure and run server with MongoDB and Node-RED environment.** its recommend to grand acess only from working station static IP database, please close all extra ports and filter IP's !.

Upload Arduino program - recommended is to use PlatformIO core.

Run correct program for station: 
+ preparing room        - main00.py
+ pressing room         - main01.py
+ cutting room          - main02.py
+ sanding room          - main03.py
+ finishing room        - main04.py
+ package room          - main05.py
+ entering order        - order.py

## HARDWARE REQUIREMENTS

For one working station:

+ Rasbperry Pi (recommended). It can be used clone but it may cause some trouble with PySerial (not recommended for OrangePi family)
+ Arduino UNO (recommended). There can be used clone ( it was tested and did not cause  any problems),
+ standard ISO wireless barcode scanner
+ strong wifi antenna
+ Arduino USB shield like for eg.: https://store.arduino.cc/arduino-usb-host-shield,
+ 12 V power supply for Arduino and ventillator
+ 5 V power supplu for SBC (RaspberryPi) at least 2 A
+ standard computer 12V 120x120 ventilator
+ standard wireless keyboard/mouse setup with monitor

Standalone server

## SOFTWARE REQUIREMENTS

+ Rasbian OS (recommended)
+ Python 3.5 or higher
+ PyMongo module (Python)
+ Kivy module (Python)
+ PySerial module (Python)
+ PlatfformIO - https://platformio.org/
+ some time to configure
+ standalone server with MongoDB and NodeRED
+ MondoDB node for NodeRED




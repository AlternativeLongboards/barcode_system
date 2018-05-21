from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import Label as ButtonText
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.text import Label as CoreLabel
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
import math
import serial
import time
from pymongo import MongoClient
import datetime
import threading
import socket
from kivy.uix.scrollview import ScrollView

time.sleep(5)

#host = '213.32.89.50'
host = '192.168.1.200'
port = 6646                                                                                                             # tu zmienic !!!
port2 = 6746                                                                                                            # tu zmienic !!!
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.setblocking(0)
s.settimeout(0)

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((host, port2))
s2.setblocking(0)
s2.settimeout(0)

print('connected to socket')

#client = MongoClient('mongodb://213.32.89.50:27017/')
client = MongoClient('mongodb://192.168.1.200:27017/')

print('conneted to mongodb')

db = client['production']
staff = db['staff']
second_category = db['nd2category']
comments = db['comments']
collection_00 = db['preparing']
collection_01 = db['pressing']
collection_02 = db['cutting']
collection_03 = db['sanding']
collection_04 = db['finishing']
collection_05 = db['stock']
collection_topress = db['topress']
collection_tocut = db['tocut']
collection_tosand = db['tosand']
collection_tofinish = db['tofinish']
collection_tostock = db['stock']
collection_evermade = db['evermade']
collection_missingcodes = db['missingcodes']
collection_workertime = db['workertime']
collection_orders = db['orders']
collection_history_orders = db['history_orders']
collection_packages = db['packages']

print('conneted to mongodb')
try:
    MasterModule = serial.Serial('COM8', 115200 )

except:
    MasterModule = serial.Serial('/dev/ttyUSB0', 115200)
print('connected to arduino at: %s' % MasterModule.name)
time.sleep(1)

machine_state = 0
code = ["", "", "", "", "", "", "", "", "", ""]
code_win = ["", "", "", "", "", "", "", "", "", "","", "", "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "" ]
label_list = ['barcode1', 'barcode2', 'barcode3', 'barcode4', 'barcode5', 'barcode6', 'barcode7', 'barcode8',
              'barcode9', 'barcode10']
lis_window = ['cut00', 'cut01', 'cut02', 'cut03', 'cut04', 'cut05', 'cut06', 'cut07', 'cut08', 'cut09',
              'cut10', 'cut11', 'cut12', 'cut13', 'cut14', 'cut15', 'cut16', 'cut17', 'cut18', 'cut19',
              'cut20', 'cut21', 'cut22', 'cut23', 'cut24', 'cut25', 'cut26', 'cut27', 'cut28', 'cut29',
              'cut30', 'cut31', 'cut32', 'cut33', 'cut34', 'cut35', 'cut36', 'cut37', 'cut38', 'cut39']

current_code = ""
current_time = ""
worker = ""
last_record = ""
b = 0
data = 0
send_zero = 0

read_code = ""
timestamp = ""
data_added = 0
comm_added = 0
comment_added = 0
sec = 0
com = 0
worker_time_start = ""
worker_time_stop = ""

code_tcp = ""
time_tcp = ""

message = ""
last_message = ""

boards_on_pack = [ "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "",
                   "", "", "", "", "", "", "", "", "", "", ]

models_to_pack = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]

read_button_flag = 0

document = dict()
order_number = 0
mode_flag = 0                                                                                                           # flaga trybu ( 0 - normalna praca, 1 - delete, 2 - find, 3 - hold)
board_string = ""
total_to_pack = 0
find_label = 0
remove_label = 0

Builder.load_string("""

<MainWindow>:
    BoxLayout:
        canvas.before:
            Color:
                rgba: 1,1,1, .80
            Rectangle:
                pos: root.pos
                size: root.size
        orientation: 'vertical'
        color: (1,1,1,0)
        orientation: 'vertical'
        BoxLayout:
            orientation: 'vertical'
            BoxLayout:
                canvas.before:
                    Color:
                        rgba: 0,0,0, 0.75
                    Rectangle:
                        pos: self.pos
                        size: self.size
                orientation: 'horizontal'
                size_hint: 1, .18
                Label:
                    text: '[b]PACKAGE ROOM - 05[b]'                                                                     # tu zmienic !!!
                    markup: 'True'
                    font_size: self.parent.width/20
                Label:
                    size_hint: 0.3 , 1
                Image:
                    source: 'logo.png'
                    size_hint: 0.5 , 1
                Label:
                    size_hint: .1, 1
            BoxLayout:
                orientation: 'horizontal'
                BoxLayout:
                    orientation: 'vertical'
                    size_hint: .9, 1
                    Label:
                        size_hint: 1, .2
                    Label:
                        text: '[b]SCANNED BARCODES[b]'
                        markup: 'True'
                        size_hint: 1, 1.2
                        font_size: self.parent.width/13
                        color: 0, .6156, .48235
                    Label:
                        size_hint: 1, 0.1
                    Label:
                        id: barcode1
                        text: ''
                        color: 0, 0, 0, .6
                        font_size: self.parent.width/19
                    Label:
                        id: barcode2
                        text: ''
                        color: 0, 0, 0, .6
                        font_size: self.parent.width/19
                    Label:
                        id: barcode3
                        text: ''
                        color: 0, 0, 0, .6
                        font_size: self.parent.width/19
                    Label:
                        id: barcode4
                        text: ''
                        color: 0, 0, 0, .6
                        font_size: self.parent.width/19
                    Label:
                        id: barcode5
                        text: ''
                        color: 0, 0, 0, .6
                        font_size: self.parent.width/19
                    Label:
                        size_hint: 1, .2
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: 1, 4
                        Label:
                            size_hint: .2, 1
                        BoxLayout:
                            orientation: 'vertical'
                            Label:
                                size_hint: 1,.5
                                text: 'ORDER NUMBER'
                                font_size: self.parent.width/12
                                color: 0,0,0,1
                            TextInput:
                                id: order_number_textinput
                                size_hint: 1,.6
                                font_size: self.parent.width/12
                                padding_x: self.width/2
                                on_text: root.update_padding(args[0])
                            Label:
                                size_hint: 1,.5
                                text: 'COMMENT'
                                font_size: self.parent.width/12
                                color: 0,0,0,1
                            TextInput:
                                size_hint: 1,.6
                                font_size: self.parent.width/12
                                padding_x: self.width/2
                                on_text: root.update_padding(args[0])
                        Label:
                            size_hint: .2, 1
                    Label:
                        size_hint: 1, 0.5
                Label:
                    size_hint: 0.01 , 1
                BoxLayout:
                    orientation: 'vertical'
                    Label:
                        id: client_label
                        text: 'NO CLIENT'
                        color: 1,0,0, .5
                        font_size: self.parent.width/12
                    Label:
                        id: last_code
                        text: '[b]0100010100101[b]'
                        markup: 'True'
                        color: 1,0,0, .5
                        font_size: self.parent.width/10
                        size_hint: 1 , .6
                    Label:
                        id: last_code_time
                        text: '[b][b]'
                        markup: 'True'
                        color: 1,0,0,.6
                        font_size: self.parent.width/10
                        size_hint: 1, 0.5
                        size_hint: 1 , .6
                    Label:
                        id: status
                        text: '[b]DISCONNECT[b]'
                        markup: 'True'
                        color: 0,0,0,.7
                        font_size: self.parent.width/12
                        halign: 'center'
                        valign: 'middle'
                        size_hint: 1 , .6
                    Label:
                        id: worker_label
                        text: '-'
                        font_size: self.parent.width/13
                        color: 0, .6156, .48235, 1
                        halign: 'center'
                        valign: 'middle'
                        size_hint: 1 , .6
#                    Label:
#                        size_hint: 1, .05
                    BoxLayout:
                        BoxLayout:
                            orientation: 'vertical'
                            size_hint: 1.2 ,1.1
                            Label:
                                size_hint: 1, 0.4
                            BoxLayout:
                                orientation: 'horizontal'
                                Label:
                                    size_hint: .05 , 1
                                Button:
                                    id: read_button
                                    text: 'READ'
                                    font_size: self.parent.width/26
                                    text_size: self.parent.width/4  , None
                                    halign: 'center'
                                    valign: 'middle'
                                    background_color: 0,0,0, 0.75
                                    background_normal: ''
                                    on_press: root.read_order()
                                Label:
                                    size_hint: .1 , 1
                                Button:
                                    text: 'CLEAR'
                                    font_size: self.parent.width/26
                                    text_size: self.parent.width/5, None
                                    halign: 'center'
                                    valign: 'middle'
                                    background_color: 0, .6156, .48235, 1
                                    background_normal: ''
                                    on_press: root.clear_boards()
                                Label:
                                    size_hint: .1 , 1
                                Button:
                                    id: delete_board_button
                                    text: 'DELETE BOARD'
                                    font_size: self.parent.width/26
                                    text_size: self.parent.width/5, None
                                    halign: 'center'
                                    valign: 'middle'
                                    background_color: 0, .6156, .48235, 1
                                    background_normal: ''
                                    on_press: root.delete_board()                                                                     # tu zmienic tylko dla 00
                                Label:
                                    size_hint: .1 , 1
                                Button:
                                    id: find_button
                                    text: 'FIND'
                                    font_size: self.parent.width/26
                                    text_size: self.parent.width/5, None
                                    halign: 'center'
                                    valign: 'middle'
                                    background_color: 0, .6156, .48235, 1
                                    background_normal: ''
                                    on_press: root.find_board()
                                Label:
                                    size_hint: .05 , 1
                    Label:
                        size_hint: 1,.2
                    BoxLayout:
                        orientation: 'horizontal'
                        size_hint: 1, .8
                        Label:
                            size_hint: .05 , 1
                        Button:
                            text: 'SEND'
                            font_size: self.parent.width/26
                            background_color: 0,0,0, 0.55
                            background_normal: ''
                            on_press: root.send_package()
                        Label:
                            size_hint: .15 , 1
                        Button:
                            text: 'STOCK'
                            font_size: self.parent.width/26
                            text_size: self.parent.width/5, None
                            halign: 'center'
                            valign: 'middle'
                            background_color: 0, .6156, .48235, 1
                            background_normal: ''
                            on_press: root.show_info()
                        Label:
                            size_hint: .15, 1
                        Button:
                            text: 'SHOW BOARDS'
                            font_size: self.parent.width/26
                            text_size: self.parent.width/5, None
                            halign: 'center'
                            valign: 'middle'
                            background_color: 0, .6156, .48235, 1
                            background_normal: ''
                            on_press: root.show_boards()
                        Label:
                            size_hint: .15 , 1
                        Button:
                            text: 'EXIT'
                            font_size: self.parent.width/26
                            background_color: 0, .6156, .48235, 1
                            background_normal: ''
                            on_press: dupa
                        Label:
                            size_hint: .05, 1
                    Label:
                        size_hint: 1, 0.25

<BoardWindow>:
    size_hint: 0.5, 1
    title_align: 'center'
    title: 'SCANNED BOARD LIST'
    BoxLayout:
        ScrollView:
            Label:
                halign: 'center'
                valign: 'middle'
                text_size: self.parent.width/3.7, None
                id: board_list_message



<InfoWindow>:
    on_open: root.popup_count()
    size_hint: 0.8, 0.8
    title_align: 'center'
    title: 'BOARDS TO SEND'                                                                                              #tu zmienic
    BoxLayout:
        orientation: 'horizontal'
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: root.board_name_list[0]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[1]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[2]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[3]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[4]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[5]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[6]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[7]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[8]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[9]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
        BoxLayout:
            orientation: 'vertical'
            Label:
                id: cut00
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut01
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut02
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut03
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut04
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut05
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut06
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut07
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut08
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut09
                text: '0'
                color: 1,0,0,1
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: root.board_name_list[10]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[11]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[12]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[13]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[14]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[15]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[16]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[17]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[18]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[19]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
        BoxLayout:
            orientation: 'vertical'
            Label:
                id: cut10
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut11
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut12
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut13
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut14
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut15
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut16
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut17
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut18
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut19
                text: '0'
                color: 1,0,0,1
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: root.board_name_list[20]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[21]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[22]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[23]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[24]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[25]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[26]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[27]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[28]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[29]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
        BoxLayout:
            orientation: 'vertical'
            Label:
                id: cut20
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut21
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut22
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut23
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut24
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut25
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut26
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut27
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut28
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut29
                text: '0'
                color: 1,0,0,1
        BoxLayout:
            orientation: 'vertical'
            Label:
                text: root.board_name_list[30]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[31]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[32]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[33]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[34]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[35]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[36]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[37]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[38]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
            Label:
                text: root.board_name_list[39]
                size_hint: 1.5 , 1
                text_size: self.width, self.height
                font_size: self.parent.width/root.board_name_text_scale
                halign: 'left'
                valign: 'middle'
        BoxLayout:
            orientation: 'vertical'
            Label:
                id: cut30
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut31
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut32
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut33
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut34
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut35
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut36
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut37
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut38
                text: '0'
                color: 1,0,0,1
            Label:
                id: cut39
                text: '0'
                color: 1,0,0,1

""")

class BoardWindow(Popup):

    def __init__(self, **kwargs):

        super(BoardWindow, self).__init__(**kwargs)

        global boards_on_pack
        global board_string

        board_list_message = self.ids['board_list_message']
        for each in boards_on_pack:

            if (board_string.find(each) == - 1):

                board_string = board_string + each

        board_list_message.text = board_string
        board_string = ""

class InfoWindow(Popup):

    global boards_on_pack
    global models_to_pack

    board_name_list = ['00 - OSTRICH S', '01 - OSTRICH M', '02 - JUNKO M', '03 - CHAUMA M', '04 - CHAUMA W',
                       '05 - BUNTING', '06 - WROBEL', '07 - FLAMINGO M', '08 - FLAMINGO S', '09 - FANTAIL',
                       '10 - VERDIN', '11 - STARLING', '12 - ERGET S', '13 - ERGET M', '14 - EMPTY',
                       '15 - EMPTY', '16 - EMPTY', '17 - EMPTY', '18 - EMPTY', '19 - EMPTY',
                       '20 - EMPTY', '21 - EMPTY', '22 - EMPTY', '23 - EMPTY', '24 - EMPTY',
                       '25 - EMPTY', '26 - EMPTY', '27 - EMPTY', '28 - EMPTY', '29 - EMPTY',
                       '30 - EMPTY', '31 - EMPTY', '32 - EMPTY', '33 - EMPTY', '34 - EMPTY',
                       '35 - EMPTY', '36 - EMPTY', '37 - EMPTY', '38 - EMPTY', '39 - EMPTY', ]

    board_name_text_scale = 7

    def __init__(self, **kwargs):

        super(InfoWindow, self).__init__(**kwargs)

    def popup_count(self):

        global lis_window

        co = 0
        while co < 40:
            mo = ''
            code_win[co] = self.ids[lis_window[co]]
            code_win[co].text = str(models_to_pack[co])                                   #tu zmienic !!
            co += 1

class MainWindow(Screen):

    def __init__(self, **kwargs):

        super(MainWindow, self).__init__(**kwargs)
        Clock.schedule_interval(self.main_handling, 0.01)

    def show_boards(self, *args):

        global worker

        if (worker != ""):

            BoardWindow().open()

    def update_padding(self, text_input, *args):

        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width) / 2

    def show_info(self, *args):

        global worker

        if (worker != ""):

            InfoWindow().open()

    def serial_write(self, data_to_send):

        MasterModule.write(str(data_to_send).encode('utf-8'))
        MasterModule.flush()
#        time.sleep(0.01)

    def serial_clear(self):

        if (MasterModule.inWaiting() > 0):

            MasterModule.read(MasterModule.inWaiting())
            MasterModule.flush()

    def serial_read(self):

        myData = MasterModule.read(MasterModule.inWaiting())
        return myData

    def ask_data(self):

        readData = ""
        sendConfirmation = ""
        readConfirmation = ""
        counter = 0

        while (readConfirmation[0:4] != 'AC2E' or counter < 3):

            readData = ""
            sendConfirmation = ""
            readConfirmation = ""
            self.serial_clear()
            self.serial_write('AC1E')
            time.sleep(0.01)
            #readData = self.serial_read().decode()
            readData = self.serial_read().decode(encoding='UTF-8', errors='ignore')
            if (readData[0:1] != '0'):

                while (readConfirmation[0:4] != 'AC2E'):

                    sendConfirmation = 'AD' + str(readData[8:17]) + 'E'
                    self.serial_clear()
                    self.serial_write(sendConfirmation)
                    time.sleep(0.01)
                    readConfirmation = self.serial_read().decode()
                    if (readConfirmation[0:4] == 'AC2E'):

                        return readData[1:17]
                        break
                    else:

                        counter = counter + 1
                        if (counter == 3):
                            counter = 0
                            return -1
                            break
                break
            else:

                return 0
                break

    def label_handling(self):

        global label_list
        global current_code
        global current_time
        global last_record
        global data

        n = 4
        while n > 0:

            m = n - 1
            code[n] = self.ids[label_list[n]]
            code[m] = self.ids[label_list[m]]
            code[n].text = code[m].text
            n = n - 1

        code[0] = self.ids[label_list[0]]
        code[0].text = str(last_record)

        current_code.text = str(data[3:15])
        current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
        last_record = current_time.text + "  " + current_code.text

    def main_handling(self, *args):

        global code
        global worker
        global current_code
        global machine_state
        global current_time
        global last_record
        global message
        global data
        global time_tcp
        global code_tcp
        global read_code
        global timestamp
        global data_added
        global comm_added
        global comment_added
        global sec
        global com
        global worker_time_start
        global worker_time_stop
        global boards_on_pack
        global models_to_pack
        global read_button_flag
        global mode_flag
        global find_label
        global remove_label
        global total_to_pack

        current_code = self.ids['last_code']
        status_label = self.ids['status']
        current_time = self.ids['last_code_time']
        i_have_no_idea_for_variable = self.ids['worker_label']
        find_button = self.ids['find_button']
        delete_board_button = self.ids['delete_board_button']

        data = self.ask_data()
        comment_added = 0
        comm_added = 0
        data_added = 0



        if (machine_state == 0 and data == 0):

            status_label.text = 'CONNECTED'
            current_code.text = 'SCAN NIGGER CARD'
            machine_state = 1

        if (data != 0 and data != -1):

            worker_name = list(staff.find({"code": data[3:15]}, {"name": 1, "_id": 0}))
            worker_name = str(worker_name)
            timestamp = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            read_code = str(data[3:15])
            model = data[5:7]
            if (len(worker_name) > 2):

                worker_name = worker_name[11:len(worker_name) - 3]
                if (worker != ""):

                    worker_time_stop = datetime.datetime.now()
                    print('stop time: ' + str(worker_time_stop))
                    print('worker finish work: ' + worker)
                    t = str(round((worker_time_stop - worker_time_start).total_seconds() / 60))
                    worker_time = {

                        "worker": worker,
                        "finish": timestamp,
                        "start": str(worker_time_start),
                        "time": t,
                        "station": "03"

                    }
                    collection_workertime.insert_one(worker_time)

                if (worker_name == worker):

                    current_time.text = '-'
                    i_have_no_idea_for_variable.text ="-"
                    worker = ""
                    machine_state = 0
                else:

                    worker_time_start = datetime.datetime.now()
                    print('start time: ' + str(worker_time_start))
                    worker = worker_name
                    i_have_no_idea_for_variable.text = worker
                    current_code.text = 'READY TO WORK'
                    status_label.text = 'CONNECTED'
                    print('setting worker to: %s' % worker_name)
                    current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
            else:

                if (worker != ""):

                    model = read_code[2:4]
                    model = int(model)

                    self.total_pack_calculation()

                    if (read_button_flag == 1):

                        if (total_to_pack > 0):

                            if (mode_flag == 0):

                                if ((read_code in boards_on_pack) == False):

                                    if (models_to_pack[model] > 0):

                                        boards_on_pack.append(read_code)
                                        models_to_pack[model] = models_to_pack[model] - 1
                                        current_code.text = read_code
                                        status_label.text = 'WRITED'
                                        self.label_handling()
                                    else:

                                        status_label.text = 'CONNECTED'
                                        current_code.text = 'POSITION FULL'
                                        current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
                                else:

                                    self.label_handling()
                                    status_label.text = 'CONNECTED'
                                    current_code.text = 'DUPLICATED'
                                    current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
                        else:

                            status_label.text = 'READY'
                            current_code.text = 'ALL BOARDS PACKED'
                            current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
                    else:

                        status_label.text = 'CONNECTED'
                        current_code.text = 'READ ORDER FIRST'
                        current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))

                    if (mode_flag == 2):

                        mode_flag = 0
                        find_button.text = 'FIND'

                        if ( (read_code in boards_on_pack) == True ):

                            status_label.text = 'FIND'
                            current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
                            current_code.text = read_code
                        else:

                            status_label.text = 'NOT PRESENT'
                            current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
                            current_code.text = read_code
                        self.label_handling()
                        find_label = 0

                    if (mode_flag == 1):

                        mode_flag = 0
                        delete_board_button.text = "DELETE"

                        if ( (read_code in boards_on_pack) == True ):

                            status_label.text = 'REMOVED'
                            current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
                            current_code.text = read_code
                            boards_on_pack.remove(read_code)
                            models_to_pack[model] = models_to_pack[model] + 1
                        else:

                            status_label.text = 'NOT PRESENT'
                            current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
                            current_code.text = read_code
                        self.label_handling()
                        remove_label = 0

                else:

                    current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
                    status_label.text = 'NO WORKER SCANNED'

    def read_order(self):

        global models_to_pack
        global read_button_flag
        global document
        global boards_on_pack
        global order_number
        global worker

        current_time = self.ids['last_code_time']
        current_code = self.ids['last_code']
        read_button = self.ids['read_button']
        client_label = self.ids['client_label']
        order_number_textinput = self.ids['order_number_textinput']
        order_number_label = self.ids['order_number_textinput']
        status_label = self.ids['status']
        order_number = order_number_label.text

        if (worker != ""):

            if (read_button_flag == 0):

                document = collection_orders.find_one({"order_number": order_number})
            if (bool(document) == True):

                if (read_button_flag == 0):

                    client_label.text = str(order_number)
                    order_number_textinput.text = ""
                    for each in range(0,14):

                        board_label = ""
                        if (each < 10):

                            board_label = "board0" + str(each)
                        else:

                            board_label = "board" + str(each)
                        models_to_pack[each] = document.get(board_label)

                    read_button_flag = 1
                    read_button.text = "CANCEL"
                    status_label.text = "READY"
                    current_code.text = ""
                    current_time.text = ""
                else:

                    for each in range(0,40):

                        models_to_pack[each] = 0
                    boards_on_pack = []
                    document.clear()
                    client_label.text = "NO ORDER"
                    read_button.text = "READ"
                    status_label.text = "CANCELLED"
                    read_button_flag = 0
            else:

                status_label.text = "WRONG NUMBER"
                order_number_textinput.text = ""
                current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))

    def clear_boards(self):

        global models_to_pack
        global boards_on_pack
        global order_number
        global board_string
        global worker

        status_label = self.ids['status']
        current_time = self.ids['last_code_time']
        current_code = self.ids['last_code']

        if (worker != ""):

            for each in range(0,40):

                models_to_pack[each] = 0
            boards_on_pack = []
            board_string = ""
            document = collection_orders.find_one({"order_number": order_number})
            if (bool(document) == True):

                for each in range(0, 14):

                    board_label = ""
                    if (each < 10):

                        board_label = "board0" + str(each)
                    else:

                        board_label = "board" + str(each)
                    models_to_pack[each] = document.get(board_label)
                status_label.text = "CLEARED"
                current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
                current_code.text = ""
            else:

                status_label.text = "CANNOT CLEAR"
                current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
                current_code.text = ""

    def find_board(self):

        global mode_flag
        global read_button_flag
        global worker
        global find_label

        current_code = self.ids['last_code']
        status_label = self.ids['status']
        current_time = self.ids['last_code_time']
        find_button = self.ids['find_button']

        find_label = 1

        if (worker != ""):

            if (mode_flag == 2):
                find_button.text = "FIND"
                mode_flag = 0
                status_label.text = "READY"
                current_code.text = ""
                current_time.text = ""
            else:

                if (mode_flag == 0 or mode_flag == 3):

                    if (read_button_flag == 1):

                        mode_flag = 2
                        current_code.text = "SCAN CODE"
                        status_label.text = ""
                        current_time.text = "TO FIND"
                        find_button.text = "CANCEL"
                    else:

                        status_label.text = 'CONNECTED'
                        current_code.text = 'READ ORDER FIRST'
                        current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))

    def delete_board(self):

        global mode_flag
        global read_button_flag
        global worker
        global remove_label

        remove_label = 1

        current_code = self.ids['last_code']
        status_label = self.ids['status']
        current_time = self.ids['last_code_time']
        find_button = self.ids['find_button']
        delete_board_button = self.ids['delete_board_button']

        if (worker != ""):

            if (mode_flag == 1 or mode_flag == 3):
                mode_flag = 0
                delete_board_button.text = "DELETE"
                status_label.text = "READY"
                current_code.text = ""
                current_time.text = ""

            else:
                if (mode_flag == 0):

                    if (read_button_flag == 1):

                        mode_flag = 1
                        current_code.text = "SCAN CODE"
                        status_label.text = ""
                        current_time.text = "TO DELETE"
                        delete_board_button.text = "CANCEL"
                    else:

                        status_label.text = 'CONNECTED'
                        current_code.text = 'READ ORDER FIRST'
                        current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))

    def send_package(self):

        global models_to_pack
        global boards_on_pack
        global total_to_pack
        global order_number
        global read_button_flag

        current_time = self.ids['last_code_time']
        current_code = self.ids['last_code']
        read_button = self.ids['read_button']
        client_label = self.ids['client_label']
        order_number_textinput = self.ids['order_number_textinput']
        order_number_label = self.ids['order_number_textinput']
        status_label = self.ids['status']

        self.total_pack_calculation()
        old_document = dict()
        document_to_send = dict()

        if (total_to_pack == 0):

            old_document = collection_orders.find_one({"order_number": order_number})
            del old_document['_id']
            collection_history_orders.insert_one(old_document)
            i = collection_orders.delete_many({"order_number": order_number}).deleted_count
            document_to_send["name"] = old_document["name"]
            document_to_send["order_number"] = old_document["order_number"]
            document_to_send["invoice"] = old_document["invoice"]
            document_to_send["timestamp"] = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            for each in boards_on_pack:
                document_to_send[each] = 1
                i = collection_tostock.delete_many({"code":each}).deleted_count
                print ( i )
            del old_document
            collection_packages.insert_one(document_to_send)
            del document_to_send

            for each in range(0, 40):
                models_to_pack[each] = 0
            boards_on_pack = []
            document.clear()
            client_label.text = "NO ORDER"
            read_button.text = "READ"
            status_label.text = "SEND !"
            current_code.text = ""
            current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
            read_button_flag = 0
        else:

            try:
                self.label_handling()
            except:
                pass

            status_label.text = "NOT FULL"
            current_code.text = ""
            current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))

    def total_pack_calculation(self):

        global total_to_pack

        total_to_pack = 0
        for each in range(0, 40):
            total_to_pack = total_to_pack + models_to_pack[each]

class ScanApp(App):
    def __init__(self, **kwargs):

        super(ScanApp, self).__init__(**kwargs)
        Clock.schedule_interval(self.send_tcp, 0.5)

    def send_tcp(self, *args):

        global time_tcp
        global code_tcp
        global worker
        global send_zero

        if (time_tcp != "1" and code_tcp != "1"):
            string_to_send = '!' + time_tcp + '*' + '/' + code_tcp + '*' + ';' + worker + '*' + '$' + '1' + '*'
            s2.sendall(str.encode(string_to_send))
            code_tcp = "1"
            time_tcp = "1"
            send_zero = 1

        elif (send_zero == 1):
            string_to_send = '*' + '$' + '0'
            s2.sendall(str.encode(string_to_send))
            send_zero = 0

    def build(self):
        return MainWindow()


if __name__ == '__main__':
    ScanApp().run()

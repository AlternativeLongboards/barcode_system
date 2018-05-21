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

time.sleep(5)

#host = '213.32.89.50'
host = '192.168.1.200'
port = 6626                                                                                                             # tu zmienic !!!
port2 = 6726                                                                                                            # tu zmienic !!!
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
collection_missingcodes = db['missingcodes']
collection_workertime = db['workertime']

print('conneted to mongodb')
try:
    MasterModule = serial.Serial('COM3', 115200)
except:
    MasterModule = serial.Serial('/dev/ttyUSB0', 115200)
print('connected to arduino at: %s' % MasterModule.name)
time.sleep(1)

machine_state = 0
code = ["", "", "", "", "", "", "", "", "", ""]
code_win = ["", "", "", "", "", "", "", "", "", "","", "", "", "", "", "", "", "", "", ""]
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
                    text: '[b]CNC ROOM - 02[b]'                                                                         # tu zmienic !!!
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
                        size_hint: 1, 0.4
                    Label:
                        text: '[b]SCANNED BARCODES[b]'
                        markup: 'True'
                        size_hint: 1, 1.2
                        font_size: self.parent.width/13
                        color: 0, .6156, .48235
                    Label:
                        size_hint: 1, 0.2
                    Label:
                        id: barcode1
                        text: ''
                        color: 0, 0, 0, 1
                        font_size: self.parent.width/19
                    Label:
                        id: barcode2
                        text: ''
                        color: 0, 0, 0, 0.95
                        font_size: self.parent.width/19
                    Label:
                        id: barcode3
                        text: ''
                        color: 0, 0, 0, 0.9
                        font_size: self.parent.width/19
                    Label:
                        id: barcode4
                        text: ''
                        color: 0, 0, 0, 0.85
                        font_size: self.parent.width/19
                    Label:
                        id: barcode5
                        text: ''
                        color: 0, 0, 0, 0.8
                        font_size: self.parent.width/19
                    Label:
                        id: barcode6
                        text: ''
                        color: 0, 0, 0, 0.75
                        font_size: self.parent.width/19
                    Label:
                        id: barcode7
                        text: ''
                        color: 0, 0, 0, 0.7
                        font_size: self.parent.width/19
                    Label:
                        id: barcode8
                        text: ''
                        color: 0, 0, 0, 0.65
                        font_size: self.parent.width/19
                    Label:
                        id: barcode9
                        text: ''
                        color: 0, 0, 0, 0.6
                        font_size: self.parent.width/19
                    Label:
                        id: barcode10
                        text: ''
                        color: 0, 0, 0, 0.55
                        font_size: self.parent.width/19
                    Label:
                        size_hint: 1, 0.5
                Label:
                    size_hint: 0.01 , 1
                BoxLayout:
                    orientation: 'vertical'
                    Label:
                        size_hint: 1, 0.7
                    Label:
                        id: last_code
                        text: '[b]-[b]'
                        markup: 'True'
                        color: 1,0,0, .5
                        font_size: self.parent.width/10
                        size_hint: 1 , .6
                    Label:
                        id: last_code_time
                        text: '[b]-[b]'
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
                    Label:
                        size_hint: 1, .2
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
                                    text: 'ADD COMMENTS'
                                    font_size: self.parent.width/26
                                    text_size: self.parent.width/4  , None
                                    halign: 'center'
                                    valign: 'middle'
                                    background_color: 0, .6156, .48235
                                    background_color: 0, .6156, .48235, 1
                                    background_normal: ''
                                    on_press: root.addcoment()
                                Label:
                                    size_hint: .1 , 1
                                Button:
                                    text: 'ADD 2nd CATEGORY'
                                    font_size: self.parent.width/26
                                    text_size: self.parent.width/5, None
                                    halign: 'center'
                                    valign: 'middle'
                                    background_color: 0, .6156, .48235, 1
                                    background_normal: ''
                                    on_press: root.nd2category()
                                Label:
                                    size_hint: .1 , 1
                                Button:
                                    text: 'STOCK'
                                    font_size: self.parent.width/26
                                    background_color: 0, .6156, .48235, 1
                                    background_normal: ''
                                    on_press: root.show_info()                                                          # tu zmienic tylko dla 00
                                Label:
                                    size_hint: .1 , 1
                                Button:
                                    text: 'EXIT'
                                    font_size: self.parent.width/26
                                    text_size: self.parent.width/5, None
                                    halign: 'center'
                                    valign: 'middle'
                                    background_color: 0, .6156, .48235, 1
                                    background_normal: ''
                                    on_press: dupa
                                Label:
                                    size_hint: .05 , 1
                    Label:
                        text: 'COMMENT'
                        color: 0,0,0,1
                        size_hint: 1, 0.3
                    TextInput:
                        id: comment
                        size_hint: 1 , 0.6
                    Label:
                        size_hint: 1, 0.3
                Label:
                    size_hint: .03, 1

<MessageWindow>:
    size_hint: 0.5, 0.5
    title_align: 'center'
    title: 'WIADOMOSC DLA PANA MURZYNA'
    BoxLayout:
        Label:
            id: messagetext

<InfoWindow>:
    on_open: root.popup_count()
    size_hint: 0.8, 0.8
    title_align: 'center'
    title: 'BOARDS TO CUT'                                                                                              #tu zmienic
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


class MessageWindow(Popup):

    def __init__(self, **kwargs):

        super(MessageWindow, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 0.2)

    def update(self, *args):

        global last_message

        pop = self.ids['messagetext']
        pop.text = last_message

class InfoWindow(Popup):

    board_name_list = ['00 - OSTRICH S S', '01 - OSTRICH M S', '02 - JUNKO M', '03 - CHAUMA M S', '04 - CHAUMA W S',
                       '05 - BUNTING', '06 - WROBEL', '07 - FLAMINGO M S', '08 - FLAMINGO S S', '09 - FANTAIL',
                       '10 - VERDIN S', '11 - STARLING', '12 - ERGET S S', '13 - ERGET M S', '14 - KAROO M S',
                       '15 - KAROO M', '16 - FLAMINGO MEDIUM', '17 - OSTRICH MEDIUM', '18 - VERDIN MEDIUM', '19 - ERGET MEDIUM',
                       '20 - CHAUMA W', '21 - CHAUMA M', '22 - EMPTY', '23 - EMPTY', '24 - EMPTY',
                       '25 - EMPTY', '26 - EMPTY', '27 - EMPTY', '28 - EMPTY', '29 - EMPTY',
                       '30 - EMPTY', '31 - EMPTY', '32 - EMPTY', '33 - EMPTY', '34 - EMPTY',
                       '35 - EMPTY', '36 - EMPTY', '37 - EMPTY', '38 - EMPTY', '39 - EMPTY', ]

    board_name_text_scale = 7

    def __init__(self, **kwargs):

        super(InfoWindow, self).__init__(**kwargs)

    def popup_count(self):

        global lis_window

        co = 0
        while co < 20:
            mo = ''
            code_win[co] = self.ids[lis_window[co]]
            if (co < 10):
                mo = str('0' + str(co))
            if (co > 9):
                mo = str(co)
            code_win[co].text = str(collection_tocut.find({"model": mo}).count())                                       #tu zmienic !!
            co += 1

class MainWindow(Screen):

    def __init__(self, **kwargs):

        super(MainWindow, self).__init__(**kwargs)
        Clock.schedule_interval(self.main_handling, 0.2)
        Clock.schedule_interval(self.display_message, 2)
        Clock.schedule_interval(self.th, 1)

    def message_read(self, *args):

        global message

        try:
            message = s.recv(512)
            message = message.decode('utf-8')
            message = str(message)
        except:
            pass

    def th(self, *args):

#        threading.Thread(target=self.message_read).start()
        self.message_read()

    def display_message(self, *args):

        global message
        global last_message

        if (message != ""):
            last_message = message
            MessageWindow().open()
            message = ""

    def show_info(self, *args):

        InfoWindow().open()

    def serial_write(self, data_to_send):

        MasterModule.write(str(data_to_send).encode('utf-8'))
        MasterModule.flush()
        time.sleep(0.01)

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
                        return -1
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

        n = 9
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

    def nd2category(self):

        global sec
        global worker

        print (" 2 nd category button pressed")

        if (worker != ""):
            current_code = self.ids['last_code']
            status_label = self.ids['status']
            current_time = self.ids['last_code_time']

            current_code.text = ''
            status_label.text = 'SCAN CODE'
            current_time.text = ''

            sec = 1

    def addcoment(self):

        global com
        global worker

        print(" add comment button pressed")

        if (worker != ""):
            current_code = self.ids['last_code']
            status_label = self.ids['status']
            current_time = self.ids['last_code_time']

            current_code.text = 'TYPE COMMENT '
            status_label.text = 'SCAN CODE'
            current_time.text = 'AND'

            com = 1

    def data_check(self):                                                                                               # tu_zmienic !!!

        global data_added

        is_present = 0
        check_counter = 0
        while (is_present == 0):
            is_present = collection_02.find({"code": read_code}).count()
            if (is_present > 0):
                data_added = 1
                break
            else:
                check_counter += 1
                if (check_counter > 8):
                    data_added = - 1
                    break

    def comm_check(self):                                                                                               # tu zmienic !!!

        global comm_added

        is_present = 0
        check_counter = 0
        while (is_present == 0):
            is_present = collection_tosand.find({"code": read_code}).count()
            if (is_present > 0):
                comm_added = 1
                break
            else:
                check_counter += 1
                if (check_counter > 8):
                    comm_added = -1
                    break

    def comment_check(self):

        global comment_added

        is_present = 0
        check_counter = 0
        while (is_present == 0 and comment_added == 0):
            is_present = comments.find({"timestamp": timestamp}).count()
            if (is_present > 0):
                comment_added = 1
                break
            else:
                check_counter += 1
                if (check_counter > 8):
                    comment_added = -1
                    break

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

        current_code = self.ids['last_code']
        status_label = self.ids['status']
        current_time = self.ids['last_code_time']
        i_have_no_idea_for_variable = self.ids['worker_label']
        comment_label = self.ids['comment']

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
            if (len(worker_name) > 2 and sec == 0 and com == 0):
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
                    if (sec == 0 and com == 0):
                        if (collection_02.find({"code": read_code}).count() == 0):                                      # tu zmienic !!!
                            new_data = {

                                "timestamp": timestamp,
                                "year_number": str(datetime.datetime.now().strftime('%j')),
                                "year": str(datetime.datetime.now().strftime('%Y')),
                                "month": str(datetime.datetime.now().strftime('%m')),
                                "day": str(datetime.datetime.now().strftime('%d')),
                                "hour": str(datetime.datetime.now().strftime('%H')),
                                "minute": str(datetime.datetime.now().strftime('%M')),
                                "second": str(datetime.datetime.now().strftime('%S')),
                                "code": read_code,
                                "model": model,
                                "worker": worker,
                                "operation": "02",                                                                      # tu zmienic !!!

                            }
                            collection_02.insert_one(new_data)                                                          # tu zmienic !!!
                            print("added to 02 base : " + read_code)                                                    # tu zmienic !!!

                            new_data2 = {

                                "code": read_code,
                                "model": model

                            }

                            collection_tosand.insert_one(new_data2)                                                     # tu zmienic !!!
                            i = db.tocut.delete_many({"code": read_code}).deleted_count                                 # tu zmienic !!!  uwaga przy 00

                            if (i < 1):
                                missing_code = {

                                    "code": read_code,
                                    "model": model,
                                    "missing": "01",                                                                    # tu zmienic !!!
                                    "timestamp": timestamp
                                }

                                collection_missingcodes.insert_one(missing_code)
                                print("missing in 01 base : " + read_code)                                              # tu zmienic !!!


                            if(str(comment_label.text) != ''):
                                comm = {

                                    "timestamp": timestamp,
                                    "code": read_code,
                                    "model": model,
                                    "worker": worker,
                                    "comment": comment_label.text

                                }

                                comments.insert_one(comm)
                                comment_added = 1
                            else:
                                comment_added = 1

                            data_added = 1                                                                              #self.data_check()  zlikwidowałem bo mongo i tak sprawdza czy jest ok. Mozna potem dodać rózne teksty pod wyjatki
                            comm_added = 1                                                                              #self.comm_check()
                            comment_added = 1                                                                           #self.comment_check()

                            if (data_added == 1 and comm_added == 1 and comment_added == 1):
                                self.label_handling()
                                status_label.text = 'WRITED'
                                code_tcp = str(data[3:15])
                                time_tcp = timestamp
                                comment_label.text = ""
                                current_code.text = read_code
                                current_time.text = timestamp[11:19]
                                print( read_code + " " + timestamp)

                        else:
                            current_code.text = read_code
                            current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
                            status_label.text = 'DUPLICATED'
                            print('element duplicated %s' % str(read_code))

                    if (sec == 1):
                        if (staff.find({"code": read_code}).count() == 0):
                            if (second_category.find({"code": read_code}).count() == 0 ):
                                nd2data = {

                                    "code": read_code,
                                    "timestamp": timestamp,
                                    "model": model

                                }

                                second_category.insert_one(nd2data)
                                print('board added to 2nd cat: ' + read_code)
                                status_label.text = 'ADDED 2ND CAT'
                                current_code.text = read_code
                                current_time.text = timestamp[11:19]
                                sec = 0
                            else:
                                status_label.text = 'ALREADY ADDED'
                                current_code.text = read_code
                                current_time.text = timestamp[11:19]
                                sec = 0
                        else:
                            print('error scanning worker card')
                            status_label.text = 'SECOND CAT'
                            current_code.text = 'PEOPLE ARE NOT'
                            current_time.text = timestamp[11:19]
                            sec = 0

                    if (com == 1):
                        if (comment_label.text == ""):
                            status_label.text = 'COMMENT EMPTY !'
                            current_code.text = 'ERROR'
                            current_time.text = timestamp[11:19]
                            com = 0
                        if (comment_label.text != ""):
                            com_data = {

                                "code": read_code,
                                "timestamp": timestamp,
                                "comment": comment_label.text,
                                "model": model

                            }

                            comments.insert_one(com_data)
                            print('insert comment: ' + comment_label.text)
                            status_label.text = 'ADDED COMMENT'
                            current_code.text = read_code
                            current_time.text = timestamp[11:19]
                            comment_label.text = ""
                            com = 0

                else:
                    current_time.text = str(datetime.datetime.now().strftime('%H:%M:%S'))
                    status_label.text = 'NO WORKER SCANNED'


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

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

# chuj

# host = '213.32.89.50'
host = '192.168.1.200'
port = 6606  # tu zmienic !!!
port2 = 6706  # tu zmienic !!!
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.setblocking(0)
s.settimeout(0)

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((host, port2))
s2.setblocking(0)
s2.settimeout(0)

print('connected to socket')

client = MongoClient('mongodb://192.168.1.200:27017/')
print('conneted to mongodb')

db = client['production']

collection_orders = db['orders']
collecttion_stock_count = db['stock_count']

print('conneted to mongodb')

time.sleep(1)

app_stop = 0
read_timestamp = ""

# Window.size = (800,600)

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
                    text: '[b]ORDER[b]'                                                                     # tu zmienic !!!
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
                orientation: 'vertical'
                Label:
                    size_hint: 1, .03
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint: 1, .6
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint: .5,1
                        BoxLayout:
                            size_hint: 1, .1
                            orientation: 'horizontal'
                            Label:
                                size_hint: .1, 1
                            Label:
                                id: label_client
                                text: '[b]CLIENT NAME[b]'
                                color: 0,0,0,1
                                size_hint: 2.2,1
                                markup: 'True'
                                font_size: self.parent.width/30
                            Label:
                                size_hint: .2, 1
                            Label:
                                id: label_country
                                text: '[b]COUNTRY[b]'
                                color: 0,0,0,1
                                markup: 'True'
                                font_size: self.parent.width/30
                            Label:
                                size_hint: .1, 1
                        BoxLayout:
                            size_hint: 1, .1
                            orientation: 'horizontal'
                            Label:
                                size_hint: .1, 1
                            TextInput:
                                id: client_name
                                size_hint: 2.2,1
                                on_text: root.update_padding(args[0])
                                padding_x: self.width/2
                                padding_y: self.height/4
                            Label:
                                size_hint: .2, 1
                            TextInput:
                                id: country
                                on_text: root.update_padding(args[0])
                                padding_x: self.width/2
                                padding_y: self.height/4
                            Label:
                                size_hint: .1, 1
                        BoxLayout:
                            size_hint: 1, .1
                            orientation: 'horizontal'
                            Label:
                                size_hint: .1, 1
                            Label:
                                id: label_adress
                                text: '[b]ADRESS[b]'
                                size_hint: 1.5,1
                                color: 0,0,0,1
                                markup: 'True'
                                font_size: self.parent.width/30
                            Label:
                                size_hint: .2, 1
                            Label:
                                id: label_post_code
                                text: '[b]POST-CODE[b]'
                                size_hint: .5,1
                                color: 0,0,0,1
                                markup: 'True'
                                font_size: self.parent.width/30
                            Label:
                                size_hint: .2, 1
                            Label:
                                id: label_invoice
                                text: '[b]INVOICE[b]'
                                color: 0,0,0,1
                                markup: 'True'
                                font_size: self.parent.width/30
                            Label:
                                size_hint: .1, 1
                        BoxLayout:
                            size_hint: 1, .1
                            orientation: 'horizontal'
                            Label:
                                size_hint: .1, 1
                            TextInput:
                                id: adress
                                size_hint: 1.5,1
                                on_text: root.update_padding(args[0])
                                padding_x: self.width/2
                                padding_y: self.height/4
                            Label:
                                size_hint: .2, 1
                            TextInput:
                                id: post_code
                                size_hint: .5,1
                                on_text: root.update_padding(args[0])
                                padding_x: self.width/2
                                padding_y: self.height/4
                            Label:
                                size_hint: .2, 1
                            TextInput:
                                id: invoice
                                on_text: root.update_padding(args[0])
                                padding_x: self.width/2
                                padding_y: self.height/4
                            Label:
                                size_hint: .1, 1
                    Label:
                        id: status
                        text: '[b]CONNECT[b]'
                        size_hint: .2, 1
                        color: 0,0,1,.6
                        markup: 'True'
                        font_size: self.parent.width/20
                Label:
                    size_hint: 1, .05
                BoxLayout:
                    orientation: 'horizontal'
                    BoxLayout:
                        orientation: 'vertical'
                        Label:
                            text: root.board_name_list[0]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[1]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[2]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[3]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[4]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[5]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[6]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[7]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[8]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[9]
                            color: 0,0,0,1
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint: .3, 1
                        TextInput:
                            id: board_00
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_01
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_02
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_03
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_04
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_05
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_06
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_07
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_08
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_09
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                    BoxLayout:
                        orientation: 'vertical'
                        Label:
                            text: root.board_name_list[10]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[11]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[12]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[13]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[14]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[15]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[16]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[17]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[18]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[19]
                            color: 0,0,0,1
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint: .3, 1
                        TextInput:
                            id: board_10
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_11
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_12
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_13
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_14
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_15
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_16
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_17
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_18
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_19
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                    BoxLayout:
                        orientation: 'vertical'
                        Label:
                            text: root.board_name_list[20]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[21]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[22]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[23]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[24]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[25]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[26]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[27]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[28]
                            color: 0,0,0,1
                        Label:
                            text: root.board_name_list[29]
                            color: 0,0,0,1
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint: .3, 1
                        TextInput:
                            id: board_20
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_21
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_22
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_23
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_24
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_25
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_26
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_27
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_28
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_29
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                    BoxLayout:
                        orientation: 'vertical'
                        Label:
                            text: root.board_name_list[30]
                        Label:
                            text: root.board_name_list[31]
                        Label:
                            text: root.board_name_list[32]
                        Label:
                            text: root.board_name_list[33]
                        Label:
                            text: root.board_name_list[34]
                        Label:
                            text: root.board_name_list[35]
                        Label:
                            text: root.board_name_list[36]
                        Label:
                            text: root.board_name_list[37]
                        Label:
                            text: root.board_name_list[38]
                        Label:
                            text: root.board_name_list[39]
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint: .3, 1
                        TextInput:
                            id: board_30
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_31
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_32
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_33
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_34
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_35
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_36
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_37
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_38
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                        TextInput:
                            id: board_39
                            padding_x: self.width/2
                            padding_y: self.height/4
                            on_text: root.update_padding(args[0])
                    Label:
                        size_hint: .1, 1
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint: .7, 1
                        Button:
                            text: 'SEND'
                            background_color: 0, .6156, .48235, 1
                            background_normal: ''
                            on_press: root.add_record()
                            on_release: root.app_stop_restart()
                        Label:
                            size_hint: 1,.1
                        Button:
                            text: 'CANCEL'
                            background_color: 0, .6156, .48235, 1
                            background_normal: ''
                            on_press: root.clear_button()
                        Label:
                            size_hint: 1,.1
                        Button:
                            id: button_read
                            text: 'READ'
                            background_color: 0, .6156, .48235, 1
                            background_normal: ''
                            on_press: root.read_records()
                        Label:
                            size_hint: 1,.1
                        Button:
                            text: 'EXIT'
                            background_color: 0, .6156, .48235, 1
                            background_normal: ''
                            on_press: root.update_count(), dupa
                    Label:
                        size_hint: .1,1
                Label:
                    size_hint: 1,.05

""")


class MainWindow(Screen):
    board_name_list = [ 'OSTRICH S S', 'OSTRICH M S', 'JUNKO M', 'CHAUMA M S', 'CHAUMA W S',
                        'BUNTING', 'WROBEL', 'FLAMINGO M S', 'FLAMINGO S S', 'FANTAIL',
                        'VERDIN S', 'STARLING', 'ERGET S S', 'ERGET M S', 'KAROO M S',
                        'KAROO M', 'FLAMINGO M', 'OSTRICH M', ' VERDIN M', 'ERGET M',
                        ' CHAUMA W', 'CHAUMA M', '', '', '',
                        '', '', '', '', '',
                        '', '', '', '', '',
                        '', '', '', '', '' ]

    def update_padding(self, text_input, *args):
        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width) / 2

    def add_record(self):

        global app_stop
        global read_timestamp

        client_name_id = self.ids['client_name']
        country_id = self.ids['country']
        adress_id = self.ids['adress']
        post_code_id = self.ids['post_code']
        invoice_id = self.ids['invoice']
        board_00_id = self.ids['board_00']
        board_01_id = self.ids['board_01']
        board_02_id = self.ids['board_02']
        board_03_id = self.ids['board_03']
        board_04_id = self.ids['board_04']
        board_05_id = self.ids['board_05']
        board_06_id = self.ids['board_06']
        board_07_id = self.ids['board_07']
        board_08_id = self.ids['board_08']
        board_09_id = self.ids['board_09']
        board_10_id = self.ids['board_10']
        board_11_id = self.ids['board_11']
        board_12_id = self.ids['board_12']
        board_13_id = self.ids['board_13']
        board_14_id = self.ids['board_14']
        board_15_id = self.ids['board_15']
        board_16_id = self.ids['board_16']
        board_17_id = self.ids['board_17']
        board_18_id = self.ids['board_18']
        board_19_id = self.ids['board_19']
        board_20_id = self.ids['board_20']
        board_21_id = self.ids['board_21']
        board_22_id = self.ids['board_22']
        board_23_id = self.ids['board_23']
        board_24_id = self.ids['board_24']
        board_25_id = self.ids['board_25']
        board_26_id = self.ids['board_26']
        board_27_id = self.ids['board_27']
        board_28_id = self.ids['board_28']
        board_29_id = self.ids['board_29']
        board_30_id = self.ids['board_30']
        board_31_id = self.ids['board_31']
        board_32_id = self.ids['board_32']
        board_33_id = self.ids['board_33']
        board_34_id = self.ids['board_34']
        board_35_id = self.ids['board_35']
        board_36_id = self.ids['board_36']
        board_37_id = self.ids['board_37']
        board_38_id = self.ids['board_38']
        board_39_id = self.ids['board_39']

        status_id = self.ids['status']

        label_client = self.ids['label_client']
        label_country = self.ids['label_country']
        label_adress = self.ids['label_adress']
        label_post_code = self.ids['label_post_code']
        label_invoice = self.ids['label_invoice']

        timestamp = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        new_name = client_name_id.text
        new_country = country_id.text
        new_adress = adress_id.text
        new_post_code = post_code_id.text
        new_invoice = invoice_id.text

        try:
            new_board_00 = int(board_00_id.text)
        except:
            new_board_00 = 0
        try:
            new_board_01 = int(board_01_id.text)
        except:
            new_board_01 = 0
        try:
            new_board_02 = int(board_02_id.text)
        except:
            new_board_02 = 0
        try:
            new_board_03 = int(board_03_id.text)
        except:
            new_board_03 = 0
        try:
            new_board_04 = int(board_04_id.text)
        except:
            new_board_04 = 0
        try:
            new_board_05 = int(board_05_id.text)
        except:
            new_board_05 = 0
        try:
            new_board_06 = int(board_06_id.text)
        except:
            new_board_06 = 0
        try:
            new_board_07 = int(board_07_id.text)
        except:
            new_board_07 = 0
        try:
            new_board_08 = int(board_08_id.text)
        except:
            new_board_08 = 0
        try:
            new_board_09 = int(board_09_id.text)
        except:
            new_board_09 = 0
        try:
            new_board_10 = int(board_10_id.text)
        except:
            new_board_10 = 0
        try:
            new_board_11 = int(board_11_id.text)
        except:
            new_board_11 = 0
        try:
            new_board_12 = int(board_12_id.text)
        except:
            new_board_12 = 0
        try:
            new_board_13 = int(board_13_id.text)
        except:
            new_board_13 = 0
        new_board_14 = 0  # jesli chcesz wiecej to musisz try expect
        new_board_15 = 0
        new_board_16 = 0
        new_board_17 = 0
        new_board_18 = 0
        new_board_19 = 0
        new_board_20 = 0
        new_board_21 = 0
        new_board_22 = 0
        new_board_23 = 0
        new_board_24 = 0
        new_board_25 = 0
        new_board_26 = 0
        new_board_27 = 0
        new_board_28 = 0
        new_board_29 = 0
        new_board_30 = 0
        new_board_31 = 0
        new_board_32 = 0
        new_board_33 = 0
        new_board_34 = 0
        new_board_35 = 0
        new_board_36 = 0
        new_board_37 = 0
        new_board_38 = 0
        new_board_39 = 0

        if (app_stop == 2):

            status_id = self.ids['status']
            to_remove = status_id.text

            result = collection_orders.delete_many({"order_number": to_remove})

            i = invoice_id.text

            if (new_invoice == ""):
                new_invoice = "NO"

            order_number = status_id.text

            new_data = {

                "timestamp": read_timestamp,
                "order_number": order_number,
                "name": new_name,
                "country": new_country,
                "adress": new_adress,
                "post_code": new_post_code,
                "invoice": i,
                "board00": new_board_00,
                "board01": new_board_01,
                "board02": new_board_02,
                "board03": new_board_03,
                "board04": new_board_04,
                "board05": new_board_05,
                "board06": new_board_06,
                "board07": new_board_07,
                "board08": new_board_08,
                "board09": new_board_09,
                "board10": new_board_10,
                "board11": new_board_11,
                "board12": new_board_12,
                "board13": new_board_13,

            }

            collection_orders.insert_one(new_data)
            status_id.text = "UPDATED"

            self.clear_all()
            self.update_count()
            button_read = self.ids['button_read']
            button_read.text = 'FIND'
            app_stop = 3

        if (app_stop == 0):

            label_client.text = "CLIENT NAME"
            label_country.text = "COUNTRY"
            label_adress.text = "ADRESS"
            label_post_code.text = "POST-CODE"
            label_invoice.text = "INVOICE"

            if (new_name == "" or new_country == "" or new_adress == "" or new_post_code == ""):

                status_id.text = 'FILL ALL'
            else:

                status_id.text = 'SENDING'

                if (new_invoice == ""):
                    new_invoice = "NO"

                year_number = str(datetime.datetime.now().strftime('%j'))
                time = str(datetime.datetime.now().strftime('%H%M%S'))
                order_number = year_number + time

                new_data = {

                    "timestamp": timestamp,
                    "order_number": order_number,
                    "name": new_name,
                    "country": new_country,
                    "adress": new_adress,
                    "post_code": new_post_code,
                    "invoice": new_invoice,
                    "board00": new_board_00,
                    "board01": new_board_01,
                    "board02": new_board_02,
                    "board03": new_board_03,
                    "board04": new_board_04,
                    "board05": new_board_05,
                    "board06": new_board_06,
                    "board07": new_board_07,
                    "board08": new_board_08,
                    "board09": new_board_09,
                    "board10": new_board_10,
                    "board11": new_board_11,
                    "board12": new_board_12,
                    "board13": new_board_13,

                }

                collection_orders.insert_one(new_data)

                status_id.text = order_number

                self.update_count()

                self.clear_all()

        elif (app_stop == 1):

            order_number_to_find = new_country

            data_to_edit = collection_orders.find_one({"order_number": order_number_to_find})

            label_client.text = "CLIENT NAME"
            label_country.text = "COUNTRY"
            label_adress.text = "ADRESS"
            label_post_code.text = "POST-CODE"
            label_invoice.text = "INVOICE"

            if (data_to_edit == None):

                status_id.text = 'NONE'
                app_stop = 0
                self.clear_all()

            else:

                status_id.text = order_number_to_find
                client_name_id.text = data_to_edit["name"]
                country_id.text = data_to_edit["country"]
                post_code_id.text = data_to_edit["post_code"]
                adress_id.text = data_to_edit["adress"]
                invoice_id.text = data_to_edit["invoice"]
                status_id.text = order_number_to_find
                board_00_id.text = str(data_to_edit["board00"])
                board_01_id.text = str(data_to_edit["board01"])
                board_02_id.text = str(data_to_edit["board02"])
                board_03_id.text = str(data_to_edit["board03"])
                board_04_id.text = str(data_to_edit["board04"])
                board_05_id.text = str(data_to_edit["board05"])
                board_06_id.text = str(data_to_edit["board06"])
                board_07_id.text = str(data_to_edit["board07"])
                board_08_id.text = str(data_to_edit["board08"])
                board_09_id.text = str(data_to_edit["board09"])
                board_10_id.text = str(data_to_edit["board10"])
                board_11_id.text = str(data_to_edit["board11"])
                board_12_id.text = str(data_to_edit["board12"])
                board_13_id.text = str(data_to_edit["board13"])

                read_timestamp = str(data_to_edit["timestamp"])

                button_read = self.ids['button_read']
                button_read.text = 'REMOVE'
                app_stop = 2

    def clear_button(self):

        global app_stop

        label_client = self.ids['label_client']
        label_country = self.ids['label_country']
        label_adress = self.ids['label_adress']
        label_post_code = self.ids['label_post_code']
        label_invoice = self.ids['label_invoice']

        if (app_stop != 0):
            label_client.text = "CLIENT NAME"
            label_country.text = "COUNTRY"
            label_adress.text = "ADRESS"
            label_post_code.text = "POST-CODE"
            label_invoice.text = "INVOICE"
            button_read = self.ids['button_read']
            button_read.text = 'FIND'
            app_stop = 0

        status_id = self.ids['status']
        self.clear_all()
        status_id.text = 'CLEARED'

    def clear_all(self):

        client_name_id = self.ids['client_name']
        country_id = self.ids['country']
        adress_id = self.ids['adress']
        post_code_id = self.ids['post_code']
        invoice_id = self.ids['invoice']
        board_00_id = self.ids['board_00']
        board_01_id = self.ids['board_01']
        board_02_id = self.ids['board_02']
        board_03_id = self.ids['board_03']
        board_04_id = self.ids['board_04']
        board_05_id = self.ids['board_05']
        board_06_id = self.ids['board_06']
        board_07_id = self.ids['board_07']
        board_08_id = self.ids['board_08']
        board_09_id = self.ids['board_09']
        board_10_id = self.ids['board_10']
        board_11_id = self.ids['board_11']
        board_12_id = self.ids['board_12']
        board_13_id = self.ids['board_13']
        board_14_id = self.ids['board_14']
        board_15_id = self.ids['board_15']
        board_16_id = self.ids['board_16']
        board_17_id = self.ids['board_17']
        board_18_id = self.ids['board_18']
        board_19_id = self.ids['board_19']
        board_20_id = self.ids['board_20']
        board_21_id = self.ids['board_21']
        board_22_id = self.ids['board_22']
        board_23_id = self.ids['board_23']
        board_24_id = self.ids['board_24']
        board_25_id = self.ids['board_25']
        board_26_id = self.ids['board_26']
        board_27_id = self.ids['board_27']
        board_28_id = self.ids['board_28']
        board_29_id = self.ids['board_29']
        board_30_id = self.ids['board_30']
        board_31_id = self.ids['board_31']
        board_32_id = self.ids['board_32']
        board_33_id = self.ids['board_33']
        board_34_id = self.ids['board_34']
        board_35_id = self.ids['board_35']
        board_36_id = self.ids['board_36']
        board_37_id = self.ids['board_37']
        board_38_id = self.ids['board_38']
        board_39_id = self.ids['board_39']

        client_name_id.text = ""
        country_id.text = ""
        adress_id.text = ""
        post_code_id.text = ""
        invoice_id.text = ""

        board_00_id.text = ""
        board_01_id.text = ""
        board_02_id.text = ""
        board_03_id.text = ""
        board_04_id.text = ""
        board_05_id.text = ""
        board_06_id.text = ""
        board_07_id.text = ""
        board_08_id.text = ""
        board_09_id.text = ""
        board_10_id.text = ""
        board_11_id.text = ""
        board_12_id.text = ""
        board_13_id.text = ""
        board_14_id.text = ""
        board_15_id.text = ""
        board_16_id.text = ""
        board_17_id.text = ""
        board_18_id.text = ""
        board_19_id.text = ""
        board_20_id.text = ""
        board_21_id.text = ""
        board_22_id.text = ""
        board_23_id.text = ""
        board_24_id.text = ""
        board_25_id.text = ""
        board_26_id.text = ""
        board_27_id.text = ""
        board_28_id.text = ""
        board_29_id.text = ""
        board_30_id.text = ""
        board_31_id.text = ""
        board_32_id.text = ""
        board_33_id.text = ""
        board_34_id.text = ""
        board_35_id.text = ""
        board_36_id.text = ""
        board_37_id.text = ""
        board_38_id.text = ""
        board_39_id.text = ""

    def update_count(self):

        board00 = collection_orders.find({"board00": {'$gt': 0}})
        board00_count = 0

        for doc in board00:
            board00_count = board00_count + int(doc['board00'])

        board01 = collection_orders.find({"board01": {'$gt': 0}})
        board01_count = 0

        for doc in board01:
            board01_count = board01_count + int(doc['board01'])

        board02 = collection_orders.find({"board02": {'$gt': 0}})
        board02_count = 0

        for doc in board02:
            board02_count = board02_count + int(doc['board02'])

        board03 = collection_orders.find({"board03": {'$gt': 0}})
        board03_count = 0

        for doc in board03:
            board03_count = board03_count + int(doc['board03'])

        board04 = collection_orders.find({"board04": {'$gt': 0}})
        board04_count = 0

        for doc in board04:
            board04_count = board04_count + int(doc['board04'])

        board04 = collection_orders.find({"board04": {'$gt': 0}})
        board04_count = 0

        for doc in board04:
            board04_count = board04_count + int(doc['board04'])

        board05 = collection_orders.find({"board05": {'$gt': 0}})
        board05_count = 0

        for doc in board05:
            board05_count = board05_count + int(doc['board05'])

        board06 = collection_orders.find({"board06": {'$gt': 0}})
        board06_count = 0

        for doc in board06:
            board06_count = board06_count + int(doc['board06'])

        board07 = collection_orders.find({"board07": {'$gt': 0}})
        board07_count = 0

        for doc in board07:
            board07_count = board07_count + int(doc['board07'])

        board08 = collection_orders.find({"board08": {'$gt': 0}})
        board08_count = 0

        for doc in board08:
            board08_count = board08_count + int(doc['board08'])

        board09 = collection_orders.find({"board09": {'$gt': 0}})
        board09_count = 0

        for doc in board09:
            board09_count = board09_count + int(doc['board09'])

        board10 = collection_orders.find({"board10": {'$gt': 0}})
        board10_count = 0

        for doc in board10:
            board10_count = board10_count + int(doc['board10'])

        board11 = collection_orders.find({"board11": {'$gt': 0}})
        board11_count = 0

        for doc in board11:
            board11_count = board11_count + int(doc['board11'])

        board12 = collection_orders.find({"board12": {'$gt': 0}})
        board12_count = 0

        for doc in board12:
            board12_count = board12_count + int(doc['board12'])

        board13 = collection_orders.find({"board13": {'$gt': 0}})
        board13_count = 0

        for doc in board13:
            board13_count = board13_count + int(doc['board13'])

        # ----------------------------------------------------------------------------

        board14 = collection_orders.find({"board14": {'$gt': 0}})
        board14_count = 0

        for doc in board14:
            board14_count = board14_count + int(doc['board14'])

        board15 = collection_orders.find({"board15": {'$gt': 0}})
        board15_count = 0

        for doc in board15:
            board15_count = board15_count + int(doc['board15'])

        board16 = collection_orders.find({"board16": {'$gt': 0}})
        board16_count = 0

        for doc in board16:
            board16_count = board16_count + int(doc['board16'])

        board17 = collection_orders.find({"board17": {'$gt': 0}})
        board17_count = 0

        for doc in board17:
            board17_count = board17_count + int(doc['board17'])

        board18 = collection_orders.find({"board18": {'$gt': 0}})
        board18_count = 0

        for doc in board18:
            board18_count = board18_count + int(doc['board18'])

        board19 = collection_orders.find({"board19": {'$gt': 0}})
        board19_count = 0

        for doc in board19:
            board19_count = board19_count + int(doc['board19'])

        board20 = collection_orders.find({"board20": {'$gt': 0}})
        board20_count = 0

        for doc in board20:
            board20_count = board20_count + int(doc['board20'])

        board21 = collection_orders.find({"board21": {'$gt': 0}})
        board21_count = 0

        for doc in board21:
            board21_count = board21_count + int(doc['board21'])

        # -------------------------------16.02.2017-----------------------------------

        collecttion_stock_count.delete_many({})

        stock_data = {

            "board00": board00_count,
            "board01": board01_count,
            "board02": board02_count,
            "board03": board03_count,
            "board04": board04_count,
            "board05": board05_count,
            "board06": board06_count,
            "board07": board07_count,
            "board08": board08_count,
            "board09": board09_count,
            "board10": board10_count,
            "board11": board11_count,
            "board12": board12_count,
            "board13": board13_count,
            "board14": board14_count,
            "board15": board15_count,
            "board16": board16_count,
            "board17": board17_count,
            "board18": board18_count,
            "board19": board19_count,
            "board20": board20_count,
            "board21": board21_count

        }

        collecttion_stock_count.insert_one(stock_data)

    def read_records(self):

        global app_stop

        if (app_stop == 0):
            client_name_id = self.ids['client_name']
            country_id = self.ids['country']
            adress_id = self.ids['adress']
            post_code_id = self.ids['post_code']
            invoice_id = self.ids['invoice']
            board_00_id = self.ids['board_00']
            board_01_id = self.ids['board_01']
            board_02_id = self.ids['board_02']
            board_03_id = self.ids['board_03']
            board_04_id = self.ids['board_04']
            board_05_id = self.ids['board_05']
            board_06_id = self.ids['board_06']
            board_07_id = self.ids['board_07']
            board_08_id = self.ids['board_08']
            board_09_id = self.ids['board_09']
            board_10_id = self.ids['board_10']
            board_11_id = self.ids['board_11']
            board_12_id = self.ids['board_12']
            board_13_id = self.ids['board_13']
            board_14_id = self.ids['board_14']
            board_15_id = self.ids['board_15']
            board_16_id = self.ids['board_16']
            board_17_id = self.ids['board_17']
            board_18_id = self.ids['board_18']
            board_19_id = self.ids['board_19']
            board_20_id = self.ids['board_20']
            board_21_id = self.ids['board_21']
            board_22_id = self.ids['board_22']
            board_23_id = self.ids['board_23']
            board_24_id = self.ids['board_24']
            board_25_id = self.ids['board_25']
            board_26_id = self.ids['board_26']
            board_27_id = self.ids['board_27']
            board_28_id = self.ids['board_28']
            board_29_id = self.ids['board_29']
            board_30_id = self.ids['board_30']
            board_31_id = self.ids['board_31']
            board_32_id = self.ids['board_32']
            board_33_id = self.ids['board_33']
            board_34_id = self.ids['board_34']
            board_35_id = self.ids['board_35']
            board_36_id = self.ids['board_36']
            board_37_id = self.ids['board_37']
            board_38_id = self.ids['board_38']
            board_39_id = self.ids['board_39']

            status_id = self.ids['status']

            self.clear_all()

            label_client = self.ids['label_client']
            label_country = self.ids['label_country']
            label_adress = self.ids['label_adress']
            label_post_code = self.ids['label_post_code']
            label_invoice = self.ids['label_invoice']

            status_id.text = '<- FILL'
            label_client.text = ""
            label_country.text = "ORDER NUMBER"
            label_adress.text = ""
            label_post_code.text = ""
            label_invoice.text = ""

            app_stop = 1

        if (app_stop == 2):
            status_id = self.ids['status']

            to_remove = status_id.text
            result = collection_orders.delete_many({"order_number": to_remove})

            button_read = self.ids['button_read']
            button_read.text = 'FIND'
            app_stop = 0
            status_id.text = "REMOVED"
            self.update_count()
            self.clear_all()

    def app_stop_restart(self):

        global app_stop

        if (app_stop == 3):
            app_stop = 0


class ScanApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    ScanApp().run()

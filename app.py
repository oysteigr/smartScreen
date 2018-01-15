#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import time

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from ping import PingService

WIDTH = 1024
HEIGHT = 600

BOX_SIZE = 30

YELLOW = (1, .7, 0)
ORANGE = (1, .45, 0)
RED = (1, 0, 0)
GREEN = (0, 1, 0)
WHITE = (1, 1, 1)

ipMap = {"KG": "192.168.1.84",
         "ØG": "192.168.1.126",
         "SG": "192.168.1.153",
         #"TS": "192.168.1.154",
         #"PS": "192.168.1.155",
         #"IG": "192.168.1.156",
         "HH": "192.168.1.124",
         "OF": "192.168.1.161"
         }

def draw_background(widget, y_pos, thickness, *args):
    with widget.canvas.before:
        Color(.4, .4, .4, 1)
        Rectangle(pos=(0, y_pos), size=(WIDTH, thickness))

class OnlineStatus:
    def __init__(self, ipMap):
        self.ipMap = ipMap
        self.pingService = PingService(ipMap)
        self.onlineMap = {}
        Clock.schedule_interval(self.updateStatus, 10)

    def updateStatus(self, *largs):
        self.onlineMap = self.pingService.pingAndParseResult(self.onlineMap)

    def getSecondsSinceOnline(self, key):
        if len(self.onlineMap.items()) == 0:
            return -1
        elif self.onlineMap.keys().__contains__(key):
            return self.onlineMap[key]
        else:
            return -1


class IncrediblyCrudeClock(Label):
    def update(self, *args):
        self.text = time.strftime("%d. %B - %H:%M:%S")


class PersonOnline(AnchorLayout):
    def __init__(self, initials, **kwargs):
        super().__init__(**kwargs)
        self.backgroundColor = Label()
        self.frontText = Label(text=initials)
        self.add_widget(self.backgroundColor)
        self.add_widget(self.frontText)
        self.onlineStatus = OnlineStatus(ipMap)
        Clock.schedule_interval(self.update, 2)

    def update(self, *args):
        self.backgroundColor.canvas.clear()
        timestampLastOnline = self.onlineStatus.getSecondsSinceOnline(self.frontText.text)
        if timestampLastOnline == -1:
            return
        secondsSinceOnline = time.time() - timestampLastOnline
        with self.backgroundColor.canvas:
            if secondsSinceOnline < 60:
                Color(*GREEN, 0.5)
            elif secondsSinceOnline < 3600:
                Color(*YELLOW, 0.5)
            else:
                Color(*RED, 0.5)
            RoundedRectangle(pos=self.getPos(BOX_SIZE, BOX_SIZE), size=(BOX_SIZE, BOX_SIZE), radius=[20, 20, 20, 20])

    def getPos(self, size_x, size_y):
        x = self.pos[0] + self.size[0] / 2 - size_x / 2
        y = self.pos[1] + self.size[1] / 2 - size_y / 2
        return x, y


class InfoSkjerm(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from kivy.config import Config
        Config.set('graphics', 'width', WIDTH)
        Config.set('graphics', 'height', HEIGHT)

    def build(self):
        onlines = GridLayout(rows=2, size_hint=(0.25, 1))

        onlines.add_widget(PersonOnline('KG'))
        onlines.add_widget(PersonOnline('ØG'))
        onlines.add_widget(PersonOnline('HH'))
        onlines.add_widget(PersonOnline('OF'))
        onlines.add_widget(PersonOnline('SG'))
        # onlines.add_widget(PersonOnline('IG'))
        # onlines.add_widget(PersonOnline('TS'))
        # onlines.add_widget(PersonOnline('PS'))

        status = Label(text='status', size_hint=(0.25, 1))

        clock = IncrediblyCrudeClock(font_size='38sp', size_hint=(0.5, 1))
        Clock.schedule_interval(clock.update, 1)

        header = BoxLayout(size_hint=(1, 0.15))
        header.add_widget(onlines)
        header.add_widget(clock)
        header.add_widget(status)


        trikk1_name = Label(text='11 - Galgeberg'.upper(), size_hint=(0.2, 0.05),
                            valign='middle', halign='left', underline=True, padding_x=15)
        trikk1_name.bind(size=trikk1_name.setter('text_size'))
        trikk1_times = GridLayout(rows=1, size_hint=(0.8, 0.05))
        trikk2_name = Label(text='11 - Skøyen'.upper(), size_hint=(0.2, 0.05),
                            valign='middle', halign='left', underline=True, padding_x=15)
        trikk2_name.bind(size=trikk2_name.setter('text_size'))
        trikk2_times = GridLayout(rows=1, size_hint=(0.8, 0.05))
        trikk3_name = Label(text='12 - Helsfyr'.upper(), size_hint=(0.2, 0.05),
                            valign='middle', halign='left', underline=True, padding_x=15)
        trikk3_name.bind(size=trikk3_name.setter('text_size'))
        trikk3_times = GridLayout(rows=1, size_hint=(0.8, 0.05))
        trikk4_name = Label(text='12 - Tjuvholmen'.upper(), size_hint=(0.2, 0.05),
                            valign='middle', halign='left', underline=True, padding_x=15)
        trikk4_name.bind(size=trikk4_name.setter('text_size'))
        trikk4_times = GridLayout(rows=1, size_hint=(0.8, 0.05))
        trikk5_name = Label(text='13 - Nydalen'.upper(), size_hint=(0.2, 0.05),
                            valign='middle', halign='left', underline=True, padding_x=15)
        trikk5_name.bind(size=trikk5_name.setter('text_size'))
        trikk5_times = GridLayout(rows=1, size_hint=(0.8, 0.05))
        trikk6_name = Label(text='13 - Bygdøy'.upper(), size_hint=(0.2, 0.05),
                            valign='middle', halign='left', underline=True, padding_x=15)
        trikk6_name.bind(size=trikk6_name.setter('text_size'))
        trikk6_times = GridLayout(rows=1, size_hint=(0.8, 0.05))
        buss1_name = Label(text='20 - Galgeberg'.upper(), size_hint=(0.2, 0.05),
                           valign='middle', halign='left', underline=True, padding_x=15)
        buss1_name.bind(size=buss1_name.setter('text_size'))
        buss1_times = GridLayout(rows=1, size_hint=(0.8, 0.05))
        buss2_name = Label(text='20 - Skøyen'.upper(), size_hint=(0.2, 0.05),
                           valign='middle', halign='left', underline=True, padding_x=15)
        buss2_name.bind(size=buss2_name.setter('text_size'))
        buss2_times = GridLayout(rows=1, size_hint=(0.8, 0.05))
        buss3_name = Label(text='21 - Helsfyr'.upper(), size_hint=(0.2, 0.05),
                           valign='middle', halign='left', underline=True, padding_x=15)
        buss3_name.bind(size=buss3_name.setter('text_size'))
        buss3_times = GridLayout(rows=1, size_hint=(0.8, 0.05))
        buss4_name = Label(text='21 - Tjuvholmen'.upper(), size_hint=(0.2, 0.05),
                           valign='middle', halign='left', underline=True, padding_x=15)
        buss4_name.bind(size=buss4_name.setter('text_size'))
        buss4_times = GridLayout(rows=1, size_hint=(0.8, 0.05))
        buss5_name = Label(text='30 - Nydalen'.upper(), size_hint=(0.2, 0.05),
                           valign='middle', halign='left', underline=True, padding_x=15)
        buss5_name.bind(size=buss5_name.setter('text_size'))
        buss5_times = GridLayout(rows=1, size_hint=(0.8, 0.05))
        buss6_name = Label(text='30 - Bygdøy'.upper(), size_hint=(0.2, 0.05),
                           valign='middle', halign='left', underline=True, padding_x=15)
        buss6_name.bind(size=buss6_name.setter('text_size'))
        buss6_times = GridLayout(rows=1, size_hint=(0.8, 0.05))

        for i in range(1, 6):
            trikk1_times.add_widget(Label(text=str(i * 6) + ' min'))
            trikk2_times.add_widget(Label(text=str(i * 6 + 1) + ' min'))
            trikk3_times.add_widget(Label(text=str(i * 6 + 2) + ' min'))
            trikk4_times.add_widget(Label(text=str(i * 6 + 3) + ' min'))
            trikk5_times.add_widget(Label(text=str(i * 6 + 4) + ' min'))
            trikk6_times.add_widget(Label(text=str(i * 6 + 5) + ' min'))
            buss1_times.add_widget(Label(text=str(i * 6 + 6) + ' min'))
            buss2_times.add_widget(Label(text=str(i * 6 + 7) + ' min'))
            buss3_times.add_widget(Label(text=str(i * 6 + 8) + ' min'))
            buss4_times.add_widget(Label(text=str(i * 6 + 9) + ' min'))
            buss5_times.add_widget(Label(text=str(i * 6 + 1) + ' min'))
            buss6_times.add_widget(Label(text=str(i * 6 + 2) + ' min'))

        body = GridLayout(cols=2, size_hint=(1, 0.85))

        body.add_widget(trikk1_name)
        body.add_widget(trikk1_times)
        body.add_widget(trikk2_name)
        body.add_widget(trikk2_times)
        body.add_widget(trikk3_name)
        body.add_widget(trikk3_times)
        body.add_widget(trikk4_name)
        body.add_widget(trikk4_times)
        body.add_widget(trikk5_name)
        body.add_widget(trikk5_times)
        body.add_widget(trikk6_name)
        body.add_widget(trikk6_times)
        body.add_widget(buss1_name)
        body.add_widget(buss1_times)
        body.add_widget(buss2_name)
        body.add_widget(buss2_times)
        body.add_widget(buss3_name)
        body.add_widget(buss3_times)
        body.add_widget(buss4_name)
        body.add_widget(buss4_times)
        body.add_widget(buss5_name)
        body.add_widget(buss5_times)
        body.add_widget(buss6_name)
        body.add_widget(buss6_times)

        root = BoxLayout(orientation='vertical')
        root.add_widget(header)
        root.add_widget(body)

        draw_background(root, 600 * 0.85, 3)
        draw_background(root, 1 * ((600 * 0.85) / 12), 1)
        draw_background(root, 2 * ((600 * 0.85) / 12), 1)
        draw_background(root, 3 * ((600 * 0.85) / 12), 1)
        draw_background(root, 4 * ((600 * 0.85) / 12), 1)
        draw_background(root, 5 * ((600 * 0.85) / 12), 1)
        draw_background(root, 6 * ((600 * 0.85) / 12), 1)
        draw_background(root, 7 * ((600 * 0.85) / 12), 1)
        draw_background(root, 8 * ((600 * 0.85) / 12), 1)
        draw_background(root, 9 * ((600 * 0.85) / 12), 1)
        draw_background(root, 10 * ((600 * 0.85) / 12), 1)
        draw_background(root, 11 * ((600 * 0.85) / 12), 1)

        return root


if __name__ == '__main__':
    InfoSkjerm().run()
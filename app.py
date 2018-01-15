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

TRANSPORT_SIZE = 34
LINE_THICKNESS = 1

YELLOW = (1, .7, 0)
ORANGE = (1, .45, 0)
RED = (1, 0, 0)
BLUE = (0.2, 0.2, 1)
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
            if secondsSinceOnline < 300:
                Color(*GREEN, 0.5)
            elif secondsSinceOnline < 3600:
                Color(*YELLOW, 0.5)
            elif secondsSinceOnline < 36000:
                Color(*RED, 0.5)
            RoundedRectangle(pos=self.getPos(BOX_SIZE, BOX_SIZE), size=(BOX_SIZE, BOX_SIZE), radius=[20, 20, 20, 20])

    def getPos(self, size_x, size_y):
        x = self.pos[0] + self.size[0] / 2 - size_x / 2
        y = self.pos[1] + self.size[1] / 2 - size_y / 2
        return x, y

class TransportTab(GridLayout):
    def __init__(self, number, heading, source, tram, **kwargs):
        super().__init__(**kwargs)
        self.tram = tram
        self.source_place = Label(text=source.upper(),
                                   valign='middle', halign='right', underline=False)
        self.source_place.bind(size=self.source_place.setter('text_size'))
        self.backgroundColor = Label()
        self.number = Label(text=number.upper(),
                           valign='middle', underline=True)
        self.heading_place = Label(text=heading.upper(),
                           valign='middle', underline=True)
        self.heading_place.bind(size=self.heading_place.setter('text_size'))
        self.add_widget(self.source_place)
        self.add_widget(self.number)
        self.number.add_widget(self.backgroundColor)

        self.add_widget(self.heading_place)
        Clock.schedule_interval(self.update, 4)
        self.update()

        self.times = []

        for i in range(1, 6):
            self.times.append(Label(text=str(i * 6) + ' min'))
            self.add_widget(self.times[i-1])

    def update(self, *args):
        self.backgroundColor.canvas.clear()
        with self.backgroundColor.canvas:
            if self.tram:
                Color(*BLUE, 0.5)
            else:
                Color(*RED, 0.5)
            RoundedRectangle(pos=self.getPos(TRANSPORT_SIZE, TRANSPORT_SIZE), size=(TRANSPORT_SIZE, TRANSPORT_SIZE), radius=[30, 0, 30, 0])
            Rectangle(pos=self.getLinePos(), size=(2000, LINE_THICKNESS))
            Rectangle(pos=self.getLinePosStart(), size=(self.getPos(TRANSPORT_SIZE, TRANSPORT_SIZE)[0], LINE_THICKNESS))

    def getPos(self, size_x, size_y):
        x = self.number.pos[0] + self.number.size[0] / 2 - size_x / 2
        y = self.number.pos[1] + self.number.size[1] / 2 - size_y / 2
        return x, y

    def getLinePos(self):
        x = self.number.pos[0] + self.number.size[0] / 2 + TRANSPORT_SIZE / 2
        y = self.number.pos[1] + self.number.size[1] / 2 + TRANSPORT_SIZE / 2 - LINE_THICKNESS
        return x, y

    def getLinePosStart(self):
        x = 0
        y = self.number.pos[1] + self.number.size[1] / 2 - TRANSPORT_SIZE / 2 + LINE_THICKNESS
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

        trikk_1 = TransportTab('11', 'Kjelsås', 'Birkelunden', True, rows=1, size_hint=(0.8, 0.05))
        trikk_2 = TransportTab('11', 'Majorstua', 'Birkelunden', True, rows=1, size_hint=(0.8, 0.05))
        trikk_3 = TransportTab('12', 'Kjelsås', 'Birkelunden', True, rows=1, size_hint=(0.8, 0.05))
        trikk_4 = TransportTab('12', 'Majorstua', 'Birkelunden', True, rows=1, size_hint=(0.8, 0.05))
        trikk_5 = TransportTab('13', 'Storo-Grefsen', 'Birkelunden', True, rows=1, size_hint=(0.8, 0.05))
        trikk_6 = TransportTab('13', 'Lilleaker', 'Birkelunden', True, rows=1, size_hint=(0.8, 0.05))
        bus_1 = TransportTab('20', 'Skøyen', 'Kjøpenhavnsg.', False, rows=1, size_hint=(0.8, 0.05))
        bus_2 = TransportTab('20', 'Galgeberg', 'Kjøpenhavnsg.', False, rows=1, size_hint=(0.8, 0.05))
        bus_3 = TransportTab('21', 'Helsfyr', 'Kjøpenhavnsg.', False, rows=1, size_hint=(0.8, 0.05))
        bus_4 = TransportTab('21', 'Tjuvholmen', 'Sannergata', False, rows=1, size_hint=(0.8, 0.05))
        bus_5 = TransportTab('30', 'Nydalen', 'Dælenenga', False, rows=1, size_hint=(0.8, 0.05))
        bus_6 = TransportTab('30', 'Bygdøy', 'Birkelunden', False, rows=1, size_hint=(0.8, 0.05))

        body = GridLayout(cols=1, size_hint=(1, 0.85))

        body.add_widget(trikk_1)
        body.add_widget(trikk_2)
        body.add_widget(trikk_3)
        body.add_widget(trikk_4)
        body.add_widget(trikk_5)
        body.add_widget(trikk_6)
        body.add_widget(bus_1)
        body.add_widget(bus_2)
        body.add_widget(bus_3)
        body.add_widget(bus_4)
        body.add_widget(bus_5)
        body.add_widget(bus_6)

        root = BoxLayout(orientation='vertical')
        root.add_widget(header)
        root.add_widget(body)



        return root


if __name__ == '__main__':
    InfoSkjerm().run()
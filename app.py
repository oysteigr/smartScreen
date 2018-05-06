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
from ruterService import RuterService

WIDTH = 800
HEIGHT = 480

BOX_SIZE = 30

TRANSPORT_SIZE = 34
LINE_THICKNESS = 2

YELLOW = (1.0, 0.9, 0.0)
ORANGE = (1.0, 0.45, 0.0)
RED = (1.0, 0.0, 0.0)
BLUE = (0.2, 0.2, 1.0)
GREEN = (0.0, 1.0, 0.0)
WHITE = (1.0, 1.0, 1.0)
BLACK = (0.0, 0.0, 0.0)

GREEN_TIMEOUT = 5*60
YELLOW_TIMEOUT = 10*60
RED_TIMEOUT = 8*60*60
BLACK_TIMEOUT = 24*60*60
VISIBILITY_TIMEOUT = 24*60*60*7


ipMap = {"KG": "192.168.1.126",
         "ØG": "192.168.1.58",
         "SG": "192.168.1.153",
         "HH": "192.168.1.124",
         "OF": "192.168.1.161",
         "KS": "192.168.1.28"
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
        self.show = False
        Clock.schedule_interval(self.update, 2)

    def update(self, *args):
        self.backgroundColor.canvas.clear()
        timestampLastOnline = self.onlineStatus.getSecondsSinceOnline(self.frontText.text)
        if timestampLastOnline == -1:
            return
        secondsSinceOnline = time.time() - timestampLastOnline
        with self.backgroundColor.canvas:
            if secondsSinceOnline < GREEN_TIMEOUT:
                Color(*GREEN, 0.5)
                self.show = True
            elif secondsSinceOnline < YELLOW_TIMEOUT:
                a = (secondsSinceOnline-GREEN_TIMEOUT)/YELLOW_TIMEOUT
                colour = (GREEN[0] * (1.0 - a) + YELLOW[0] * a,
                          GREEN[1] * (1.0 - a) + YELLOW[1] * a,
                          GREEN[2] * (1.0 - a) + YELLOW[2] * a)
                Color(*colour, 0.5)
            elif secondsSinceOnline < RED_TIMEOUT:
                a = (secondsSinceOnline-YELLOW_TIMEOUT)/RED_TIMEOUT
                colour = (YELLOW[0] * (1.0 - a) + RED[0] * a,
                          YELLOW[1] * (1.0 - a) + RED[1] * a,
                          YELLOW[2] * (1.0 - a) + RED[2] * a)
                Color(*colour, 0.5)
            elif secondsSinceOnline < BLACK_TIMEOUT:
                a = (secondsSinceOnline-RED_TIMEOUT)/BLACK_TIMEOUT
                colour = (RED[0] * (1.0 - a) + BLACK[0] * a,
                          RED[1] * (1.0 - a) + BLACK[1] * a,
                          RED[2] * (1.0 - a) + BLACK[2] * a)
                Color(*colour, 0.5)
            elif secondsSinceOnline < VISIBILITY_TIMEOUT:
                Color(*BLACK, 0.5)
            else:
                self.show = False

            RoundedRectangle(pos=self.getPos(BOX_SIZE, BOX_SIZE), size=(BOX_SIZE, BOX_SIZE), radius=[20, 20, 20, 20])

    def getPos(self, size_x, size_y):
        x = self.pos[0] + self.size[0] / 2 - size_x / 2
        y = self.pos[1] + self.size[1] / 2 - size_y / 2
        return x, y


class TransportTab(GridLayout):
    def __init__(self, number, tram, stopId, direction, **kwargs):
        super().__init__(rows=2, size_hint=(1, 1), **kwargs)
        self.tram = tram
        self.backgroundColor = Label()
        self.number = Label(text=number.upper(), size_hint=(0.2, 1), font_size='30',
                            valign='middle', underline=False, font_name='BebasNeue Regular.ttf')
        self.heading_place = Label(text='-', font_size='18', size_hint=(0.8, 1),
                                   valign='middle', underline=True, font_name='BebasNeue Regular.ttf')
        self.heading_place.bind(size=self.heading_place.setter('text_size'))

        self.header = BoxLayout(size_hint=(1, 0.15))
        self.header.add_widget(self.number)
        self.number.add_widget(self.backgroundColor)

        self.header.add_widget(self.heading_place)

        self.ruter_service = RuterService(number, stopId, direction)

        self.body = BoxLayout(size_hint=(1, 0.85))

        self.times = []

        self.next_times = GridLayout(rows=3, size_hint=(0.3, 1))

        self.times.append(Label(text='-', font_size='70', font_name='BebasNeue Regular.ttf', halign='right'))
        self.next = BoxLayout(size_hint=(0.7, 1))
        self.next.add_widget(self.times[0])

        for i in range(1, 4):
            self.times.append(Label(text='-', font_name='BebasNeue Regular.ttf', font_size='25'))
            self.next_times.add_widget(self.times[i])

        self.body.add_widget(self.next)
        self.body.add_widget(self.next_times)

        self.add_widget(self.header)
        self.add_widget(self.body)

        Clock.schedule_interval(self.update_times, 2)
        Clock.schedule_interval(self.refresh_times, 10)
        Clock.schedule_interval(self.update, 10)
        Clock.schedule_interval(self.set_names, 10)

        self.update()
        self.ruter_service.refresh()
        self.set_names()

    def set_names(self, *args):
        if self.heading_place.text == '-':
            self.heading_place.text = self.ruter_service.getDestName()

    def refresh_times(self, *args):
        self.ruter_service.refresh()

    def update_times(self, *args):
        times_strings = self.ruter_service.getNextDeparturesInText(5)
        for i in range(0, 4):
            if len(times_strings) > i:
                self.times[i].text = times_strings[i]
            else:
                self.times[i].text = ''

    def update(self, *args):
        self.backgroundColor.canvas.clear()
        with self.backgroundColor.canvas:
            if self.tram:
                Color(*BLUE, 0.5)
            else:
                Color(*RED, 0.5)
            RoundedRectangle(pos=self.getPos(TRANSPORT_SIZE, TRANSPORT_SIZE), size=(TRANSPORT_SIZE, TRANSPORT_SIZE), radius=[0, 0, 0, 0])
            Rectangle(pos=self.getLinePos(), size=(150, LINE_THICKNESS))

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

        self.onlines = GridLayout(rows=1, size_hint=(0.25, 1))

        Clock.schedule_interval(self.update, 5)
        self.persons = []
        self.persons.append(PersonOnline('KG'))
        self.persons.append(PersonOnline('ØG'))
        self.persons.append(PersonOnline('HH'))
        self.persons.append(PersonOnline('OF'))
        self.persons.append(PersonOnline('SG'))
        self.persons.append(PersonOnline('KS'))

    def update(self, *args):
        self.onlines.clear_widgets()

        for person in self.persons:
            if person.show:
                self.onlines.add_widget(person)


    def build(self):



        status = Label(text='status', size_hint=(0.25, 1))

        clock = IncrediblyCrudeClock(font_size='38sp', size_hint=(0.5, 1))
        Clock.schedule_interval(clock.update, 1)

        header = BoxLayout(size_hint=(1, 0.15))
        header.add_widget(self.onlines)
        header.add_widget(clock)
        header.add_widget(status)

        trikk_1 = TransportTab('11', True, '3010520', '1')
        trikk_2 = TransportTab('11', True, '3010520', '2')
        trikk_3 = TransportTab('12', True, '3010520', '1')
        trikk_4 = TransportTab('12', True, '3010520', '2')
        trikk_5 = TransportTab('13', True, '3010520', '1')
        trikk_6 = TransportTab('13', True, '3010520', '2')
        bus_1 = TransportTab('20', False, '3010525', '2')
        bus_2 = TransportTab('20', False, '3010525', '1')
        bus_3 = TransportTab('21', False, '3010525', '1')
        bus_4 = TransportTab('21', False, '3010521', '2')
        bus_5 = TransportTab('30', False, '3010524', '1')
        bus_6 = TransportTab('30', False, '3010519', '2')

        body = GridLayout(cols=4, size_hint=(1, 0.85))

        body.add_widget(trikk_2)
        body.add_widget(trikk_4)
        body.add_widget(trikk_6)
        body.add_widget(bus_1)
        body.add_widget(bus_4)
        body.add_widget(bus_6)

        body.add_widget(trikk_1)
        body.add_widget(trikk_3)
        body.add_widget(trikk_5)
        body.add_widget(bus_2)
        body.add_widget(bus_3)
        body.add_widget(bus_5)

        root = BoxLayout(orientation='vertical')
        root.add_widget(header)
        root.add_widget(body)



        return root


if __name__ == '__main__':
    InfoSkjerm().run()
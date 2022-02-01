from abc import ABC, abstractmethod
from graphics_and_games_klassen import Kreis
from intern.zeichenfenster import Zeichenfenster
import math


class Planet(ABC, Kreis):
    @property
    def Name(self):
        return self._Name

    @Name.setter
    def Name(self, name: str):
        self._Name = name

    @property
    def FarbeHuelle(self):
        return self._FarbeHuelle

    @FarbeHuelle.setter
    def FarbeHuelle(self, farbe: str):
        self._FarbeHuelle = farbe

    @property
    def Dickehuelle(self):
        return self._Dickehuelle

    @Dickehuelle.setter
    def Dickehuelle(self, farbe: float):
        self._Dickehuelle = farbe

    @property
    def Umlaufgeschwindigkeit(self):
        return self._Umlaufgeschwindigkeit

    @Umlaufgeschwindigkeit.setter
    def Umlaufgeschwindigkeit(self, geschwindigkeit: float):
        self._Umlaufgeschwindigkeit = geschwindigkeit

    @property
    def UmlaufWinkel(self):
        return self._UmlaufWinkel

    @UmlaufWinkel.setter
    def UmlaufWinkel(self, winkel: float):
        self._UmlaufWinkel = winkel

    @property
    def Bahnradius(self):
        return self._Bahnradius

    @Bahnradius.setter
    def Bahnradius(self, radius: float):
        self._Bahnradius = radius

    def NachRechtsVerschieben(self, anzahlPixel):
        self.PositionSetzen(self.x + anzahlPixel, self.y)

    def AktionAusfuehren(self):
        neuesX = math.cos(self.UmlaufWinkel) * self.Bahnradius + Zeichenfenster().FENSTERBREITE/2
        neuesY = math.sin(self.UmlaufWinkel) * self.Bahnradius + Zeichenfenster().FENSTERHOEHE/2
        self.PositionSetzen(neuesX, neuesY)
        self.WinkelAktualisieren()

    def WinkelAktualisieren(self):
        self.UmlaufWinkel += self.Umlaufgeschwindigkeit


class Gesteinsplanet(Planet):
    def __init__(self, name, radius=10.0, farbe="blau", umlaufgeschwindigkeit=0.05, bahnradius=100.0):
        super().__init__()
        Zeichenfenster().BeobachterRegistrieren(self)
        self.UmlaufWinkel = 0
        self.Name = name
        self.Umlaufgeschwindigkeit = umlaufgeschwindigkeit
        self.Bahnradius = bahnradius
        self.PositionSetzen(Zeichenfenster().FENSTERBREITE/2+self.Bahnradius, Zeichenfenster().FENSTERHOEHE/2)
        self.FarbeSetzen(farbe)
        self.RadiusSetzen(radius)


class Gasplanet(Planet):
    pass

from abc import ABC
from graphics_and_games_klassen import Kreis
from intern.zeichenfenster import Zeichenfenster


class Planet(ABC, Kreis):
    Name: str
    Radius: float
    Farbe: str
    FarbeHuelle: str
    Dickehuelle: str
    Umlaufgeschwindigkeit: float
    UmlaufWinkel: float
    Bahnradius: float


class Gesteinsplanet(Planet):
    def __init__(self, name, radius = 10.0, farbe="blau", umlaufgeschwindigkeit=5.0, bahnradius=100.0 ):
        super().__init__()
        Zeichenfenster().BeobachterRegistrieren(self)
        self.Name = name
        self.Radius = radius
        self.Farbe = farbe
        self.Umlaufgeschwindigkeit = umlaufgeschwindigkeit
        self.Bahnradius = bahnradius
        self.PositionSetzen(100,100)
        self.FarbeSetzen(self.Farbe)


    def AktionAusfuehren(self):
        print("Test")


class Gasplanet(Planet):
    pass

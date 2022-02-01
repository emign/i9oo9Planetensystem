from intern.zeichenfenster import Zeichenfenster
from graphics_and_games_klassen import Kreis
from Planeten import Gesteinsplanet, Gasplanet

sonne = Kreis()
sonne.RadiusSetzen(35.0)
sonne.FarbeSetzen("gelb")
sonne.PositionSetzen(Zeichenfenster().FENSTERBREITE/2, Zeichenfenster().FENSTERHOEHE/2)
merkur = Gesteinsplanet(name="Merkus", radius=6.0, farbe="braun", bahnradius=50, umlaufgeschwindigkeit=0.03)
venus = Gesteinsplanet(name="Venus", radius=10.0, farbe="lila", bahnradius=120, umlaufgeschwindigkeit=0.03)
erde = Gesteinsplanet(name="Erde", radius=15.0, farbe="blau", bahnradius=180, umlaufgeschwindigkeit=0.01)
mars = Gesteinsplanet(name="Mars", radius=15.0, farbe="rot", bahnradius=180, umlaufgeschwindigkeit=0.02)
jupiter = Gasplanet(name="Jupiter", radius=30.0, farbe="grün", bahnradius=250, umlaufgeschwindigkeit=0.01)
Zeichenfenster().run()

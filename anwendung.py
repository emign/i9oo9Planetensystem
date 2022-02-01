from intern.zeichenfenster import Zeichenfenster
from Planeten import Gesteinsplanet

merkur = Gesteinsplanet(name="Merkus", radius=6.0, farbe="braun", bahnradius=30)
venus = Gesteinsplanet(name="Venus", radius=10.0, farbe="lila", bahnradius=80)
erde = Gesteinsplanet(name="Erde", radius=15.0, farbe="blau", bahnradius=120)
mars = Gesteinsplanet(name="Mars", radius=15.0, farbe="rot", bahnradius=180)

Zeichenfenster().run()

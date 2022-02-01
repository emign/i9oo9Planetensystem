from __future__ import annotations

from threading import Lock, Thread

from typing import Optional

import pygame, math



TRANS = (1, 1, 1)

WEISS = (255, 255, 255)

ROT = (255, 0, 0)

GRUEN = (0, 255, 0)

BLAU = (0, 0, 255)

GELB = (255,255,0)

MAGENTA = (255,0, 255)

CYAN = (0, 255, 255)

HELLGELB = (255, 255, 128)

HELLGRUEN = (128, 255, 128)

ORANGE = (255, 128,0)

BRAUN = (96, 64, 0)

GRAU = (128, 128, 128)

SCHWARZ =  (0, 0, 0)





## Hilfsklasse zur Realisierung des Singleton-Musters, damit zu jeder Zeit nur ein einziges Objekt der Klasse Zeichenfenster existiert. 

class SingletonMeta(type):

    _instanz: Optional[Singleton] = None

    _lock: Lock = Lock()



    ## Methode sorgt dafür, dass nur ein Objekt der Klasse ausgegeben wird.

    def __call__(cls, *args, **kwargs):

        with cls._lock:

            if not cls._instanz:

                cls._instanz = super().__call__(*args, **kwargs)

        return cls._instanz





## Klasse zur Steuerung des Zeichenfensters

class Zeichenfenster(metaclass=SingletonMeta):

    

    ## Der Konstruktor legt das Fenster an und die notwendigen Strukturen zur Verwaltung der Objekte

    def __init__(self):    

        #Aufruf des Oberklassenkonstruktors: Thread erzeugen

        super().__init__()

        #Fenstergroesse

        self.FENSTERBREITE = 800

        self.FENSTERHOEHE = 600

        #Liste aller Figuren und Liste der beobachter

        self.figurenliste = pygame.sprite.RenderUpdates()

        self.beobachter = []

        #Attribut zum Pausieren der Animation mittels Start/Stopp-Button

        self.nichtGestoppt = False

        #Starten des Threads

        #self.start()

             

    ## Fügt eine Figur in die Liste der zu verwaltenden Objekte ein

    # @param figur einzufügendes Objekt (interne Klasse)        

    def ObjektEinfuegen(self, figur):

        self.figurenliste.add(figur)



    ## Registriert ein Objekt (Turtle, Figur oder Ereignisbehandlung) als Beobachter ein.

    # @param beobachter einzufügender Beobachter   

    def BeobachterRegistrieren(self, beobachter):

         self.beobachter.append(beobachter)

         

    ## Entfernt ein Objekt (Turtle, Figur oder Ereignisbehandlung) als Beobachter.

    # @param beobachter zu entfernender Beobachter   

    def BeobachterEntfernen(self, beobachter):

         self.beobachter.remove(beobachter)   



    ## Informiert die Beobachter (Turtles, Figuren und Ereignisbehandlungs-Objekte) über einem Taktschlag

    def AktionAusfuehren(self):

        kopie_von_beobachterliste = self.beobachter.copy()

        for beobachter in kopie_von_beobachterliste:

            beobachter.AktionAusfuehren()

 

    ## Informiert die Beobachter (Turtles, Figuren und Ereignisbehandlungs-Objekte) über einen Mausklick

    # @param button Maustaste (1-links, 2-Mausrad, 3-rechts, 4-Mausrad nach oben, 5-Mausrad nach unten)

    # @param pos Position des Mausklicks

    def MausGeklickt(self, button, pos):

        x, y = pos

        if x < self.FENSTERBREITE-100 or y < self.FENSTERHOEHE-90:

            kopie_von_beobachterliste = self.beobachter.copy()

            for beobachter in kopie_von_beobachterliste:

                beobachter.MausGeklickt(button, pos)



    ## Informiert die Beobachter (Turtles, Figuren und Ereignisbehandlungs-Objekte) über einen Tastendruck

    # @param taste gedrückte Taste         

    def TasteGedrueckt(self, taste):

        kopie_von_beobachterliste = self.beobachter.copy()

        for beobachter in kopie_von_beobachterliste:

            beobachter.TasteGedrueckt(taste)

            

    ## Taktgeber unterbricht Benachrichtigungen der Beobachter.    

    def Pausieren(self):

        self.nichtGestoppt = False



    ## Taktgeber nimmt Benachrichtigungen der Beobachter wieder auf.   

    def Starten(self):

        self.nichtGestoppt = True



    ## Methode zum Setzen der Geschwindigkeit

    # @param fps frames per second - Bilder pro Sekunde

    def GeschwindigkeitSetzen(self, fps):

        self.FPS = fps



    ##run-Methode des Threads - enthält die Hauptroutine des Programms         

    def run(self): 

      

        #Pygame und Fenster initialisieren

        pygame.init()

        groesse = (self.FENSTERBREITE,self.FENSTERHOEHE)

        self.fenster = pygame.display.get_surface()

        if self.fenster is None:

            self.fenster = pygame.display.set_mode(groesse)

            pygame.display.set_caption("Zeichenfenster")

        

        #Entfernung unnoetiger Ereignisse, so dass sie nicht in die Ereignisliste kommen

        pygame.event.set_blocked(pygame.ACTIVEEVENT)

        pygame.event.set_blocked(pygame.MOUSEMOTION)

        pygame.event.set_blocked(pygame.JOYAXISMOTION)

        pygame.event.set_blocked(pygame.JOYBALLMOTION)

        pygame.event.set_blocked(pygame.JOYHATMOTION)

        pygame.event.set_blocked(pygame.JOYBUTTONUP)

        pygame.event.set_blocked(pygame.JOYBUTTONDOWN)

        pygame.event.set_blocked(pygame.VIDEORESIZE)

        pygame.event.set_blocked(pygame.VIDEOEXPOSE)

        pygame.event.set_blocked(pygame.USEREVENT)

        

        #Taktsteuerung

        clock=pygame.time.Clock()

        self.FPS = 300



        #Button und Schieberegler initalisieren

        self.schaltflaeche = self.Button((self.FENSTERBREITE-50,self.FENSTERHOEHE-70),  self.fenster, self)     

        self.schieberegler = self.Schieberegler( "Tempo", 50, 1, self.FPS, self.FENSTERBREITE-100,self.FENSTERHOEHE-50, self.fenster, self)

        

        #lokales Attribut zum Beenden des Spiels

        nichtBeendet = True

        



    

        #Hauptroutine des Pygames 

        while nichtBeendet:

                

                # Ereignisbehandlung: Durchlaufe alle aktuellen Ereignisse

                for event in pygame.event.get():

                    

                    #Schliessen-Button

                    if event.type==pygame.QUIT:

                        nichtBeendet=False

                    

                    #Maus losgelassen

                    elif event.type == pygame.MOUSEBUTTONUP:

                        self.schaltflaeche.mousebuttonup()

                        self.schieberegler.hit = False

                        self.MausGeklickt(event.button, event.pos)

                        

                    #Maus gedrueckt

                    elif event.type == pygame.MOUSEBUTTONDOWN:

                        pos = pygame.mouse.get_pos()

                        if self.schieberegler.button_rect.collidepoint(pos):

                            self.schieberegler.hit = True

                    

                    #Taste gedrueckt

                    elif event.type == pygame.KEYDOWN:

                        self.TasteGedrueckt(pygame.key.name(event.key))

                        

                #Steuerung des Sliders im Menue rechts unten        

                if self.schieberegler.hit:

                    self.schieberegler.move()

                    

                #Information der Beobachter ueber den Taktschlag

                if self.nichtGestoppt:

                        self.AktionAusfuehren()

                

                #Darstellung des Hintergrunds und der Objekte

                self.FensterNeuZeichnen()

         

                #Wartezeit bis zum nächsten Durchlauf (FPS -> Frames per second)

                clock.tick(self.FPS)

        

        #Schliessen des Fensters nach Abbruch der Hauptroutine         

        pygame.quit()

        #self._delete()

        del(self)



    ## Bringt eine Figur ganz nach vorne. 

    # @param figur Figur, die nach vorne kommt.      

    def GanzNachVornBringen(self,figur):

        if(self.figurenliste.has(figur)):

            self.figurenliste.remove(figur)

            self.figurenliste.add(figur)



    ## Bringt eine Figur ganz nach hinten. 

    # @param figur Figur, die nach hinten kommt.         

    def GanzNachHintenBringen(self,figur):

        if(self.figurenliste.has(figur)):

            self.figurenliste.remove(figur)

            kopie=self.figurenliste.copy()

            self.figurenliste.empty()

            self.figurenliste.add(figur)

            self.figurenliste.add(kopie)



    ## Bringt eine Figur eine Ebene nach hinten. 

    # @param figur Figur, die nach hinten kommt.

    def NachHintenBringen(self,figur):

       if(self.figurenliste.has(figur)):

        liste=self.figurenliste.sprites()

        index_figur = liste.index(figur)

        if index_figur > 0:

            self.figurenliste.empty()

            if index_figur >= 2:

                for i in range(index_figur-1):

                    figur = liste.pop(0)

                    self.figurenliste.add(figur) 

            self.figurenliste.add(liste.pop(1))

            self.figurenliste.add(liste)

     

    ## Bringt eine Figur eine Ebene nach vorne. 

    # @param figur Figur, die nach vorne kommt.        

    def NachVorneBringen(self,figur):

        if(self.figurenliste.has(figur)):

          liste=self.figurenliste.sprites()

          index_figur = liste.index(figur)

          if index_figur < len(liste)-1:

            self.figurenliste.empty()

            if index_figur >= 1:

                for i in range(index_figur):

                    figur=liste.pop(0)

                    self.figurenliste.add(figur)

            self.figurenliste.add(liste.pop(1))

            self.figurenliste.add(liste)  



    ## Entfernt eine Figur.

    # @param figur Figur, die nach vorne kommt.             

    def Entfernen(self, figur):

        if(self.figurenliste.has(figur)):

            self.figurenliste.remove(figur)

            

    def FensterNeuZeichnen(self):

            #Darstellung des Hintergrunds und der Objekte

            self.fenster.fill((230,230,230))

            figurenliste = self.figurenliste.copy()

            for figur in figurenliste:   

                figur.Darstellen(self.fenster)

      



            #Darstellung des Menues

            pygame.draw.rect(self.fenster, GRAU, [self.FENSTERBREITE-100,self.FENSTERHOEHE-90, 100,90])

            self.schaltflaeche.draw()

            self.schieberegler.draw()

     

            #Aktualisierung des gesamten Fensters

            if pygame.display.get_active():

                pygame.display.flip()             

    

    ## Klasse zur Beschreibung eines Buttons (für Start/Stop)

    class Button():

        ## Konstruktor des Buttons

        # @param location Position 

        # @param fenster Pygame-Fenster

        # @param zeichenfenster Zeichenfenster-Referenz  

        def __init__(self, location, fenster, zeichenfenster):

            self.color = (255,255,255)  # the static (normal) color

            self.bg = (255,255,255)  # actual background color, can change on mouseover

            self.fg = (0,0,0)  # text color

            self.groesse = (90,30)

            self.fenster=fenster

            self.zeichenfenster=zeichenfenster

    

            self.font = pygame.font.SysFont("Arial", 16)

            self.txt = "Start"

            self.txt_surf = self.font.render(self.txt, 1, self.fg)

            self.txt_rect = self.txt_surf.get_rect(center=[s//2 for s in self.groesse])

    

            self.surface = pygame.surface.Surface(self.groesse)

            self.rect = self.surface.get_rect(center=location)

    

        ## Zeichnen des Buttons    

        def draw(self):

            self.mouseover()

            self.surface.fill(self.bg)

            self.surface.blit(self.txt_surf, self.txt_rect)

            self.fenster.blit(self.surface, self.rect)

 

        ## Reaktion auf Mausberührung    

        def mouseover(self):

            self.bg = self.color

            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):

                self.bg = (200,200,200)  # mouseover color



        ## Welchsel zwischen Start und Stopp      

        def wechseln(self):

            if self.txt=="Start":                

                self.txt = "Stop"

                self.zeichenfenster.nichtGestoppt = True

            else:

                self.txt = "Start"

                self.zeichenfenster.nichtGestoppt = False

            self.txt_surf = self.font.render(self.txt, 1, self.fg)

        

        ## Reaktion auf Drücken des Buttons          

        def mousebuttonup(self):

            pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(pos):

                   self.wechseln()

                   #button.wechseln()



    ## Klasse zur Beschreibung eines Schiebereglers (für Tempo)  

    class Schieberegler():

        def __init__(self, name, val, mini, maxi, xpos, ypos, fenster, zeichenfenster):

            self.val = val  # start value

            self.maxi = maxi  # maximum at slider position right

            self.mini = mini  # minimum at slider position left

            self.xpos = xpos

            self.ypos = ypos

            self.surf = pygame.surface.Surface((100, 50))

            self.fenster = fenster

            self.hit = False  # the hit attribute indicates slider movement due to mouse interaction

            self.font = pygame.font.SysFont("Arial", 12)

            self.txt_surf = self.font.render(name, 1, (0,0,0))

            self.txt_rect = self.txt_surf.get_rect(center=(50, 15))

            self.zeichenfenster = zeichenfenster

    

            # Static graphics - slider background #

            self.surf.fill((100, 100, 100))

            pygame.draw.rect(self.surf, GRAU, [0, 0, 100, 50], 3)

            pygame.draw.rect(self.surf, ORANGE, [10, 10, 80, 10], 0)

            pygame.draw.rect(self.surf, WEISS, [10, 30, 80, 5], 0)

    

            self.surf.blit(self.txt_surf, self.txt_rect)  # this surface never changes

    

            # dynamic graphics - button surface #

            self.button_surf = pygame.surface.Surface((20, 20))

            self.button_surf.fill(TRANS)

            self.button_surf.set_colorkey(TRANS)

            pygame.draw.circle(self.button_surf, SCHWARZ, (10, 10), 6, 0)

            pygame.draw.circle(self.button_surf, ORANGE, (10, 10), 4, 0)

            

        ## Zeichnen des Schiebereglers    

        def draw(self):

            # static

            surf = self.surf.copy()  

            # dynamic

            pos = (10+int((self.val-self.mini)/(self.maxi-self.mini)*80), 33)

            self.button_rect = self.button_surf.get_rect(center=pos)

            surf.blit(self.button_surf, self.button_rect)

            self.button_rect.move_ip((self.xpos, self.ypos))  # move of button box to correct fenster position

            # fenster

            self.fenster.blit(surf, (self.xpos, self.ypos))

 

        ## Bewegung des Knopfes

        def move(self):



            self.val = (pygame.mouse.get_pos()[0] - self.xpos - 10) / 80 * (self.maxi - self.mini) + self.mini

            if self.val < self.mini:

                self.val = self.mini

            if self.val > self.maxi:

                self.val = self.maxi

            self.zeichenfenster.FPS = self.val













## Interne Oberklasse, erbt von pygame.sprite.Sprite

class Intern(pygame.sprite.Sprite):



    ## Konstruktor der internen Oberklasse

    # @param farbe Farbe des Objekts

    # @param x x-Position

    # @param y y-Position

    # @param breite Breite des Objekts

    # @param hoehe Höhe des Objekts

    # @param winkel Winkel des Objekts

    # @param sichtbar Sichtbarkeit des Objekts

    def __init__(self, farbe, x, y, breite, hoehe, winkel, sichtbar):

        # Aufruf des Oberklassenkonstruktors

        super().__init__()

        Zeichenfenster()

  

        #Initialisierung der Attribute.

        self.x = x

        self.y = y

        self.breite = breite

        self.hoehe = hoehe

        self.farbe = self.FarbeGeben(farbe)

        self.winkel = winkel

        self.sichtbar = True

        

        

        self.image = pygame.Surface([self.breite, self.hoehe])

        self.NeuZeichnen()

        self.NeuPositionieren()

        self.geaendert = False

        self.positionGeaendert = False

        self.winkelGeaendert = False

        

        Zeichenfenster().ObjektEinfuegen(self)

    

    ## Das gesamte Fenster wird neu gezeichnet.

    # Dies passiert nach einem Durchlauf der Hauptroutine des Programms automatisch.

    # Will man innerhalb einer Methode ein Neuzeichnen veranlassen (z. B. um nach Bewegung eines Objekts auf Berührung zu testen), so kann diese Methode ein Neuzeichnen zu anderer Zeit bewirken.

    def FensterNeuZeichnen(self):

        Zeichenfenster().FensterNeuZeichnen()

        

        

    ## Neuzeichnen des Objekts            

    def NeuZeichnen(self):

        #self.image = pygame.Surface([self.breite, self.hoehe])

        self.image.fill(TRANS)#???

        self.image.set_colorkey(TRANS)#Transparente Farbe

        self.geaendert = False

        

    def NeuPositionieren(self):

        self.rect = self.image.get_rect()

        self.rect.topleft = (self.x,self.y)

        self.positionGeaendert = False



    ## Neuzeichnen für Winkel != 0       

    def NeuGedrehtZeichnen(self):

        old_center = self.rect.center

        self.image_gedreht = pygame.transform.rotate(self.image , self.winkel)

        self.rect_gedreht = self.image_gedreht.get_rect()

        self.rect_gedreht.center = old_center  



    ## Darstellen

    # @param fenster Fenster, in dem die Darstellung erfolgt    

    def Darstellen(self, fenster):

        if self.sichtbar:

            if self.geaendert:

                self.NeuZeichnen()

            if self.positionGeaendert:

                self.NeuPositionieren()

            if self.winkelGeaendert:

                self.NeuGedrehtZeichnen()

            self.image.unlock()    

            if self.winkel == 0:

                   fenster.blit(self.image,self.rect)

            else:

                   fenster.blit(self.image_gedreht,self.rect_gedreht) 



    ## Festlegen der Position des Objekts

    # @param x x-Position

    # @param y y-Position                    

    def PositionSetzen(self, x, y):

        self.x = x

        self.y = y

        self.positionGeaendert = True

     

    ## Festlegen der Größe des Objekts

    # @param breite Breite des umgebenden Rechtecks 

    # @param hoehe Höhe des umgebenden Rechtecks          

    def GroesseSetzen (self, breite, hoehe):

        self.breite = breite

        self.hoehe = hoehe  

        self.image = pygame.Surface([self.breite, self.hoehe])

        self.geaendert = True

        self.positionGeaendert = True

        if self.winkel > 0:

            self.winkelGeaendert = True



    ## Festlegen der Farbe des Objekts

    # @param farbe Farbe des Objekts     

    def FarbeSetzen(self, farbe):

        self.farbe = self.FarbeGeben(farbe)

        self.geaendert = True



    ## Festlegen des Winkels des Objekts

    # @param winkel Winkel des Objekts         

    def WinkelSetzen(self, winkel):

        self.winkel = winkel % 360

        self.winkelGeaendert = True

        

        

    ## Festlegen der Sichtbarkeit des Objekts

    # @param sichtbar Sichtbarkeit des Objekts         

    def SichtbarkeitSetzen(self, sichtbar):

        self.sichtbar = sichtbar



    ## Entfernen des Objekts    

    def Entfernen(self):

        Zeichenfenster().Entfernen(self)

        del self



    ## Ermittlung des RGB-Farbwertes

    # @param wert Farbe als String (auch RGB wird akzeptiert)       

    def FarbeGeben(self, wert):

        if wert in ("weiss", "weiss", "white"):

            return WEISS

        elif wert in ("red", "rot"):

            return ROT

        elif wert in ("gruen", "grün", "green"):

            return GRUEN

        elif wert in ("blue", "blau"):

            return BLAU

        elif wert in ("yellow", "gelb"):

            return GELB

        elif wert in ("magenta", "pink"):

            return MAGENTA

        elif wert == "cyan":

            return CYAN

        elif wert == "hellgelb":

            return HELLGELB

        elif wert in ("hellgruen", "hellgrün"):

            return HELLGRUEN

        elif wert == "orange":

            return ORANGE

        elif wert in ("braun", "brown"):

            return BRAUN

        elif wert in ("grau", "grey"):

            return GRAU

        elif wert in ("transparent", "TRANS"):

            return TRANS

        elif wert in ("black", "schwarz"):

            return SCHWARZ

        elif type(wert) is tuple:

            if (0,0,0) <= wert <= (255,255,255):

                return wert

        else:

            return SCHWARZ

    

    ## Objekt in den Vordergrund bringen    

    def GanzNachVornBringen(self):

        Zeichenfenster().GanzNachVornBringen(self)



    ## Objekt eine Ebene nach vorne bringen           

    def NachVorneBringen(self):

        Zeichenfenster().NachVorneBringen(self)



    ## Objekt eine Ebene nach hinten bringen     

    def NachHintenBringen(self):

        Zeichenfenster().NachHintenBringen(self)



    ## Objekt in den Hintergrund bringen     

    def GanzNachHintenBringen(self):

        Zeichenfenster().GanzNachHintenBringen(self)

    

    ## Überprüft, ob die gegebene Farbe die Farbe des Objekts ist.

    # @param farbe zu überprüfender Farbwert

    # @return Wert gibt an, ob Farben identisch sind      

    def EnthaeltFarbe(self, farbe):

        return self.farbe == farbe

        







        

## Klasse zur Beschreibung des Rechtecks (intern)       

class RechteckIntern(Intern):

 

    ## Konstruktor der internen Rechtecksklasse

    # @param farbe Farbe des Objekts

    # @param x x-Position

    # @param y y-Position

    # @param breite Breite des Objekts

    # @param hoehe Höhe des Objekts

    # @param winkel Winkel des Objekts

    # @param sichtbar Sichtbarkeit des Objekts

    def __init__(self, farbe, x, y, breite, hoehe, winkel, sichtbar):

        super().__init__(farbe, x, y, breite, hoehe, winkel,sichtbar)

    

    ## Methode zum Zeichnen des internen Rechtecks    

    def NeuZeichnen(self):

        super().NeuZeichnen()

        pygame.draw.rect(self.image, self.farbe, (0,0,self.breite, self.hoehe))

        if self.winkel != 0:

            super().NeuGedrehtZeichnen()







            

## Klasse zur Beschreibung des Kreises (intern)         

class KreisIntern(Intern):



    ## Konstruktor der internen Kreisklasse

    # @param farbe Farbe des Objekts

    # @param x x-Position

    # @param y y-Position

    # @param radius Radius des Objekts

    # @param winkel Winkel des Objekts

    # @param sichtbar Sichtbarkeit des Objekts 

    def __init__(self, farbe, x, y, radius,  winkel, sichtbar):

        super().__init__(farbe, x, y, radius* 2, radius * 2, winkel, sichtbar)



    ## Methode zum Zeichnen des internen Kreises       

    def NeuZeichnen(self):

        super().NeuZeichnen()

        pygame.draw.ellipse(self.image, self.farbe, (0,0,self.breite, self.hoehe))

        if self.winkel != 0:

            super().NeuGedrehtZeichnen()









## Klasse zur Beschreibung des Dreiecks (intern)             

class DreieckIntern(Intern):



    ## Konstruktor der internen Dreiecksklasse

    # @param farbe Farbe des Objekts

    # @param x x-Position

    # @param y y-Position

    # @param breite Breite des Objekts

    # @param hoehe Höhe des Objekts

    # @param winkel Winkel des Objekts

    # @param sichtbar Sichtbarkeit des Objekts  

    def __init__(self, farbe, x, y, breite, hoehe, winkel, sichtbar):

        super().__init__(farbe, x, y, breite, hoehe, winkel, sichtbar)



    ## Methode zum Zeichnen des internen Dreiecks          

    def NeuZeichnen(self):

        super().NeuZeichnen()

        pygame.draw.polygon(self.image, self.farbe, [(self.breite/2,0),(self.breite, self.hoehe),(0, self.hoehe)])

        if self.winkel != 0:

            super().NeuGedrehtZeichnen()

  



      

 

## Klasse zur Beschreibung des Textes (intern)

class TextIntern(Intern):



    ## Konstruktor der internen Textklasse

    # @param farbe Farbe des Objekts

    # @param x x-Position

    # @param y y-Position

    # @param textgroesse Größe des Texts

    # @param winkel Winkel des Objekts

    # @param sichtbar Sichtbarkeit des Objekts  

    def __init__(self, farbe, x, y, textgroesse, winkel, sichtbar):

        self.groesse = textgroesse

        self.textinhalt = "Text"

        self.geaendert = True

        super().__init__(farbe, x, y, 0, 0, winkel,sichtbar)



    ## Methode zum Festlegen des Textes

    # @param text darzustellender Text    

    def TextSetzen(self, text):

        self.textinhalt = text

        self.geaendert = True



    ## Festlegung der Textgröße

    # @param groesse Schriftgröße        

    def TextGroesseSetzen(self, groesse):

        self.groesse = groesse

        self.geaendert = True



    ## Vergrößerung der Schrift       

    def TextVergroessern(self):

        if self.groesse <= 10:

            self.groesse += 1

        elif self.groesse <= 40:

            self.groesse += 2

        else:

            self.groesse += 4

        self.geaendert = True

 

    ## Verkleinerung der Schrift        

    def TextVerkleinern(self):

        if self.groesse <= 10:

            self.groesse -= 1

        elif self.groesse <= 40:

            self.groesse -= 2

        else:

            self.groesse -= 4

        if self.groesse < 1:

            self.groesse = 1

        self.geaendert = True



    ## Methode zum Zeichnen des internen Textes          

    def NeuZeichnen(self):

        font = pygame.font.SysFont("Arial", self.groesse)

        self.text = font.render(self.textinhalt, True, self.farbe)

        self.textRect = self.text.get_rect()

        self.textRect.topleft = (self.x,self.y)

        if self.winkel != 0:

            self.NeuGedrehtZeichnen()

            

    ## Methode zum Zeichnen des internen Textes bei Winkel != 0    

    def NeuGedrehtZeichnen(self):

        old_center = self.textRect.center

        self.textGedreht = pygame.transform.rotate(self.text, self.winkel)

        self.textRectGedreht=self.textGedreht.get_rect()

        self.textRectGedreht.center = old_center 

    

    ## Darstellen des Textes im Fenster

    # @param fenster      

    def Darstellen(self, fenster):

        if self.geaendert:

            self.geaendert = False

            self.NeuZeichnen()

            

        if self.winkel == 0:

               fenster.blit(self.text,self.textRect)

        else:

               fenster.blit(self.textGedreht,self.textRectGedreht) 

  





## Klasse zur Beschreibung der Figur (intern)      

class FigurIntern(Intern):

    

    ## Konstruktor der internen Figurklasse

    # @param x x-Position

    # @param y y-Position

    # @param groesse Größe der Figur

    # @param winkel Winkel des Objekts

    # @param sichtbar Sichtbarkeit des Objekts 

    def __init__(self, x, y, groesse, winkel, sichtbar):

           self.xD = x

           self.yD = y

           self.homeX = x

           self.homeY = y

           self.homeWinkel = 0

           self.figurenliste = []

           self.IstStandardfigur = True

           super().__init__((255,255,255), x, y, groesse, groesse, winkel, sichtbar)

           self.farbliste = []

           self.StandardfigurErzeugen() 



    ## Setzt die Position der Figur.

    # @param x x-Position der Mitte der Figur

    # @param y y-Position der Mitte der Figur    

    def PositionSetzen(self, x, y):

        super().PositionSetzen(x, y)

        self.xD = x

        self.yD = y

        self.positionGeaendert = True



    ## Verschiebt die Figur in die Richtung ihres Winkels.

    # @param laenge Anzahl der Längeneinheiten   

    def Gehen(self,laenge):

        neuX = self.xD + math.cos(self.winkel*math.pi/180)*laenge

        neuY = self.yD - math.sin(self.winkel*math.pi/180)*laenge

        self.xD = neuX

        self.yD = neuY

        self.x = round(neuX)

        self.y = round(neuY)

        self.positionGeaendert  = True        



    ## Setzt die Größe der Figur.

    # @param groesse Größe des umgebenden Quadrats          

    def GroesseSetzen (self, groesse):

        super().GroesseSetzen(groesse, groesse)      



    ## Bringt die Figur zu ihrem Startpunkt.          

    def ZumStartpunktGehen(self):

        self.x = self.homeX

        self.y = self.homeY

        self.xD = self.x

        self.yD = self.y

        self.winkel = self.homeWinkel

        self.positionGeaendert = True



    ## Zeichnet die Figur neu im Fenster.        

    def NeuZeichnen(self):

        super().NeuZeichnen()  

        for codezeile in self.figurenliste:

           exec(codezeile) 

        if self.winkel != 0:

            super().NeuGedrehtZeichnen()

            

            

    ## Positioniert die Turtle neu.

    def NeuPositionieren(self):

        self.rect = self.image.get_rect()

        self.rect.center = (self.x,self.y)

        self.positionGeaendert = False

            

        

    ## Testet, ob die Figur eine andere Figur (Turtle, Rechteck,...) berührt.

    # @return true, wenn die Figur und eine Grafikfigur überlappen     

    def Beruehrt(self):

        sprites_list = Zeichenfenster().figurenliste.copy()

        sprites_list.remove(self)

        for figur in sprites_list:

            if not (isinstance(figur, TextIntern)):

                if not(pygame.sprite.collide_mask(self, figur) is None):

                    return True

        return False



    ## Testet, ob die Figur eine Objekt berührt, das die gegebene Farbe enthält.

    # (die Farbe muss nicht unbedingt sichtbar oder direkt berührt werden)

    # @param farbe Farbe, auf die getestet werden soll.

    # @return true wenn ein Objekt mit der Farbe berührt wird.      

    def BeruehrtFarbe(self, farbe):

        sprites_list = Zeichenfenster().figurenliste.copy()

        sprites_list.remove(self)

        for figur in sprites_list:

            if not (isinstance(figur, TextIntern)):

                if not(pygame.sprite.collide_mask(self, figur) is None):

                    if figur.EnthaeltFarbe(self.FarbeGeben(farbe)):

                        return True

        return False



    ## Testet, ob die Figur eine Objekt berührt.

    # @param objekt Objekt, mit dem eine Überschneidung geprüft werden soll.

    # @return true wenn das übergebene Objekt mit der Farbe berührt.             

    def BeruehrtObjekt(self, objekt):

        if (isinstance(objekt, TextIntern)):

            return False

        return not (pygame.sprite.collide_mask(self, objekt.symbol) is None)



    ## Erzeugt eine Standardfigur

    def StandardfigurErzeugen(self):

        if(not self.IstStandardfigur):

            self.figurenliste.clear()

            self.image.fill(TRANS)

            self.IstStandardfigur = True

        self.figurenliste.append("pygame.draw.polygon(self.image, GELB, [(0, 0),(self.breite, self.hoehe/2),(0, self.hoehe)])")

        self.figurenliste.append("pygame.draw.ellipse(self.image, BLAU, (20, self.hoehe/2 -4,8,8))")

        self.farbliste = []

        self.farbliste.append(GELB)

        self.farbliste.append(BLAU)

        self.geaendert  = True



    ## Erzeugt ein neues, rechteckiges Element.

    # Alle Werte beziehen sich auf eine Figur der Größe 100x100 und den Koordinaten (0|0) in der Mitte des Quadrats

    # @param x x-Wert der linken oberen Ecke des Rechtecks innerhalb der Figur (-50<=x<=50)

    # @param y y-Wert der linken oberen Ecke des Rechtecks innerhalb der Figur (-50<=y<=50)

    # @param breite Breite des Rechtecks innerhalb der Figur (0<=breite<=50-x)

    # @param hoehe Höhe des Rechtecks innerhalb der Figur (0<=hoehe<=50-x)

    # @param farbe Farbe des Figurelements

    def FigurteilFestlegenRechteck(self,x, y, breite, hoehe, farbe):

        if(self.IstStandardfigur):

            self.figurenliste.clear()

            self.image.fill(TRANS)

            self.IstStandardfigur = False

            self.farbliste = []

        

        x = int(round(self.breite*x/100+self.breite/2))

        y = int(round(self.hoehe*y/100+self.hoehe/2))

        breite = int(round(self.breite*breite/100))

        hoehe = int(round(self.hoehe*hoehe/100))



        farbeCodiert = self.FarbeGeben(farbe)

        string =  "pygame.draw.rect(self.image,"+ str(farbeCodiert)+", ("+str(x)+","+str(y)+","+str(breite)+", "+str(hoehe)+"))"

        self.figurenliste.append(string)

        if not farbeCodiert in self.farbliste:

            self.farbliste.append(farbeCodiert)

        self.geaendert  = True



    ## Erzeugt ein neues, elliptisches Element.

    # Alle Werte beziehen sich auf eine Figur der Größe 100x100 und den Koordinaten (0|0) in der Mitte des Quadrats

    # @param x x-Wert der linken oberen Ecke des Rechtecks, das die Ellipse umgibt, innerhalb der Figur (-50<=x<=50)

    # @param y y-Wert der linken oberen Ecke des Rechtecks, das die Ellipse umgibt, innerhalb der Figur (-50<=y<=50)

    # @param breite Breite des Rechtecks, das die Ellipse umgibt, innerhalb der Figur (0<=breite<=50-x)

    # @param hoehe Höhe des Rechtecks, das die Ellipse umgibt, innerhalb der Figur (0<=hoehe<=50-x)

    # @param farbe Farbe des Figurelements                    

    def FigurteilFestlegenEllipse(self, x, y, breite, hoehe, farbe):

        if(self.IstStandardfigur):

            self.figurenliste.clear()

            self.image.fill(TRANS)

            self.IstStandardfigur = False

            self.farbliste = []

            

        x = int(round(self.breite*x/100+self.breite/2))

        y = int(round(self.hoehe*y/100+self.hoehe/2))

        breite = int(round(self.breite*breite/100))

        hoehe = int(round(self.hoehe*hoehe/100))







        farbeCodiert = self.FarbeGeben(farbe)

        string =  "pygame.draw.ellipse(self.image,"+ str(farbeCodiert)+", ("+str(x)+","+str(y)+","+str(breite)+", "+str(hoehe)+"))"

        self.figurenliste.append(string)

        if not farbeCodiert in self.farbliste:

            self.farbliste.append(farbeCodiert)

        self.geaendert  = True



    ## Erzeugt ein neues, dreieckiges Element einer eigenen Darstellung der Figur.

    # Die Werte müssen passend zur Größe der Figur gewählt werden (Standardwert: 40) 

    # @param x1 x-Wert des ersten Punktes innerhalb der Figur (-50<=x1<=50)

    # @param y1 y-Wert des ersten Punktes innerhalb der Figur (-50<=y1<=50)

    # @param x2 x-Wert des zweiten Punktes innerhalb der Figur (-50<=x2<=50)

    # @param y2 y-Wert des zweiten Punktes innerhalb der Figur (-50<=y2<=50)

    # @param x3 x-Wert des dritten Punktes innerhalb der Figur (-50<=x3<=50)

    # @param y3 y-Wert des dritten Punktes innerhalb der Figur (-50<=y3<=50)

    # @param farbe Farbe des Figurelements         

    def FigurteilFestlegenDreieck(self, x1, y1 ,x2, y2, x3, y3, farbe):

        if(self.IstStandardfigur):

            self.figurenliste.clear()

            self.image.fill(WEISS)

            self.IstStandardfigur = False

            self.farbliste = []

            

        x1 = int(round(self.breite*x1/100+self.breite/2))

        x2 = int(round(self.breite*x2/100+self.breite/2))

        x3 = int(round(self.breite*x3/100+self.breite/2))

        y1 = int(round(self.hoehe*y1/100+self.hoehe/2))

        y2 = int(round(self.hoehe*y2/100+self.hoehe/2))

        y3 = int(round(self.hoehe*y3/100+self.hoehe/2))



        farbeCodiert = self.FarbeGeben(farbe)

        string =  "pygame.draw.polygon(self.image,"+ str(farbeCodiert)+", [("+str(x1)+","+str(y1)+"),("+str(x2)+", "+str(y2)+"),("+str(x3)+","+str(y3)+")])"

        self.figurenliste.append(string)



        if not farbeCodiert in self.farbliste:

            self.farbliste.append(farbeCodiert)

        self.geaendert  = True



    ## Testet, ob die Figur die Farbe enthält.   

    # @param farbe zu überprüfende Farbe

    # @return wahr, wenn die Farbe vorhanden ist.

    def EnthaeltFarbe(self, farbe):

        return self.FarbeGeben(farbe) in self.farbliste

    

    

    

    

## Klasse zur Beschreibung der Turtle (intern)         

class TurtleIntern(Intern):

    

    ## Der Konstruktor erzeugt das Objekt und verwaltet die Attribute für Position und Aussehen.

    def __init__(self, farbe, x, y, groesse, winkel, sichtbar):

           self.xD = x

           self.yD = y

           self.homeX = x

           self.homeY = y

           self.homeWinkel = 0

           self.stiftUnten = True

           self.farbliste = []

           self.zeichenflaeche = pygame.Surface([Zeichenfenster().FENSTERBREITE, Zeichenfenster().FENSTERHOEHE])

           self.zeichenflaeche.fill(TRANS)#???

           self.zeichenflaeche.set_colorkey(TRANS)#transparente Farbe

           self.sichtbarkeitZeichenflaeche = True

           self.schwanzspitze = Schwanzspitze()

           self.schwanzspitze.PositionSetzen(x, y)

           super().__init__(farbe, x, y, 60, 25, winkel, sichtbar)   



    ## Setzt die Position der Turtle (Position der Schwanzspitze). Bei der Positionsänderung wird auch bei abgesenktem Stift keine Linie gezeichnet.

    # @param x x-Position der Schwanzspitze

    # @param y y-Position der Schwanzspitze    

    def PositionSetzen(self, x, y):

        super().PositionSetzen(x, y)

        self.xD = x

        self.yD = y

        self.schwanzspitze.rect.topleft = (self.x, self.y)

        self.positionGeaendert = True



    ## Verschiebt die Turtle in die Richtung ihres Winkels.

    # @param laenge Anzahl der Längeneinheiten         

    def Gehen(self,laenge):

        neuX = self.xD + math.cos(self.winkel*math.pi/180)*laenge

        neuY = self.yD - math.sin(self.winkel*math.pi/180)*laenge

        if self.stiftUnten:

            pygame.draw.line(self.zeichenflaeche, self.farbe, (self.x, self.y), (round(neuX), round(neuY)))

        self.xD = neuX

        self.yD = neuY

        self.x = round(neuX)

        self.y = round(neuY)

        self.schwanzspitze.PositionSetzen(self.x, self.y)

        self.positionGeaendert  = True

        



    ## Turtle bewegt sich danach, ohne zu zeichnen.         

    def StiftHeben(self):

        self.stiftUnten = False



    ## Turtle wechselt in den Zeichenmodus.       

    def StiftSenken(self):

        self.stiftUnten = True

 

    ## Turtle geht zum Startpunkt         

    def ZumStartpunktGehen(self):

        self.x = self.homeX

        self.y = self.homeY

        self.xD = self.x

        self.yD = self.y

        self.winkel = self.homeWinkel

        self.schwanzspitze.rect.topleft = (self.x, self.y)

        self.positionGeaendert = True

        

    ## Schaltet die Sichtbarkeit der Zeichnung ein oder aus.

    # Erlaubte Parameterwerte: true, false

    # @param wert (neue) Sichtbarkeit der Zeichenfläche  

    def SichtbarkeitZeichenflaecheSetzen(self, wert):

        self.sichtbarkeitZeichenflaeche = wert

    

    ## Testet, ob die Turtle ein Grafikelement berührt.

    # @return true, wenn die Turtle und eine Grafikfigur überlappen          

    def Beruehrt(self):

        sprites_list = Zeichenfenster().figurenliste.copy()

        sprites_list.remove(self)

        for figur in sprites_list:

            if not (isinstance(figur, TextIntern)):

                if not(pygame.sprite.collide_mask(self.schwanzspitze, figur) is None):

                    return True

        return False



    ## Testet, ob die Turtle mit der Schwanzspitze eine gegebene Farbe berührt

    # @param farbe Farbe, auf die getestet werden soll.

    # @return true wenn ein Objekt mit der Farbe berührt wird.    

    def BeruehrtFarbe(self, farbe):

        if 22.5 <= self.winkel < 67.5:

            x = self.x - 2

            y = self.y + 2

        elif 67.5 <= self.winkel < 112.5:

            x = self.x

            y = self.y + 2

        elif 112.5 <= self.winkel < 157.5:

            x = self.x + 2

            y = self.y + 2

        elif 157.5 <= self.winkel < 202.5:

            x = self.x + 2

            y = self.y

        elif 202.5 <= self.winkel < 247.5:

            x = self.x + 2

            y = self.y - 2

        elif 247.5 <= self.winkel < 292.5:

            x = self.x

            y = self.y - 2

        elif 292.5 <= self.winkel < 337.5:

            x = self.x - 2

            y = self.y - 2

        else:

            x = self.x - 2

            y = self.y      

        if not (x < 0 or y < 0 or x > Zeichenfenster().FENSTERBREITE or y > Zeichenfenster().FENSTERHOEHE):

            wert1 = Zeichenfenster().fenster.get_at((x,y))

        else:

            return False

        wert2 = self.FarbeGeben(farbe)

        for i in range(3):

            if(wert1[i]!=wert2[i]):

                return False

        return True



    ## Testet, ob die Turtle eine Objekt berührt.

    # @param objekt Objekt, mit dem eine Überschneidung geprüft werden soll.

    # @return true wenn das übergebene Objekt mit der Farbe berührt.                 

    def BeruehrtObjekt(self, objekt):

        if (isinstance(objekt, TextIntern)):

            return True

        return not (pygame.sprite.collide_mask(self.schwanzspitze, objekt.symbol) is None)

        

    ## Testet, ob die Turtle eine Farbe enthält.

    # @param farbe Farbe, die geprüft werden soll.

    # @return true wenn die Turtle die Farbe enthält.      

    def EnthaeltFarbe(self, farbe):

        EnthaeltFarbe = False

        if self.FarbeGeben(farbe) in self.Farbliste:

            EnthaeltFarbe = True

        if self.FarbeGeben(farbe) == self.Farbe:

            EnthaeltFarbe = True

        return EnthaeltFarbe



    ## Zeichnet die Turtle neu.

    def NeuZeichnen(self):   

        super().NeuZeichnen()

        #Kopf

        pygame.draw.ellipse(self.image, GRUEN, (50,7,10, 12))

        #Beine

        pygame.draw.ellipse(self.image, GRUEN, (36,0,8, 25))

        pygame.draw.ellipse(self.image, GRUEN, (44,0,8, 25))

        #Augen

        pygame.draw.ellipse(self.image, self.farbe, (55,9,3, 2))

        pygame.draw.ellipse(self.image, self.farbe, (55,14,3, 2))

        #Schwanz

        pygame.draw.ellipse(self.image, self.farbe, (30,10,10, 5))

        #Rumpf

        pygame.draw.ellipse(self.image, BRAUN, (32,2,24, 21))

        self.schwanzspitze.NeuZeichnen(self.x, self.y, self.farbe)

        self.farbliste.append(GRUEN)

        self.farbliste.append(BRAUN)

      

        if self.winkel != 0:

            super().NeuGedrehtZeichnen()



    ## Positioniert die Turtle neu.

    def NeuPositionieren(self):

        self.rect = self.image.get_rect()

        self.rect.center = (self.x,self.y)

        self.positionGeaendert = False

                  

  



    ## Stellt die Turtle dar.

    # @param fenster Fenster zur Darstellung         

    def Darstellen(self, fenster):

        if self.sichtbarkeitZeichenflaeche:

            fenster.blit(self.zeichenflaeche,self.zeichenflaeche.get_rect())

        #self.schwanzspitze.Darstellen(fenster)

        fenster.blit(self.schwanzspitze.image,self.schwanzspitze.image.get_rect())

        super().Darstellen(fenster)



    ## Löscht die Zeichenfläche.        

    def Loeschen(self):

        self.zeichenflaeche.fill(TRANS)



## Klasse zur Beschreibung der Schwanzspitze der Turtle (intern)          

class Schwanzspitze(pygame.sprite.Sprite):



        ## Der Konstruktor erzeugt das Objekt und verwaltet die Attribute für Position und Aussehen.    

        def __init__(self):

                pygame.sprite.Sprite.__init__(self)

                self.image = pygame.Surface([5, 5])

                self.image.fill(ROT)

                self.rect = self.image.get_rect()

        

        ## Setzt die Position der  Schwanzspitze)

        # @param x x-Position der Schwanzspitze

        # @param y y-Position der Schwanzspitze            

        def PositionSetzen(self, x, y):

                self.rect.topleft = (x,y)



        ## Zeichnet die Turtle neu.                

        def NeuZeichnen(self,x,y, farbe):

                self.image.fill((255,255,255))

                self.image.set_colorkey(TRANS)#Transparente Farbe

                self.rect = self.image.get_rect()

                self.rect.center = (x,y)

                pygame.draw.rect(self.image, farbe, (0,0,1, 1))

                

                

        

       

    

    
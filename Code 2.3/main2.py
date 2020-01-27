"""
Créé pour un projet de TIPE consistant à piloter un foil automatique
Clément Patrizio MP FSM 2019-2020
L'enregistrement d'un fichier excel se fait par défaut dans le dossier mère mais cela peut être modifié dans l'onglet 'Outils' - 'Enregistrer excel sous'
Le port utilisé est par défaut le port COM5 mais cela peut être changé dans l'onglet 'Outils' - 'port USB'
"""

"""
Créer class 'checkButton' qui disable ou non les scales
créer des fonctions de calculs pour lier DISTANCE de consigne et angle à fournir au moteur
"""

"""
Astuces :
print("%.3f" % number) >>> 0.678 au lieu de 0.6781234
"""

# 'go' : 1 si une carte est branchée, 0 sinon
# 'running' : 1 si l'app doit etre allumée, 0 si elle est fermée
# 'valeur_consigne_angle' évolue dans [-90,90]

import tkinter as tk
from tkinter.filedialog import*
import pyfirmata
import time
import os
import inspect

from Python_To_Excel.Create_excel_file import create_excel as create_excel
from Python_Board.Board import send_to_board as send_to_board
from Python_Board.Board import get_from_board as get_from_board
from Python_Board.Board import ArduinoServo as ArduinoServo
from Python_Board.Board import ArduinoPotentiometre as ArduinoPotentiometre
from Python_Board.Board import ArduinoCapteur as ArduinoCapteur


class tkinterButton(tk.Button):
    """Créer les boutons de commande"""

    def __init__(self, id, application):
        tk.Button.__init__(self, application)

        self.id = id
        if application == app:
            if self.id == 0:
                self.state = 'off'
                self.x, self.y = 460, 135
                self.bg, self.fg, self.cursor = 'light blue', 'black', 'hand2'
                self.config(text="Pilote automatique", width=15, height=2, bg=self.bg, fg=self.fg, font="GROBOLD.ttf 11 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.automatique)

            elif self.id == 1:
                self.state = 'off'
                self.x, self.y = 650, 135
                self.bg, self.fg, self.cursor = 'grey', 'grey75', 'arrow'
                self.config(text="Envoyer échelon", width=15, height=2, bg=self.bg, fg=self.fg, font="GROBOLD.ttf 11 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.envoyer_echelon)

            elif self.id == 2:
                self.state = 'on'
                self.x, self.y = 460, 230
                self.bg, self.fg, self.cursor = 'blue', 'black', 'hand2'
                self.config(text="Pilote manuel", width=15, height=2, bg=self.bg, fg=self.fg, font="GROBOLD.ttf 11 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.manuel)

            elif self.id == 3:
                self.state = 'off'
                self.x, self.y = 460, 325
                self.bg, self.fg, self.cursor = 'red', 'black', 'hand2'
                self.config(text="STOP", width=15, height=2, bg=self.bg, fg=self.fg, font="GROBOLD.ttf 11 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.stop)

            elif self.id == 4:
                self.state = 'off'
                self.x, self.y = 460, 460
                self.bg, self.fg, self.cursor = 'grey', 'grey75', 'arrow'
                self.config(text="Mode Expérience", width=15, height=2, bg=self.bg, fg=self.fg, font="GROBOLD.ttf 11 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.experience)

            elif self.id == 5:
                self.state = 'off'
                self.x, self.y = 650, 460
                self.bg, self.fg, self.cursor = 'blue', 'black', 'hand2'
                self.config(text="Initialiser", width=15, height=2, bg=self.bg, fg=self.fg, font="GROBOLD.ttf 11 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.ouvrir_init)

            # deux modes de pilotage automatique : système asservi en consigne de hauteur OU système non asservi en consigne d'angle
            elif self.id == 6:
                self.state = 'off'
                self.x, self.y = 1800, 340
                self.bg, self.fg, self.cursor = 'grey', 'grey75', 'arrow'
                self.config(text="Système asservi en distance", width=22, height=2, bg=self.bg, fg=self.fg, font="GROBOLD.ttf 7 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.consigne_distance)

            elif self.id == 7:
                self.state = 'on'
                self.x, self.y = 1800, 340
                self.bg, self.fg, self.cursor = 'blue', 'black', 'hand2'
                self.config(text="Système non asservi en angle", width=22, height=2, bg=self.bg, fg=self.fg, font="GROBOLD.ttf 7 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.consigne_angle)


        elif application == fenetre: #boutons de la fenêtre 'initialisation du potentiomètre'
            self.id = id
            if self.id == 0:
                self.state = 'off'
                self.x, self.y = 60, 160
                self.bg, self.fg, self.cursor = 'grey', 'black', 'hand2'
                self.config(text="Initialiser le 0", width=15, height=2, bg=self.bg, fg=self.fg, font="GROBOLD.ttf 11 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.init)

            elif self.id == 1:
                self.state = 'off'
                self.x, self.y = 220, 160
                self.bg, self.fg, self.cursor = 'grey', 'black', 'hand2'
                self.config(text="Initialiser le 90", width=15, height=2, bg=self.bg, fg=self.fg, font="GROBOLD.ttf 11 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.init)


    def consigne_distance(self):
        if self.state == 'off':
            pass
        else:
            pass

    def consigne_angle(self):
        if self.state == 'off':
            pass
        else:
            pass

    def ouvrir_init(self):
        global fenetre, L_Buttons_init

        fenetre = create_app('Initialiser')
        L_Labels_init = create_L_Labels(fenetre)
        L_Buttons_init = create_L_Buttons(fenetre)

        L_Labels_init[0].place(x=L_Labels_init[0].x, y=L_Labels_init[0].y)
        L_Labels_init[1].place(x=L_Labels_init[1].x, y=L_Labels_init[1].y)
        L_Buttons_init[0].place(x=L_Buttons_init[0].x, y=L_Buttons_init[0].y)
        L_Buttons_init[1].place(x=L_Buttons_init[1].x, y=L_Buttons_init[1].y)

        fenetre.update()

    def init(self):
        """initialiser la valeur alpha = 0 du potentiomètre"""
        global zero, quatre_vingt_dix, t0_clear_Canvas
        if self.id == 0:
            if self.state == 'off':
                zero = float(Potentiometre.val)
                self.config(bg='grey75', fg='grey', cursor = 'arrow')
                self.state = 'on'
            else:
                pass
        elif self.id == 1:
            if L_Buttons_init[0].state == 'on':
                quatre_vingt_dix = float(Potentiometre.val)
                fenetre.destroy()
                L_Canvas[0].itemconfig(console_text_1, text='Potentiomètre initialisé')
                L_Canvas[0].coords(console_text_1, 90, 57)
                t0_clear_Canvas = time.time()
            else:
                pass

    def automatique(self):
        if self.state == 'off':
            self.state = 'on'
            self.bg = 'blue'
            self.config(bg=self.bg)

            L_Buttons[1].bg, L_Buttons[1].fg, L_Buttons[1].cursor = 'blue', 'black', 'hand2'
            L_Buttons[1].config(bg=L_Buttons[1].bg,
                                fg=L_Buttons[1].fg, cursor=L_Buttons[1].cursor)
            L_Buttons[2].bg, L_Buttons[2].fg, L_Buttons[2].state = 'light blue', 'black', 'off'
            L_Buttons[2].config(bg=L_Buttons[2].bg, fg=L_Buttons[2].fg)
            L_Buttons[4].bg, L_Buttons[4].fg, L_Buttons[4].cursor = 'light blue', 'black', 'hand2'
            L_Buttons[4].config(bg=L_Buttons[4].bg,
                                fg=L_Buttons[4].fg, cursor=L_Buttons[4].cursor)

            L_Scales[0].x, L_Scales[1].x, L_Scales[2].x = 70, 240, 1800
            for i in range(3):
                L_Scales[i].place(x=L_Scales[i].x, y=L_Scales[i].y)

            L_Entry[0].x, L_Entry[1].x = 147, 320
            for i in range(2):
                L_Entry[i].place(x=L_Entry[i].x, y=L_Entry[i].y)

            L_Buttons[6].x, L_Buttons[7].x = 78, 247
            for i in range(6,8):
                L_Buttons[i].place(x=L_Buttons[i].x, y=L_Buttons[i].y)

        else:
            self.state = 'off'
            self.bg = 'light blue'
            self.config(bg=self.bg)

            L_Buttons[1].bg, L_Buttons[1].fg, L_Buttons[1].cursor = 'grey', 'grey75', 'arrow'
            L_Buttons[1].config(bg=L_Buttons[1].bg,
                                fg=L_Buttons[1].fg, cursor=L_Buttons[1].cursor)
            L_Buttons[2].bg, L_Buttons[2].fg, L_Buttons[2].state = 'blue', 'black', 'on'
            L_Buttons[2].config(bg=L_Buttons[2].bg, fg=L_Buttons[2].fg,)
            L_Buttons[4].bg, L_Buttons[4].fg, L_Buttons[4].cursor, L_Buttons[4].state = 'grey', 'grey75', 'arrow', 'off'
            L_Buttons[4].config(bg=L_Buttons[4].bg,
                                fg=L_Buttons[4].fg, cursor=L_Buttons[4].cursor)

            L_Scales[0].x, L_Scales[1].x, L_Scales[2].x = 1800, 1800, 55
            for i in range(3):
                L_Scales[i].place(x=L_Scales[i].x, y=L_Scales[i].y)

            L_Entry[0].x, L_Entry[1].x = 1800, 1800
            for i in range(2):
                L_Entry[i].place(x=L_Entry[i].x, y=L_Entry[i].y)

            L_Buttons[6].x, L_Buttons[7].x = 1800, 1800
            for i in range(6,8):
                L_Buttons[i].place(x=L_Buttons[i].x, y=L_Buttons[i].y)

    def envoyer_echelon(self):
        global mode_experience, L_temps, L_angle, L_distance, acquerir, app, t0_clear_Canvas, t0_experience

        if self.bg == 'blue':  # On a cliqué sur le bouton envoyer echelon
            if go == 1:

                send_to_board(
                    board, 'automatique', valeur_consigne_angle, valeur_consigne_distance, Servo)

                L_Canvas[0].itemconfig(console_text_1, text='Echelon envoyé')
                L_Canvas[0].coords(console_text_1, 65, 57)
                t0_clear_Canvas = time.time()

                if mode_experience == 1:
                    t0_experience = time.time()
                    L_temps, L_angle, L_distance = [], [], []
                    acquerir = 1
                    self.bg = 'red'
                    self.config(text='Arrêter acquisition', bg=self.bg)

                    for i in range(6):
                        if i != 1:
                            L_Buttons[i].bg = 'grey65'
                            L_Buttons[i].config(
                                bg=L_Buttons[i].bg, state='disabled', cursor='arrow')

            else:
                print("impossible d'envoyer echelon")



        elif self.bg == 'red':  # On a cliqué sur le bouton 'arrêter acquisition'
            mode_experience = 0
            acquerir = 0

            if valeur_consigne_angle != 0:
                create_excel(valeur_consigne_angle, L_temps,
                             L_angle, L_distance, path)
            elif valeur_consigne_distance != 0:
                create_excel(valeur_consigne_distance, L_temps,
                             L_angle, L_distance, path)
            else:
                create_excel(0, L_temps, L_angle, L_distance, path)

            texte1 = "Fichier Excel créé"
            L_Canvas[0].itemconfig(console_text_1, text=texte1)
            L_Canvas[0].coords(console_text_1, 70, 57)
            t0_clear_Canvas = time.time()

            self.bg = 'blue'
            self.config(text='Envoyer échelon', bg=self.bg)

            for i in range(6):
                L_Buttons[i].config(state='normal')

            L_Buttons[0].bg, L_Buttons[0].state, L_Buttons[0].cursor = 'blue', 'on', 'hand2'
            L_Buttons[0].config(bg=L_Buttons[0].bg,
                                state='normal', cursor=L_Buttons[0].cursor)

            L_Buttons[2].bg, L_Buttons[2].fg, L_Buttons[2].state, L_Buttons[2].cursor = 'light blue', 'black', 'off', 'hand2'
            L_Buttons[2].config(bg=L_Buttons[2].bg,
                                fg=L_Buttons[2].fg, cursor=L_Buttons[2].cursor)

            L_Buttons[3].bg, L_Buttons[3].fg, L_Buttons[3].cursor = 'red', 'black', 'hand2'
            L_Buttons[3].config(bg=L_Buttons[3].bg,
                                fg=L_Buttons[3].fg, cursor=L_Buttons[3].cursor)

            L_Buttons[4].bg, L_Buttons[4].fg, L_Buttons[4].cursor, L_Buttons[4].state = 'light blue', 'black', 'hand2', 'off'
            L_Buttons[4].config(bg=L_Buttons[4].bg,
                                fg=L_Buttons[4].fg, cursor=L_Buttons[4].cursor)

            L_Buttons[5].bg, L_Buttons[5].fg, L_Buttons[5].cursor = 'blue', 'black', 'hand2'
            L_Buttons[5].config(bg=L_Buttons[5].bg,
                                fg=L_Buttons[5].fg, cursor=L_Buttons[5].cursor)

        else:  # Le bouton est indisponible
            pass

    def manuel(self):
        if self.state == 'off':
            self.state = 'on'
            self.bg = 'blue'
            self.config(bg=self.bg)

            L_Buttons[0].bg, L_Buttons[0].fg, L_Buttons[0].state = 'light blue', 'black', 'off'
            L_Buttons[0].config(bg=L_Buttons[0].bg, fg=L_Buttons[0].fg)
            L_Buttons[1].bg, L_Buttons[1].fg, L_Buttons[1].cursor = 'grey', 'grey75', 'arrow'
            L_Buttons[1].config(bg=L_Buttons[1].bg,
                                fg=L_Buttons[1].fg, cursor=L_Buttons[1].cursor)
            L_Buttons[4].bg, L_Buttons[4].fg, L_Buttons[4].cursor = 'grey', 'grey75', 'arrow'
            L_Buttons[4].config(bg=L_Buttons[4].bg,
                                fg=L_Buttons[4].fg, cursor=L_Buttons[4].cursor)

            L_Scales[0].x, L_Scales[1].x, L_Scales[2].x = 1800, 1800, 55
            for i in range(3):
                L_Scales[i].place(x=L_Scales[i].x, y=L_Scales[i].y)

            L_Entry[0].x, L_Entry[1].x = 1800, 1800
            for i in range(2):
                L_Entry[i].place(x=L_Entry[i].x, y=L_Entry[i].y)

            L_Buttons[6].x, L_Buttons[7].x = 1800, 1800
            for i in range(6,8):
                L_Buttons[i].place(x=L_Buttons[i].x, y=L_Buttons[i].y)

        else:
            self.state = 'off'
            self.bg = 'light blue'
            self.config(bg=self.bg)

            L_Buttons[0].bg, L_Buttons[0].fg, L_Buttons[0].state = 'blue', 'black', 'on'
            L_Buttons[0].config(bg=L_Buttons[0].bg, fg=L_Buttons[0].fg)
            L_Buttons[1].bg, L_Buttons[1].fg, L_Buttons[1].cursor = 'blue', 'black', 'hand2'
            L_Buttons[1].config(bg=L_Buttons[1].bg,
                                fg=L_Buttons[1].fg, cursor=L_Buttons[1].cursor)
            L_Buttons[4].bg, L_Buttons[4].fg, L_Buttons[4].cursor = 'light blue', 'black', 'hand2'
            L_Buttons[4].config(bg=L_Buttons[4].bg,
                                fg=L_Buttons[4].fg, cursor=L_Buttons[4].cursor)

            L_Scales[0].x, L_Scales[1].x, L_Scales[2].x = 70, 240, 1800
            for i in range(3):
                L_Scales[i].place(x=L_Scales[i].x, y=L_Scales[i].y)

            L_Entry[0].x, L_Entry[1].x = 147, 320
            for i in range(2):
                L_Entry[i].place(x=L_Entry[i].x, y=L_Entry[i].y)

            L_Buttons[6].x, L_Buttons[7].x = 78, 247
            for i in range(6,8):
                L_Buttons[i].place(x=L_Buttons[i].x, y=L_Buttons[i].y)

    def stop(self):
        global valeur_consigne_angle, valeur_consigne_distance, texte1, texte2, go
        valeur_consigne_distance = 0
        valeur_consigne_angle = 0
        print('SORTIE')

        if go == 1:

            # send_to_Arduino(ser, valeur_consigne)
            send_to_board(board, 'manuel', valeur_consigne_angle,
                          valeur_consigne_distance, Servo)

            texte1 = "Valeur de repos envoyée : {} cm.".format(valeur_consigne)
            print(texte1)
            L_Canvas[0].itemconfig(console_text_1, text=texte1)
            L_Canvas[0].coords(console_text_1, 118, 57)

        texte2 = 'Sortie imminente'
        L_Canvas[0].itemconfig(console_text_2, text=texte2)
        L_Canvas[0].coords(console_text_2, 72, 40)

        app.update()
        time.sleep(2)
        app.destroy()

    def experience(self):
        global mode_experience
        if self.bg != 'grey':
            if self.state == 'off':
                self.state = 'on'
                self.bg = 'blue'
                self.config(bg=self.bg)
                mode_experience = 1
            else:
                self.state = 'off'
                self.bg = 'light blue'
                self.config(bg=self.bg)
                mode_experience = 0
        else:
            pass


class tkinterScale(tk.Scale):
    """Graduation pour valeur d'entrée"""

    def __init__(self, id, application):
        global valeur_consigne_distance, valeur_consigne_angle
        tk.Scale.__init__(self, application)
        self.id = id

        valeur_consigne_distance, valeur_consigne_angle = 0, 0

        if self.id == 0:
            self.config(label='Echelon en cm', orient='vertical', from_=50, to=0, cursor='hand2', font='GROBOLD.ttf 10', state='disabled',
                        resolution=1, tickinterval=10, length=200, bg='light blue', fg='grey70', command=self.valeur_consigne_automatique)
            self.x, self.y = 1800, 130

        elif self.id == 1:
            self.config(label='Echelon en °', orient='vertical', from_=90, to=-90, cursor='hand2', font='GROBOLD.ttf 10', state='normal',
                        resolution=1, tickinterval=20, length=200, bg='light blue', command=self.valeur_consigne_automatique)
            self.x, self.y = 1800, 130

        elif self.id == 2:
            self.config(label='Angles', orient='horizontal', from_=-90, to=90, cursor='hand2', font='GROBOLD.ttf 10',
                        resolution=1, tickinterval=15, length=360, bg='light blue', command=self.valeur_consigne_manuel)
            self.x, self.y = 55, 215

    def valeur_consigne_automatique(self, state):
        global valeur_consigne_distance, valeur_consigne_angle
        if self.id == 0:
            valeur_consigne_angle = 0
            valeur_consigne_distance = int(state)
        else:
            valeur_consigne_angle = int(state)
            valeur_consigne_distance = 0

    def valeur_consigne_manuel(self, state):
        global valeur_consigne_distance
        valeur_consigne_distance = 0
        global go
        if go == 1:
            send_to_board(board, 'manuel', int(state), 0, Servo)
        else:
            print('impossible')


class tkinterMenu(tk.Frame):
    """barre menu de l'application"""

    def __init__(self, application):
        global port_usb

        tk.Frame.__init__(self, background='blue')

        # création de la barre de menu
        self.barremenu = tk.Menu(application)

        # Création du menu Fichier
        self.fichier = tk.Menu(self.barremenu, tearoff=0)
        self.barremenu.add_cascade(label='Fichier', menu=self.fichier)
        self.fichier.add_command(
            label='Ouvrir nouveau', command=self.ouvrir_nouveau, font='Arial 10')
        self.fichier.add_separator()
        self.fichier.add_command(
            label='Quitter', command=self.quitter, font='Arial 10 bold')

        # Création du menu 'Outils'
        self.outils = tk.Menu(self.barremenu, tearoff=0)
        self.barremenu.add_cascade(label='Outils', menu=self.outils)
        self.outils.add_command(
            label='Enregistrer Excel sous...', command=self.enregistrer_sous, font='Arial 10')

        # Création du sous menu 'Port' du menu 'Outils'
        self.port = tk.Menu(self.outils, tearoff=0)
        self.outils.add_cascade(label='Port', menu=self.port, font='Arial 10')
        self.port.add_command(
            label='COM 4', command=self.com4, font='Arial 10')
        self.port.add_command(
            label='COM 5', command=self.com5, font='Arial 10')

        application.config(menu=self.barremenu)

    def quitter(self):
        global running
        self.master.destroy()
        running = False

    def com4(self):
        global port_usb

        port_usb = 'COM4'
        L_Canvas[0].itemconfig(console_text_usb, text=port_usb, fill='grey')
        app.update()
        definir_board()

    def com5(self):
        global port_usb

        port_usb = 'COM5'
        L_Canvas[0].itemconfig(console_text_usb, text=port_usb, fill='grey')
        app.update()
        definir_board()

    def ouvrir_nouveau(self):
        global posx, posy
        posx = posx - 10
        posy = posy + 10
        main()

    def enregistrer_sous(self):
        global path, console_text_1, L_Canvas, t0_clear_Canvas

        path = askdirectory()
        print(path)

        texte1 = "Path modifié"
        print(texte1)
        L_Canvas[0].itemconfig(console_text_1, text=texte1)

        app.update()
        t0_clear_Canvas = time.time()


class tkinterCanvas(tk.Canvas):
    """Console d'affichage"""

    def __init__(self, id, application):
        global console_text_1, console_text_2, console_text_usb, donnees_text_0, donnees_text_pot, donnees_text_servo, donnees_text_pot_val, donnees_text_distance, donnees_text_servo_val, donnees_text_temps_val, donnees_text_distance_val
        tk.Canvas.__init__(self, application)
        self.id = id

        if self.id == 0:
            # Console
            self.config(bg="white", height=65, width=600, relief='raised')
            self.x, self.y = 100, 555

            console_text_titre = self.create_text(42, 20, text="Console",
                                                  font="GROBOLD.ttf 10 italic bold", fill="blue")
            console_text_1 = self.create_text(56, 57, text=' ',
                                              font="GROBOLD.ttf 10 italic bold", fill="black")
            console_text_2 = self.create_text(400, 40, text=' ',
                                              font="GROBOLD.ttf 10 italic bold", fill="red")
            console_text_usb = self.create_text(570, 20, text=port_usb,
                                                font="GROBOLD.ttf 10 italic bold", fill="black")

        elif self.id == 1:
            self.config(bg="white", height=100, width=300, relief='raised')
            self.x, self.y = 100, 435

            donnees_text_0 = self.create_text(42, 20, text='Données',
                                              font="GROBOLD.ttf 10 italic bold", fill="blue")

            donnees_text_temps = self.create_text(37, 45, text='Temps',  # 1
                                                  font="GROBOLD.ttf 8 italic", fill="black")
            donnees_text_temps_val = self.create_text(37, 70, text='',
                                                      font="GROBOLD.ttf 8 italic", fill="black")

            donnees_text_pot = self.create_text(113, 45, text='Potentiometre',  # 2
                                                font="GROBOLD.ttf 8 italic", fill="black")
            donnees_text_pot_val = self.create_text(113, 70, text='',
                                                    font="GROBOLD.ttf 8 italic", fill="black")

            donnees_text_servo = self.create_text(187, 45, text='Servo',  # 3
                                                  font="GROBOLD.ttf 8 italic", fill="black")
            donnees_text_servo_val = self.create_text(187, 70, text='',
                                                      font="GROBOLD.ttf 8 italic", fill="black")

            donnees_text_distance = self.create_text(263, 45, text='Distance',  # 4
                                                     font="GROBOLD.ttf 8 italic", fill="black")
            donnees_text_distance_val = self.create_text(263, 70, text='',
                                                         font="GROBOLD.ttf 8 italic", fill="black")

            ligne_1 = self.create_line(75, 40, 75, 130)
            ligne_2 = self.create_line(150, 40, 150, 130)
            ligne_3 = self.create_line(225, 40, 225, 130)


class tkinterLabel(tk.Label):

    def __init__(self, id, application):
        tk.Label.__init__(self, application)
        self.id = id

        if application == app:
            if self.id == 0:
                self.config(text='Interface de pilotage Foil', bg='light blue',
                            fg='blue', width=20, font='GROBOLD.ttf 30 bold')
                self.x, self.y = 160, 35

            if self.id == 1:
                self.config(text='________________________________________________', bg='light blue',
                            fg='blue', width=20, font='GROBOLD.ttf 20')
                self.x, self.y = 240, 385

        elif application == fenetre:
            if self.id == 0:
                self.config(text="Placer le foil à l'horizontal pour définir l'angle 0", bg='grey70',
                            fg='black', width=40, font='GROBOLD.ttf 13 bold')
                self.x, self.y = 10, 70

            if self.id == 1:
                self.config(text="Puis placer le foil à la verticale pour définir l'angle 90", bg='grey70',
                            fg='black', width=42, font='GROBOLD.ttf 13 bold')
                self.x, self.y = 0, 90


class tkinterEntry(tk.Entry):
    """boîtes d'entrée de texte pour consigne"""

    def __init__(self, id, application):
        tk.Entry.__init__(self, application)
        self.id = id

        if self.id == 0:
            self.config(width=5, font='GROBOLD.ttf 15', state='disabled')
            self.bind('<Return>', self.enter)
            self.x, self.y = 1800, 160
        elif self.id == 1:
            self.config(width=5, font='GROBOLD.ttf 15')
            self.bind('<Return>', self.enter)
            self.x, self.y = 1800, 160

    def enter(self, state):
        try:            #l'exception sert à ignorer si l'utilisateur entre une valeur absurde.
            value = int(self.get())
            self.delete(0, END)
            if value >= 0 and value <= 150 and self.id == 0:
                L_Scales[self.id].set(value)
            if value >= -90 and value <= 90 and self.id == 1:
                L_Scales[self.id].set(value)
            if self.id == 0:
                valeur_consigne_distance = value
                valeur_consigne_angle = 0
            elif self.id == 1:
                valeur_consigne_distance = 0
                valeur_consigne_angle = value
        except:
            pass


def create_app(type):

    posx, posy = 450, 0
    posx2, posy2 = 15, 200
    longueur, hauteur = 800, 800
    longueur2, hauteur2 = 150, 150

    app = tk.Tk()
    if type == 'main':
        app.title("Interface de pilotage")
        app.minsize(longueur, hauteur)
        app.resizable(width=False, height=False)
        app.geometry("820x645+{}+{}".format(str(posx), str(posy)))
        app.configure(bg="light blue")
    else:
        app.title("Initialisation du potentiomètre")
        app.minsize(longueur2, hauteur2)
        app.resizable(width=False, height=False)
        app.geometry("430x300+{}+{}".format(str(posx2), str(posy2)))
        app.configure(bg="grey70")

    return app


def create_L_Buttons(application):
    L = []
    for i in range(8):
        L.append(tkinterButton(i, application))
    return L


def create_L_Labels(application):
    L = []
    for i in range(2):
        L.append(tkinterLabel(i, application))
    return L


def create_L_Scales(application):
    L = []
    for i in range(3):
        L.append(tkinterScale(i, application))
    return L


def create_L_Canvas(application):
    L = []
    for i in range(2):
        L.append(tkinterCanvas(i, application))
    return L


def create_L_Entry(application):
    L = []
    for i in range(2):
        L.append(tkinterEntry(i, application))
    return L


def placer_objets(L_Buttons, L_Labels, L_Scales, L_Canvas, L_Entry):

    # place all objects :
    for i in range(len(L_Buttons)):
        L_Buttons[i].place(x=L_Buttons[i].x, y=L_Buttons[i].y)

    for i in range(len(L_Labels)):
        L_Labels[i].place(x=L_Labels[i].x, y=L_Labels[i].y)

    for i in range(len(L_Scales)):
        L_Scales[i].place(x=L_Scales[i].x, y=L_Scales[i].y)

    for i in range(len(L_Canvas)):
        L_Canvas[i].place(x=L_Canvas[i].x, y=L_Canvas[i].y)

    for i in range(len(L_Entry)):
        L_Entry[i].place(x=L_Entry[i].x, y=L_Entry[i].y)


def chronometre(t0):

    t = time.time() - t0
    # Conversion en tuple (1970, 1, 1, 0, 0, 4, 3, 1, 0)
    temps_tuple = time.gmtime(t)
    reste = t - temps_tuple[3] * 3600.0 - temps_tuple[4] * \
        60.0 - temps_tuple[5] * 1.0  # on récupère le reste
    # Affiche les dixièmes et centièmes de l'arrondi
    reste = ("%.2f" % reste)[-2::]
    tt = time.strftime("%H:%M:%S", temps_tuple) + "," + reste
    return tt


def definir_board():
    global go
    try:
        board = pyfirmata.Arduino(port_usb)
        iter8 = pyfirmata.util.Iterator(board)
        iter8.start()

        board.analog[0].enable_reporting()
        board.analog[1].enable_reporting()

        L_Canvas[0].itemconfig(console_text_2, text=' ')
        L_Canvas[0].itemconfig(console_text_usb, text=port_usb, fill='black')
        go = 1

        print(port_usb)
        return board

    except:
        print('Arduino non branchée')
        texte2 = 'Pas de carte Arduino branchée'
        L_Canvas[0].itemconfig(console_text_2, text=texte2)
        L_Canvas[0].coords(console_text_2, 112, 40)

        L_Canvas[0].itemconfig(console_text_usb, text=port_usb, fill='black')

        go = 0
        return False


def main():
    global app, path, board, L_Buttons, L_Labels, L_Scales, L_Canvas, L_Entry, L_Labels_init, L_Buttons_init, mode_experience, valeur_consigne
    global port_usb, running, Servo, Potentiometre, Capteur, L_temps, L_angle, L_distance, consigne, acquerir, zero, quatre_vingt_dix
    # obligé de mettre beaucoup de variables en global car l'appel aux fonctions liées aux boutons doivent avoir qu'un seul argument (self)

    app = create_app('main')
    # Pour la barre Menu (la barre menu ne fonctionne pas dans l'app)
    Frame = tk.Frame(app, bg='blue')

    Frame.place(x=0, y=0)

    port_usb = 'COM5'
    path = 'C:/Users/cleme/Desktop/Documents/1. DOCUMENTS CLEMENT/TRAVAIL/Post BAC/MP/TIPE/Modèle expérimental/Info/Arduino-Python-Excel CODE 2/Code 2.3'
    # path = str(os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])))
    #Chemin du dossier

    mode_experience, t0_experience = 0, 0
    valeur_consigne = 0

    BarreMenu = tkinterMenu(app)
    L_Buttons = create_L_Buttons(app)
    L_Labels = create_L_Labels(app)
    L_Scales = create_L_Scales(app)
    L_Canvas = create_L_Canvas(app)
    L_Entry = create_L_Entry(app)

    placer_objets(L_Buttons, L_Labels, L_Scales, L_Canvas, L_Entry)

    board = definir_board()
    Servo = ArduinoServo(board)
    Potentiometre = ArduinoPotentiometre(board)
    Capteur = ArduinoCapteur(board)
    acquerir, zero, quatre_vingt_dix = 0, 0, 1

    # consigne et Listes de valeurs à envoyer à excel
    consigne, L_temps_brut, L_temps_net, L_angle, L_distance = 0, [], [], [], []

    running = True
    t0 = time.time()
    # 'numero_boucle' permet d'avoir le bon nombre de valeurs dans le fichier excel (il y en aurait beaucoup si on append à toutes les boucles)
    numero_boucle = 0
    while running == True:
        numero_boucle += 1
        get_from_board(board, Servo, Potentiometre, Capteur) #récupérer les valeurs des objets arduino

        t = chronometre(t0)
        valeur_servo = Servo.val - 90
        try: valeur_potentiometre = ((float(Potentiometre.val)-zero)*(90-0))/((quatre_vingt_dix-zero))
        except: valeur_potentiometre = Potentiometre.val

        try:texte_pot = "%.3f" % valeur_potentiometre  #réduire les chiffres significatifs # au début, le type est 'NoneType', d'ou l'exception
        except:texte_pot = valeur_potentiometre

        try:
            # temps qui s'écoule
            L_Canvas[1].itemconfig(donnees_text_temps_val, text=t)
            # Valeur envoyée au Servo
            L_Canvas[1].itemconfig(donnees_text_servo_val, text=valeur_servo)
            # Valeur rendue par le potentiomètre
            L_Canvas[1].itemconfig(donnees_text_pot_val, text= texte_pot)
            # Valeur rendue par le capteur de distance
            L_Canvas[1].itemconfig(donnees_text_distance_val, text=Capteur.val)

            if acquerir == 1 and numero_boucle % 3 == 0: #réduire le nombre de valeurs acquises
                L_temps_brut.append(time.time()- t0)
                L_temps_net.append(time.time() - t0_experience)
                L_angle.append(valeur_potentiometre)
                L_distance.append(Capteur.val)

            if L_Scales[2].x == 1800:
                # set le scale qui ne figure pas : confort de pilotage
                L_Scales[2].set(Servo.val - 90)

            try:  # Si le texte est affiché dans le canvas depuis assez longtemps, on le supprime
                duree_Canvas = time.time() - t0_clear_Canvas
                if duree_Canvas > 2 and duree_Canvas < 2.2:
                    L_Canvas[0].itemconfig(console_text_1, text='')
            except: pass

            app.update()

        except: #sortir de la boucle while car l'application a été fermée
            running = False


if __name__ == '__main__':
    main()

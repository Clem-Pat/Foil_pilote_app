import pyfirmata
import numpy as np
"""créer une fonction pour convertir la consigne (appartient à -90,90) en valeur pour le servo (0,180)"""


class ArduinoServo():
    """Moteur Servo"""

    def __init__(self, board):
        self.type = 'digital'
        self.board = board
        try:
            self.pin = board.get_pin('d:9:s')
        except:
            self.pin = False
        self.val = 90  # (appartient à [0,180])

        try:
            self.move()
        except:
            pass

    def move(self):
        self.pin.write(self.val)

    def calculer_angle(self, distance):
        # dépend du profil du foil et de la vitesse du vent
        return 5


class ArduinoPotentiometre():
    """Potentiomètre"""

    def __init__(self, board):
        self.type = 'analog'
        self.board = board
        self.val = 0
        try:
            self.pin = board.analog[0]  # la sortie A0
        except:
            self.pin = False


class ArduinoCapteur():
    """Capteur infra-rouge. PLAGE : 5cm-50cm"""
    """ limite : approximation de la modélisation du capteur """

    def __init__(self, board):
        self.type = 'analog'
        self.board = board
        try:
            self.pin = board.analog[1]  # la sortie A1
            self.val = self.pin.read()

        except:
            self.pin = False
            self.val = 0


def equation_capteur(x):
    """retourne la valeur de la distance captée"""
    try:
        return float(48.366*np.exp(-(float(x)-0.102)/0.109)+7.931)
    except:
        return 0

def send_to_board(board, pilote, valeur_angle, valeur_distance, Servo):
    # 'valeur' peut etre un angle si le pilote est manuel ou une distance si le pilote est automatique

    if pilote == 'manuel':
        Servo.val = valeur_angle + 90
        Servo.move()  # car 'valeur_angle' est un angle entre -90 et 90

    if pilote == 'automatique':
        if valeur_angle != 0:
            Servo.val = valeur_angle + 90
            Servo.move()
        if valeur_distance != 0:
            Servo.val = Servo.calculer_angle(valeur_distance)
            Servo.move()
        else:
            # Si c'est le cas du STOP
            Servo.val = valeur_angle + 90
            Servo.move()

def get_from_board(board, Servo, Potentiometre, Capteur):

    if board == False:
        Potentiometre.val = 0
        Capteur.val = 0
    else:
        Potentiometre.val = Potentiometre.pin.read()  # Potentiometre
        Capteur.val = equation_capteur(Capteur.pin.read())  # distance captée

    return Potentiometre.val, Servo.val, Capteur.val

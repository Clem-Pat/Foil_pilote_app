"""aperçu des courbes"""

import math
import matplotlib.pyplot as plt

def afficher_apercu(L0,L2,L3):
    plt.plot(L0,L2,'g')
    plt.plot(L0,L3,'b')

    plt.show()

afficher_apercu([1,2,3,4],[1,2,3,4],[2,4,6,8])

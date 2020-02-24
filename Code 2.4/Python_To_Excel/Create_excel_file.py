import os
import pandas as pd
import openpyxl


def create_excel(consigne,L0,L1,L2,L3,path):
    """crée le fichier excel de l'expérience"""
    if len(L0) == len(L1) and len(L0) == len(L2):
        df = pd.DataFrame({ 'temps brut (s)':L0,
                            'temps net (s)': L1,
                            'Angle (°)': L2,
                            'Distance (cm)': L3})

        writer = pd.ExcelWriter(path+'/Valeurs pour alpha={}.xlsx'.format(consigne))
        df.to_excel(writer, sheet_name='Valeurs pour {}'.format(consigne), index=False)

        writer.save()
        print("Fichier excel cree a l'adresse {} nomme << Valeurs pour alpha={} >>".format(path,consigne))
    else:
        print('les listes doivent être de la même longueur')

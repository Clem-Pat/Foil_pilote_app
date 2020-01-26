import os
import pandas as pd
import openpyxl


def create_excel(consigne,L0,L1,L2,path):
    """crée le fichier excel de l'expérience"""
    if len(L0) == len(L1) and len(L0) == len(L2):
        df = pd.DataFrame({'temps(ms)': L0,
                            'Angle(°)': L1,
                            'Distance(cm)': L2})

        writer = pd.ExcelWriter(path+'/Valeurs pour alpha={}.xlsx'.format(consigne))
        df.to_excel(writer, sheet_name='Valeurs pour {}'.format(consigne), index=False)

        writer.save()
        print('Excel file created')
    else:
        print('les listes doivent être de la même longueur')

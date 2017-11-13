#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:12:50 2017

@author: olivier
@desc: Retrieves specific data for certain types of medicines
"""

import re
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

URL = 'http://base-donnees-publique.medicaments.gouv.fr/index.php#result'
def displayMedocInDataFrame(nbPages, nomMedoc):
    moleculeMedoc = []
    dosageMedoc = []
    typeMedoc = []

    for i in range(1, nbPages):
        parametresPost = {'page':str(i),
        'affliste':'0',
        'affNumero':'0',
        'isAlphabet':'0',
        'inClauseSubst':'0',
        'nomSubstances':'',
        'typeRecherche':'0',
        'choixRecherche':'medicament',
        'paginationUsed':'0',
        'txtCaracteres': nomMedoc,
        'btnMedic.x':'0',
        'btnMedic.y':'0',
        'btnMedic':'Rechercher',
        'radLibelle':'2',
        'txtCaracteresSub':'',
        'radLibelleSub':'4'}

        resultsPost = requests.post(URL, data=parametresPost)
        resultsParser = BeautifulSoup(resultsPost.text, 'html.parser')
        listMedocs = resultsParser.find_all(class_="standart")

        for medoc in listMedocs:
            my_reg = re.compile('(^IBUPROFENE)\s+(\D[A-Z]+\s)+')
            resultMatch  = my_reg.search(medoc.text)
            if(resultMatch):
                moleculeMedoc.append(resultMatch.group(0))
            else:
                moleculeMedoc.append("")

            my_reg = re.compile('((\d+\s)|(\d))(%|\w+[^a-zA-Z0-9,]\w+)')
            resultMatch  = my_reg.search(medoc.text)
            if(resultMatch):
                dosageMedoc.append(resultMatch.group(0))
            else:
                dosageMedoc.append("")

            my_reg = re.compile(',\s(.)+')
            resultMatch  = my_reg.search(medoc.text)
            if(resultMatch):
                typeMedoc.append(resultMatch.group(0).replace(",", ""))
            else:
                typeMedoc.append("")

    df = pd.DataFrame({"Molecule":moleculeMedoc ,  "dosage": dosageMedoc,
      "type":typeMedoc})
    df['Molecule'] = df['Molecule'].replace("", np.nan)
    df = df.dropna(axis=0)
    df = df.set_index(np.arange(df.shape[0]))
    print(df)

    df.to_csv("medicament.csv", sep=',')

displayMedocInDataFrame(5, "ibuprofene")
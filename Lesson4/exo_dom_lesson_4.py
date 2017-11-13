#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:12:50 2017

@author: olivier
@desc: Get from generic url to search all Renault Zoe sales in regions Ile-de-france, Aquitaine and PACA
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

marque = 'Renault'
modele = 'Zoe'
region = ['provence_alpes_cote_d_azur', 'ile_de_france', 'aquitaine']
page = 2

# If typePrix is true, s is a price otherwise it's a distance
def clearData(s, typePrix):
    for i in s:
        if(typePrix == True):
            if i == ' ':
                s = s.replace(' ', '')
            if i == '€':
                s = s.replace('€', '')
        else:
            for i in s:
                if i == ' ':
                    s = s.replace(' ', '')
                if i == 'K':
                    s = s.replace('K', '')
                if i == 'M':
                    s = s.replace('M', '')
    return s

def completeCarFeatures(paramAllCarIds):
  allCarIds = paramAllCarIds
  sizeTab = len(allCarIds)
  KILOMETRAGES_ = np.zeros(sizeTab)
  PRIX_ = np.zeros(sizeTab)
  ANNEES_=  np.zeros(sizeTab)

  for i in range(1, len(allCarIds)):

     result = requests.get('https://www.leboncoin.fr/voitures/'
      + str(allCarIds[i])
      + '.htm?ca=12_s')
     soup = BeautifulSoup(result.text, 'html.parser')

     MONTANT = soup.find_all(class_='value')
     annee = MONTANT[4].get_text()
     ANNEES_[i] = int(float(annee))

     prix = MONTANT[0].get_text()
     prix = clearData(prix, True)
     PRIX_[i] = int(prix)

     kilometrage = MONTANT[5].get_text()
     kilometrage = clearData(kilometrage, False)
     KILOMETRAGES_[i] = int(kilometrage)
  return KILOMETRAGES_, ANNEES_, PRIX_

# Search for car data by region, make, model and model by individual or professional
def getDataUnitary(paramRegion,paramMarque, paramModele, paramTypeRecherche):
    LOC_REGION = paramRegion
    LOC_MODELE = paramModele
    LOC_MARQUE = paramMarque
    LOC_RECHERCHE = paramTypeRecherche
    CAR_ID = dirty_car_id = []

    for PAGE in range(1,page):
        if LOC_RECHERCHE == 0:
            URL_PROFESSIONNEL = 'https://www.leboncoin.fr/voitures/offres/' + LOC_REGION + '/?o=' + str(PAGE) + '&brd=' + LOC_MARQUE + '&mdl=' + LOC_MODELE + '&f=c'

            RESULTS = requests.get(URL_PROFESSIONNEL)
            SOUP_PROFESSIONNEL = BeautifulSoup(RESULTS.text,'html.parser')
            MAIN_CONTENT = (SOUP_PROFESSIONNEL.find_all(class_='tabsContent block-white dontSwitch'))

        elif LOC_RECHERCHE == 1:
            URL_PARTICULIER = 'https://www.leboncoin.fr/voitures/offres/' + LOC_REGION + '/?o=' + str(PAGE) + '&brd=' + LOC_MARQUE + '&mdl=' + LOC_MODELE + '&f=p'
            RESULTS = requests.get(URL_PARTICULIER)
            SOUP_PARTICULIER = BeautifulSoup(RESULTS.text,'html.parser')
            MAIN_CONTENT = (SOUP_PARTICULIER.find_all(class_='tabsContent block-white dontSwitch'))

        if (LOC_RECHERCHE == 0) or (LOC_RECHERCHE == 1):
            for content in MAIN_CONTENT:
                ALL_LI_TAG = content.find_all('li')
                for li_tag in ALL_LI_TAG:
                    info_from_li_tag = (li_tag.contents[1].get('data-info')).replace(':','')
                    info_from_li_tag = info_from_li_tag.replace(',','')
                    dirty_car_id.append(info_from_li_tag.split()[5])

            for i in range(len(dirty_car_id)):
                CAR_ID[i] = dirty_car_id[i].replace('"', '')
        else:
            print('Please enter the type of search: Private individual = %d, Professional = %d' %(0, 1))

    KILOMETRAGES = ANNEES =  PRIX = []
    KILOMETRAGES, ANNEES, PRIX = completeCarFeatures(CAR_ID)

    if LOC_RECHERCHE == 0:
        type_recherche = "PARTICULIER"
    if LOC_RECHERCHE == 1:
         type_recherche = "PROFESSIONNEL"
    df = pd.DataFrame({'region': LOC_REGION, 'kilometrage':KILOMETRAGES, 'annee':ANNEES, 'prix': PRIX, 'marque' : LOC_MARQUE, 'modele': LOC_MODELE,
              'ID voiture': CAR_ID, 'type recherche': type_recherche})
    return  df

def getALLCarsData():
    ALL_CAR_ID = pd.DataFrame()
    df1 = getDataUnitary(region[0], marque, modele, 0)  #PACA PARTICULIER
    df2 = getDataUnitary(region[1], marque, modele, 0)  #IDF PARTICULIER
    df3 = getDataUnitary(region[2], marque, modele, 0) #AQUITAINE PARTICULIER

    df4 = getDataUnitary(region[0], marque, modele, 1)  #PACA PROFESSIONNEL
    df5 = getDataUnitary(region[1], marque, modele, 1) #IDF PROFESSIONNEL
    df6 = getDataUnitary(region[2], marque, modele, 1)  #AQUITAINE PROFESSIONNEL

    ALL_CAR_ID = pd.concat([df1, df2, df3, df4, df5, df6])

    ALL_CAR_ID = ALL_CAR_ID.set_index(np.arange( ALL_CAR_ID.region.count()))
    ALL_CAR_ID.to_csv('data_ca_leboncoin.csv')
    print(ALL_CAR_ID)

getALLCarsData()
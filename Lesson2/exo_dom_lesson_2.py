#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:12:50 2017

@author: olivier
@desc: Crawler for financial results of accounts of Paris from 2010 to 2015
"""

import csv
import requests
from bs4 import BeautifulSoup

def extractValueFromSoup(soup,classparent,classchild,positionParent,positionChild):
    result = soup.findAll(class_=classparent)[positionParent].findAll(class_=classchild)[positionChild].text.replace('\xa0','')
    return result

def getAccountsByYear(years,idcommune,dep):
    accounts = []
    for year in years:
        account = {}
        inconnues =[]

        if len(inconnues) > 5 :
            break

        accountYear = requests.get("http://alize2.finances.gouv.fr/communes/eneuro/detail.php?icom="
            + idcommune
            + "&dep="
            + dep
            + "&type=BPS&param=5&exercice="
            + str(year))

        soupAccount = BeautifulSoup(accountYear.text,'html.parser')

        try:
            account['Id Commune'] = idcommune
            account['dept'] = dep
            account['year'] = year
            account['eurohabA'] = extractValueFromSoup(soupAccount,'bleu',
                'montantpetit G',3,1)
            account['moyennestrateA'] = extractValueFromSoup(soupAccount,'bleu',
                'montantpetit G',3,2)
            account['eurohabB'] = extractValueFromSoup(soupAccount, 'bleu',
                'montantpetit G', 7, 1)
            account['moyennestrateB'] = extractValueFromSoup(soupAccount, 'bleu',
                'montantpetit G', 7, 2)
            account['eurohabC'] = extractValueFromSoup(soupAccount, 'bleu',
                'montantpetit G', 15, 1)
            account['moyennestrateC'] = extractValueFromSoup(soupAccount, 'bleu',
                'montantpetit G', 15, 2)
            account['eurohabD'] = extractValueFromSoup(soupAccount, 'bleu',
                'montantpetit G', 20, 1)
            account['moyennestrateD'] = extractValueFromSoup(soupAccount, 'bleu',
                'montantpetit G', 20, 2)
            accounts.append(account)
        except:
            print("ID cities: " + idcommune + " unknown")
            inconnues.append(idcommune)
    return accounts

def prettyPrintAccounts(accounts):
    for account in accounts:
        print("Year: "+str(account.get('year')))
        print("Township: "+account.get('Id Commune'))
        print("Produit de fonctionnement en euro par habitant: "
            + account.get('eurohabA'))
        print("Average operating product of the stratum: "
            + account.get('moyennestrateA'))
        print("Operating costs in euro per capita: "
            + account.get('eurohabB'))
        print("Average operating load of the stratum: "
            + account.get('moyennestrateB'))
        print("Investment resource in euro per capita per capita: "
            + account.get('eurohabC'))
        print("Average investment resource of the stratum: "
            + account.get('moyennestrateC'))
        print("Investment employment in euros per capita in euro: "
            + account.get('eurohabD'))
        print("Average investment employment of the stratum: "
            + account.get('moyennestrateD'))

def exportToCsv(commune):
    try:
        with open("accounts" + dep + ".csv", "a") as f:
            w = csv.DictWriter(f, fieldnames=["Id Commune","dept","year","eurohabA",
                "moyennestrateA","eurohabB", "moyennestrateB", "eurohabC",
                "moyennestrateC","eurohabD","moyennestrateD"],
                extrasaction='ignore', delimiter = ';')
            w.writerow(commune)
    except IOError :
        print("Error")
    return

idcommunesducalvados = [Y for Y in range(1,764)]
dep = '014'
for id in idcommunesducalvados:
    communeDuCalvados = getAccountsByYear([X for X in range(2015, 2016)],
        str(id).zfill(3), dep)
    prettyPrintAccounts(communeDuCalvados)
    for commune in communeDuCalvados :
        print(commune)
        exportToCsv(commune)
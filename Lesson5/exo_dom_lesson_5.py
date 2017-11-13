#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:12:50 2017

@author: olivier
@desc: doctors per city
"""

import pandas as pd
import numpy as np

# Table of the different specialities
listCol = ("Généralistes", "MEP", "Omnipraticiens","Anesthésistes",
           "Cardiologues","Chirurgiens","Dermatologues","Radiologues",
           "Gynécologues","Gastro-entérologues","ORL","Pédiatres",
           "Rhumatologues","Ophtalmologues","Stomatologues",
           "Psychiatres")

arrayCol = ["Généralistes", "MEP", "Omnipraticiens","Anesthésistes",
           "Cardiologues","Chirurgiens","Dermatologues","Radiologues",
           "Gynécologues","Gastro-entérologues","ORL","Pédiatres",
           "Rhumatologues","Ophtalmologues","Stomatologues",
           "Psychiatres"]

def cleanData(df):
    for col in listCol:
        df[col] = df[col].replace("nc", 0)

    df = df[df.Département != 'France métropolitaine']
    df = df[df.Département != 'France entière']
    df.fillna(0, inplace=True)
    return df

def genererDonnesMedecinsAPE():
    dfDensiteMedecinsParDept = pd.read_excel("Patientele_des_medecins_APE.xls",
                       sheetname=2, skiprows=3)
    dfDensiteMedecinsParDept = cleanData(dfDensiteMedecinsParDept)
    dfDensiteMedecinsParDept.to_csv("densite_medecin_departement.csv")

    dfPatienteleAPE = pd.read_excel("Patientele_des_medecins_APE.xls",
      sheetname="Patientèle", skiprows=3)
    dfPatienteleAPE = cleanData(dfPatienteleAPE)

    dfHonorairesTotaux = pd.read_excel("Patientele_des_medecins_APE.xls",
      sheetname="Honoraires totaux par patient", skiprows=3)
    dfHonorairesTotaux = cleanData(dfHonorairesTotaux)
    dfHonorairesTotaux.to_csv("honoraires_totaux.csv")

    dfHonorSansDepass = pd.read_excel("Patientele_des_medecins_APE.xls",
      sheetname="HSD par patient", skiprows=3)
    dfHonorSansDepass = cleanData(dfHonorSansDepass)
    dfHonorSansDepass.to_csv("honor_sans_depass.csv")

    dfNombreActesPatients = pd.read_excel("Patientele_des_medecins_APE.xls",
      sheetname="Nombre d'acte par patient", skiprows=3)
    dfNombreActesPatients = cleanData(dfNombreActesPatients)
    return dfDensiteMedecinsParDept, dfPatienteleAPE, dfHonorairesTotaux, dfHonorSansDepass, dfNombreActesPatients


dfDensiteMedecinsParDept, dfPatienteleAPE, dfHonorairesTotaux, dfHonorSansDepass, dfNombreActesPatients = genererDonnesMedecinsAPE()

def calculerDepassHonoraires(df1, df2):
    df = df1
    for col in listCol:
        df[col] =  df1[col] - df2[col]
    df.to_csv("depassement_honoraires_dept_specialite.csv")
    return df

df_HonorAvecDepass = calculerDepassHonoraires(dfHonorairesTotaux, dfHonorSansDepass)

def genererDensityPopulation():
    df = pd.read_excel("Effectif_et_densite_par_departement.xls", sheetname=3)
    df = df[df.DEPARTEMENT != 'TOTAL FRANCE METROPOLITAINE']
    df = df[df.DEPARTEMENT != 'TOTAL OUTRE-MER']
    return df

df_DensitePop = genererDensityPopulation()
df_DensitePop =  df_DensitePop[["DEPARTEMENT", "POPULATION FRANCAISE"]].drop_duplicates()
df_DensitePop.rename(columns={"DEPARTEMENT":"Département"}, inplace=True)

df_merge_metrics = df_DensitePop.merge(df_HonorAvecDepass)
df_merge_metrics.to_csv("depassement_honoraires_metrics.csv")
print(df_merge_metrics.describe())

dep_par_dep = df_merge_metrics.groupby("Département")[arrayCol].sum()
print(dep_par_dep)
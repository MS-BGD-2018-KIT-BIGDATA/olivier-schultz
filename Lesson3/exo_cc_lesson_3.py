# @author : SCHULTZ Olivier
# @version : 1.0
# @desc : pourcentage Dell vs Acer on cdiscount

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def findPromo(brand,page):
    url = 'http://www.cdiscount.com/search/10/' + brand + '.html?TechnicalForm.SiteMapNodeId=0&TechnicalForm.DepartmentId=10&TechnicalForm.ProductId=&hdnPageType=Search&TechnicalForm.SellerId=&TechnicalForm.PageType=SEARCH_AJAX&TechnicalForm.LazyLoading.ProductSheets=False&NavigationForm.CurrentSelectedNavigationPath=f%2F1%2F0k&FacetForm.SelectedFacets.Index=0&FacetForm.SelectedFacets.Index=1&FacetForm.SelectedFacets.Index=2&FacetForm.SelectedFacets.Index=3&FacetForm.SelectedFacets.Index=4&FacetForm.SelectedFacets.Index=5&FacetForm.SelectedFacets.Index=6&FacetForm.SelectedFacets.Index=7&FacetForm.SelectedFacets.Index=8&GeolocForm.ConfirmedGeolocAddress=&SortForm.SelectedSort=PERTINENCE&ProductListTechnicalForm.Keyword=acer&page='+ str(page) + '&_his_'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    cells = soup.findAll('div', {"class" : "prdtBZPrice"})
    listData=[]

    for cell in cells:
        promo = cell.find('span', { "class" : 'price'})
        price  = cell.find('div', { "class" : 'prdtPrSt'})
        #print("price", price)
        #print("promo",promo)

        if not promo is None and not price is None and price.text != '':
            pricer = price.text.replace('€', ',')

            promr = promo.text.replace('€', ',')

            moyenne = ((float(pricer.replace(',','.'))-float(promr.replace(',','.')))/float(pricer.replace(',','.')))*100
            listData.append(moyenne)

    return(np.mean(listData))

promo = findPromo('dell', '2')
print("Promo Dell en pourcentage : ", promo,"%")

promo = findPromo('acer', '2')
print("Promo Acer en pourcentage : ", promo,"%")
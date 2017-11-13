#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 15:12:50 2017

@author: olivier
@desc: top 256 contributors in https://gist.github.com/paulmillr/2657075
"""

import json
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup

# Get users name from GitHub
url = 'https://gist.github.com/paulmillr/2657075'
token = 'c6d6f524a51e72bdd42b1e34a278e39d3b536360'
page = 1

def extractDataForPage(soup):
  body = []
  row = []
  name = []

  table = soup.find_all(class_= 'readme blob instapaper_body')
  for t in table:
      body.extend(t.find_all('tbody'))

  for b in body:
      row = b.select('a[href^="https://github.com/"]')

  for r in row:
      name.append(r.text)

  print ("There are %s famous users" %len(name))
  return name

def getFamousGithubContributorsFromDOM(url):
    results = rq.get(url)
    soup = BeautifulSoup(results.text,'html.parser')
    name = extractDataForPage(soup)
    return name

def getStarsNumberForAllUser():

    user_repCount_starCount = []
    starCount = 0
    repCount = 0
    temp = []

    name = getFamousGithubContributorsFromDOM(url)
    print("[user name, " + "number of repositories, " + "number of stars, "
      + "mean stars per repo]")

    if len(name) > 0:
        for user in name[0:]:
            results = rq.get("https://api.github.com/users/" + user
              + "/repos?page=" + str(page), auth=(user, token))

            userList = json.loads(results.text)
            if len(userList) > 0:
                for repo in userList:
                    starCount += repo['stargazers_count']
                    repCount += 1

                temp = [user, repCount, starCount]
                if repCount > 0:
                    temp.append(starCount / repCount)
                else:
                    temp.append(0)
                print(temp)
                user_repCount_starCount.append(temp)

    df_contributor = pd.DataFrame(user_repCount_starCount)
    df_contributor.columns = ["user name", "number of repositories",
    "number of stars", "mean stars per repo"]
    print(df_contributor)
    df_contributor.to_csv('top_contributors_github.csv')

getStarsNumberForAllUser()
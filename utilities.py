import requests
import json
from collections import defaultdict
import pandas as pd

import glob
import os
from datetime import datetime


cookies_var="reese84=3:qEfE+a6RMfmMQrdC5u/ZOQ==:lJ5VpSzBhfp/NaB7lNIe5jP9z8d9O9k72SJVJNn/HUrUtkTIK/mkJQ11HodLOIh9prs/M40Y7q636elxpdK/N/SkbyWzb3/OXracUpGb/Zq9kTEk/xRN5dlsDKfSJcLDM+NI/EGrpD6QZqWiM4xkAagEGnll8Q/tbEt+yC/vUiBlR4Jl3gcwcuAcAi/pi/sqkuex5vjEkdqAWsfKF0E0a8ZBietUTCm7xezzP/jVnk0mherFfivVA0ih4AEK5W1jMHtvyua9cv3GfVH+pLwO+pnILgUZvpYKUnxxDgmTfDIZeirkMtKb0+Ilv75nK0EeXvP9U7FKEZMWWUO2EgFB5PpiGIhUebw1k5V40Kk/CBekJhLE8Y25b7iOwQG705odw2FB9YOSzT+KJKKWQu8gfj2lKUbnuLDE7Xlv+LFdwTo=:/RrUcr1lKnzokAzK/evgEXR3cAd1bj0D8zsd6Jlw97g=;"
def scraping_wohnung_mieten():
    url = 'https://www.immobilienscout24.de/Suche/de/wohnung-mieten?sorting=2'
    response = requests.post(url, headers = {"Cookie": cookies_var})
    json_data = json.loads(response.text)
    pageSize=json_data['searchResponseModel']['resultlist.resultlist']['paging']['pageSize']
    realEstate=defaultdict(list)
    numberOfPages=json_data['searchResponseModel']['resultlist.resultlist']['paging']['numberOfPages']
    
        
    path = os.path.join(os.getcwd(), "Data/Apartment/Rent/")
    list_of_files = glob.glob(f"{path}/*.csv") 

    latest_file = max(list_of_files, key=os.path.getmtime)
    df_last=pd.read_csv(latest_file,sep=";",nrows=1,usecols=["creation"])
    last_ads=datetime.strptime(df_last['creation'].tolist()[0][:10]+" "+df_last['creation'].tolist()[0][11:19], '%Y-%m-%d %H:%M:%S')
    
    for i in range(0,int(numberOfPages)):
        url = 'https://www.immobilienscout24.de/Suche/de/wohnung-mieten?sorting=2&pagenumber='+str(i+1)
        response = requests.post(url, headers = {"Cookie": cookies_var})
        json_data = json.loads(response.text)

        pageSize=json_data['searchResponseModel']['resultlist.resultlist']['paging']['pageSize']
        for j in range(pageSize):
            Annoncement_list=json_data['searchResponseModel']['resultlist.resultlist']['resultlistEntries'][0]['resultlistEntry'][j]


            realEstate_json=Annoncement_list["resultlist.realEstate"]
           
            if(datetime.strptime(Annoncement_list["@creation"][:10]+" "+Annoncement_list["@creation"][11:19], '%Y-%m-%d %H:%M:%S')<last_ads):
                return(realEstate)

            realEstate['ID'].append(str(realEstate_json[u'@id']))
            realEstate['url'].append(str(u'https://www.immobilienscout24.de/expose/%s' % str(realEstate_json[u'@id'])))
            realEstate["creation"].append(Annoncement_list["@creation"])
            realEstate["Haus/Wohnung"].append("Wohnung")

            realEstate['address'].append(str(realEstate_json['address']['description']['text']))
            realEstate['city'].append(str(realEstate_json['address']['city']))
            realEstate['postcode'].append(str(realEstate_json['address']['postcode']))
            realEstate['quarter'].append(str(realEstate_json['address']['quarter']))

            try:
                realEstate['firstname'].append(str(realEstate_json['contactDetails']['firstname']))
            except:
                realEstate['firstname'].append(str("no value"))


            try:
                realEstate['lastname'].append(str(realEstate_json['contactDetails']['lastname']))
            except:
                realEstate['lastname'].append(str("no value"))

            try:
                realEstate['phoneNumber'].append(str(realEstate_json['contactDetails']['phoneNumber']))
            except:
                realEstate['phoneNumber'].append(str("no value"))

            try:
                realEstate['company'].append(str(realEstate_json['contactDetails']['company']))
            except:
                realEstate['company'].append(str("no value"))

            realEstate['title'].append(str(realEstate_json['title']))

            realEstate['numberOfRooms'].append(str(realEstate_json['numberOfRooms']))
            realEstate['livingSpace'].append(str(realEstate_json['livingSpace']))

            realEstate['balcony'].append(str(realEstate_json['balcony']))
            realEstate['builtInKitchen'].append(str(realEstate_json['builtInKitchen']))
            realEstate['garden'].append(str(realEstate_json['garden']))
            realEstate['price'].append(str(Annoncement_list["resultlist.realEstate"]['price']['value'])+" "+str(Annoncement_list["resultlist.realEstate"]['price']['currency']))
            realEstate['privateOffer'].append(str(realEstate_json['privateOffer']))

            realEstate['floorplan'].append(str(realEstate_json['floorplan']))
            try:
                realEstate['Warm_miete'].append(str(realEstate_json['calculatedTotalRent']['totalRent']['value'])+" "+str(realEstate_json['calculatedTotalRent']['totalRent']['currency'])+"/"+str(realEstate_json['calculatedTotalRent']['totalRent']['priceIntervalType']))
            except: 
                realEstate['Warm_miete'].append(str(None))

            try:
                realEstate['lat'].append(str(realEstate_json['address'][u'wgs84Coordinate']['latitude']))
            except:
                realEstate['lat'].append(str("no value"))

            try:
                realEstate['lon'].append(str(realEstate_json['address'][u'wgs84Coordinate']['longitude']))
            except:
                realEstate['lon'].append(str("no value"))
                
    return(realEstate)
    
    
    
def scraping_haus_mieten():
    url = 'https://www.immobilienscout24.de/Suche/de/haus-mieten?sorting=2'
    response = requests.post(url, headers = {"Cookie":cookies_var})
    json_data = json.loads(response.text)
    pageSize=json_data['searchResponseModel']['resultlist.resultlist']['paging']['pageSize']
    realEstate=defaultdict(list)
    numberOfPages=json_data['searchResponseModel']['resultlist.resultlist']['paging']['numberOfPages']
    
    path = os.path.join(os.getcwd(), "Data/House/Rent/")
    list_of_files = glob.glob(f"{path}/*.csv") 

    latest_file = max(list_of_files, key=os.path.getmtime)
    df_last=pd.read_csv(latest_file,sep=";",nrows=1,usecols=["creation"])
    last_ads=datetime.strptime(df_last['creation'].tolist()[0][:10]+" "+df_last['creation'].tolist()[0][11:19], '%Y-%m-%d %H:%M:%S')
    
    for i in range(0,int(numberOfPages)):
        url = 'https://www.immobilienscout24.de/Suche/de/haus-mieten?sorting=2&pagenumber='+str(i+1)
        response = requests.post(url, headers = {"Cookie": cookies_var})
        json_data = json.loads(response.text)

        pageSize=json_data['searchResponseModel']['resultlist.resultlist']['paging']['pageSize']
        for j in range(pageSize):
            Annoncement_list=json_data['searchResponseModel']['resultlist.resultlist']['resultlistEntries'][0]['resultlistEntry'][j]


            realEstate_json=Annoncement_list["resultlist.realEstate"]
                       
            if(datetime.strptime(Annoncement_list["@creation"][:10]+" "+Annoncement_list["@creation"][11:19], '%Y-%m-%d %H:%M:%S')<last_ads):
                return(realEstate)
                
            realEstate['ID'].append(str(realEstate_json[u'@id']))
            realEstate['url'].append(str(u'https://www.immobilienscout24.de/expose/%s' % str(realEstate_json[u'@id'])))
            realEstate["creation"].append(Annoncement_list["@creation"])
            realEstate["Haus/Wohnung"].append("Haus")

            realEstate['address'].append(str(realEstate_json['address']['description']['text']))
            realEstate['city'].append(str(realEstate_json['address']['city']))
            realEstate['postcode'].append(str(realEstate_json['address']['postcode']))
            realEstate['quarter'].append(str(realEstate_json['address']['quarter']))

            try:
                realEstate['firstname'].append(str(realEstate_json['contactDetails']['firstname']))
            except:
                realEstate['firstname'].append(str("no value"))


            try:
                realEstate['lastname'].append(str(realEstate_json['contactDetails']['lastname']))
            except:
                realEstate['lastname'].append(str("no value"))

            try:
                realEstate['phoneNumber'].append(str(realEstate_json['contactDetails']['phoneNumber']))
            except:
                realEstate['phoneNumber'].append(str("no value"))

            try:
                realEstate['company'].append(str(realEstate_json['contactDetails']['company']))
            except:
                realEstate['company'].append(str("no value"))

            realEstate['title'].append(str(realEstate_json['title']))

            realEstate['numberOfRooms'].append(str(realEstate_json['numberOfRooms']))
            realEstate['livingSpace'].append(str(realEstate_json['livingSpace']))

            realEstate['plotArea'].append(str(realEstate_json['plotArea']))
            realEstate['builtInKitchen'].append(str(realEstate_json['builtInKitchen']))
            realEstate['price'].append(str(Annoncement_list["resultlist.realEstate"]['price']['value'])+" "+str(Annoncement_list["resultlist.realEstate"]['price']['currency']))
            realEstate['privateOffer'].append(str(realEstate_json['privateOffer']))

            try:
                realEstate['Warm_miete'].append(str(realEstate_json['calculatedPrice']['value'])+" "+str(realEstate_json['calculatedPrice']['currency'])+"/"+str(realEstate_json['calculatedPrice']['priceIntervalType']))
            except:
                realEstate['Warm_miete'].append(None)
            try:
                realEstate['lat'].append(str(realEstate_json['address'][u'wgs84Coordinate']['latitude']))
            except:
                realEstate['lat'].append(str("no value"))

            try:
                realEstate['lon'].append(str(realEstate_json['address'][u'wgs84Coordinate']['longitude']))
            except:
                realEstate['lon'].append(str("no value"))

            realEstate['floorplan'].append(str(realEstate_json['floorplan']))
    return(realEstate)
    
    
    
def scraping_haus_kaufen():
    url = 'https://www.immobilienscout24.de/Suche/de/haus-kaufen?sorting=2'
    response = requests.post(url, headers = {"Cookie": cookies_var})
    json_data = json.loads(response.text)
    pageSize=json_data['searchResponseModel']['resultlist.resultlist']['paging']['pageSize']
    realEstate=defaultdict(list)
    numberOfPages=json_data['searchResponseModel']['resultlist.resultlist']['paging']['numberOfPages']

    path = os.path.join(os.getcwd(), "Data/House/Buy/")
    list_of_files = glob.glob(f"{path}/*.csv") 

    latest_file = max(list_of_files, key=os.path.getmtime)
    df_last=pd.read_csv(latest_file,sep=";",nrows=1,usecols=["creation"])
    last_ads=datetime.strptime(df_last['creation'].tolist()[0][:10]+" "+df_last['creation'].tolist()[0][11:19], '%Y-%m-%d %H:%M:%S')
    
    for i in range(0,int(numberOfPages)):
        url = 'https://www.immobilienscout24.de/Suche/de/haus-kaufen?sorting=2&pagenumber='+str(i+1)
        response = requests.post(url, headers = {"Cookie": cookies_var})
        json_data = json.loads(response.text)

        pageSize=json_data['searchResponseModel']['resultlist.resultlist']['paging']['pageSize']
        for j in range(pageSize):
            Annoncement_list=json_data['searchResponseModel']['resultlist.resultlist']['resultlistEntries'][0]['resultlistEntry'][j]
           
            if(datetime.strptime(Annoncement_list["@creation"][:10]+" "+Annoncement_list["@creation"][11:19], '%Y-%m-%d %H:%M:%S')<last_ads):
                return(realEstate)

            realEstate_json=Annoncement_list["resultlist.realEstate"]
            realEstate['ID'].append(str(realEstate_json[u'@id']))
            realEstate['url'].append(str(u'https://www.immobilienscout24.de/expose/%s' % str(realEstate_json[u'@id'])))
            realEstate["creation"].append(Annoncement_list["@creation"])
            realEstate["Haus/Wohnung"].append("Haus")

            realEstate['address'].append(str(realEstate_json['address']['description']['text']))
            realEstate['city'].append(str(realEstate_json['address']['city']))
            realEstate['postcode'].append(str(realEstate_json['address']['postcode']))
            realEstate['quarter'].append(str(realEstate_json['address']['quarter']))

            try:
                realEstate['firstname'].append(str(realEstate_json['contactDetails']['firstname']))
            except:
                realEstate['firstname'].append(str("no value"))


            try:
                realEstate['lastname'].append(str(realEstate_json['contactDetails']['lastname']))
            except:
                realEstate['lastname'].append(str("no value"))

            try:
                realEstate['phoneNumber'].append(str(realEstate_json['contactDetails']['phoneNumber']))
            except:
                realEstate['phoneNumber'].append(str("no value"))

            try:
                realEstate['company'].append(str(realEstate_json['contactDetails']['company']))
            except:
                realEstate['company'].append(str("no value"))

            realEstate['title'].append(str(realEstate_json['title']))
            realEstate['guestToilet'].append(str(realEstate_json['guestToilet']))

            realEstate['numberOfRooms'].append(str(realEstate_json['numberOfRooms']))
            realEstate['livingSpace'].append(str(realEstate_json['livingSpace']))

            realEstate['plotArea'].append(str(realEstate_json['plotArea']))
            realEstate['price'].append(str(Annoncement_list["resultlist.realEstate"]['price']['value'])+" "+str(Annoncement_list["resultlist.realEstate"]['price']['currency']))
            realEstate['privateOffer'].append(str(realEstate_json['privateOffer']))

            try:
                realEstate['lat'].append(str(realEstate_json['address'][u'wgs84Coordinate']['latitude']))
            except:
                realEstate['lat'].append(str("no value"))

            try:
                realEstate['lon'].append(str(realEstate_json['address'][u'wgs84Coordinate']['longitude']))
            except:
                realEstate['lon'].append(str("no value"))

            realEstate['floorplan'].append(str(realEstate_json['floorplan']))
    return(realEstate)
    
    
    
def scraping_wohnung_kaufen():
    url = 'https://www.immobilienscout24.de/Suche/de/wohnung-kaufen?sorting=2'
    response = requests.post(url, headers = {"Cookie": cookies_var})
    json_data = json.loads(response.text)
    pageSize=json_data['searchResponseModel']['resultlist.resultlist']['paging']['pageSize']
    realEstate=defaultdict(list)

    numberOfPages=json_data['searchResponseModel']['resultlist.resultlist']['paging']['numberOfPages']

    path = os.path.join(os.getcwd(), "Data/Apartment/Buy/")
    list_of_files = glob.glob(f"{path}/*.csv") 
    
    latest_file = max(list_of_files, key=os.path.getmtime)
    df_last=pd.read_csv(latest_file,sep=";",nrows=1,usecols=["creation"])
    last_ads=datetime.strptime(df_last['creation'].tolist()[0][:10]+" "+df_last['creation'].tolist()[0][11:19], '%Y-%m-%d %H:%M:%S')
    
    for i in range(0,int(numberOfPages)):
        url = 'https://www.immobilienscout24.de/Suche/de/wohnung-kaufen?sorting=2&pagenumber='+str(i+1)
        response = requests.post(url, headers = {"Cookie": cookies_var})
        json_data = json.loads(response.text)

        pageSize=json_data['searchResponseModel']['resultlist.resultlist']['paging']['pageSize']
        for j in range(pageSize):
            Annoncement_list=json_data['searchResponseModel']['resultlist.resultlist']['resultlistEntries'][0]['resultlistEntry'][j]

           
            if(datetime.strptime(Annoncement_list["@creation"][:10]+" "+Annoncement_list["@creation"][11:19], '%Y-%m-%d %H:%M:%S')<last_ads):
                return(realEstate)
                
            realEstate_json=Annoncement_list["resultlist.realEstate"]
            realEstate['ID'].append(str(realEstate_json[u'@id']))
            realEstate['url'].append(str(u'https://www.immobilienscout24.de/expose/%s' % str(realEstate_json[u'@id'])))
            realEstate["creation"].append(Annoncement_list["@creation"])
            realEstate["Haus/Wohnung"].append("Wohnung")

            realEstate['address'].append(str(realEstate_json['address']['description']['text']))
            realEstate['city'].append(str(realEstate_json['address']['city']))
            realEstate['postcode'].append(str(realEstate_json['address']['postcode']))
            realEstate['quarter'].append(str(realEstate_json['address']['quarter']))


            try:
                realEstate['firstname'].append(str(realEstate_json['contactDetails']['firstname']))
            except:
                realEstate['firstname'].append(str("no value"))


            try:
                realEstate['lastname'].append(str(realEstate_json['contactDetails']['lastname']))
            except:
                realEstate['lastname'].append(str("no value"))

            try:
                realEstate['phoneNumber'].append(str(realEstate_json['contactDetails']['phoneNumber']))
            except:
                realEstate['phoneNumber'].append(str("no value"))

            try:
                realEstate['company'].append(str(realEstate_json['contactDetails']['company']))
            except:
                realEstate['company'].append(str("no value"))

            realEstate['title'].append(str(realEstate_json['title']))

            realEstate['numberOfRooms'].append(str(realEstate_json['numberOfRooms']))
            realEstate['livingSpace'].append(str(realEstate_json['livingSpace']))

            realEstate['balcony'].append(str(realEstate_json['balcony']))
            realEstate['builtInKitchen'].append(str(realEstate_json['builtInKitchen']))
            realEstate['garden'].append(str(realEstate_json['garden']))
            realEstate['price'].append(str(Annoncement_list["resultlist.realEstate"]['price']['value'])+" "+str(Annoncement_list["resultlist.realEstate"]['price']['currency']))
            realEstate['privateOffer'].append(str(realEstate_json['privateOffer']))

            realEstate['floorplan'].append(str(realEstate_json['floorplan']))
            realEstate['guestToilet'].append(str(realEstate_json['guestToilet']))

            try:
                realEstate['lat'].append(str(realEstate_json['address'][u'wgs84Coordinate']['latitude']))
            except:
                realEstate['lat'].append(str("no value"))

            try:
                realEstate['lon'].append(str(realEstate_json['address'][u'wgs84Coordinate']['longitude']))
            except:
                realEstate['lon'].append(str("no value"))
    return(realEstate)
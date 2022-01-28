import Extract_Transform
from datetime import datetime
import pandas as pd
import pymongo
import json

import csv
def load(new_ads):
    new_ads=Extract_Transform.Extract_and_Transform()
    now = datetime.now()
    new_file_date=now.strftime("%Y-%m-%d")
    
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["immoscout24"]
      
    df= pd.DataFrame.from_dict(new_ads[0])
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    mycol = mydb["Wohnung-Miete"]
    x = mycol.insert_many(parsed)
    df.to_csv("Data/Apartment/Rent/Wohnung-Miete_"+str(new_file_date)+".csv",sep=';',index=False)
    
    
    
    df= pd.DataFrame.from_dict(new_ads[1])
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    mycol = mydb["Haus-Miete"]
    x = mycol.insert_many(parsed)
    df.to_csv("Data/House/Rent/Haus-Miete_"+str(new_file_date)+".csv",sep=';',index=False)
    
    
    
    
    df= pd.DataFrame.from_dict(new_ads[2])
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    mycol = mydb["Wohnung-kaufen"]
    x = mycol.insert_many(parsed)
    df.to_csv("Data/Apartment/Buy/Wohnung-kaufen_"+str(new_file_date)+".csv",sep=';',index=False)
    
    
    
    df= pd.DataFrame.from_dict(new_ads[3])
    result = df.to_json(orient="records")
    parsed = json.loads(result)
    mycol = mydb["Haus-kaufen"]
    x = mycol.insert_many(parsed)
    df.to_csv("Data/House/Buy/Haus-kaufen_"+str(new_file_date)+".csv",sep=';',index=False)

               
if __name__ == '__main__':
    load(new_ads)

import Extract_Transform
from datetime import datetime
import pandas as pd

from elasticsearch import helpers, Elasticsearch
import csv
def load(new_ads):
    new_ads=Extract_Transform.Extract_and_Transform()
    now = datetime.now()
    new_file_date=now.strftime("%Y-%m-%d")
    
    df= pd.DataFrame.from_dict(new_ads[0])
    df.to_csv("Data/Apartment/Rent/Wohnung-Miete_"+str(new_file_date)+".csv",sep=';',index=False)
    
    df= pd.DataFrame.from_dict(new_ads[1])
    df.to_csv("Data/House/Rent/Haus-Miete_"+str(new_file_date)+".csv",sep=';',index=False)
    
    df= pd.DataFrame.from_dict(new_ads[2])
    df.to_csv("Data/Apartment/Buy/Wohnung-kaufen_"+str(new_file_date)+".csv",sep=';',index=False)
    
    df= pd.DataFrame.from_dict(new_ads[3])
    df.to_csv("Data/House/Buy/Haus-kaufen_"+str(new_file_date)+".csv",sep=';',index=False)
    
    
    es = Elasticsearch()
    
    for i in new_ads:
        helpers.bulk(es, i, index='immoscout-index', doc_type='immoscout_docs')
        
if __name__ == '__main__':
    load(new_ads)
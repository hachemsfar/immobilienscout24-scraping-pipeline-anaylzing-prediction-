# immobilienscout24 Scraping:
The goal of this project is to extract data from immobilienscout24 website.
These are the pipeline steps:
- **Extract_Transform.py**: extracting all usefull information about every post (appartment/houses and for both buying/renting) and save them in a dictionnary
The script will extract from all posts since the last post that was extracted.
- **Load.py** converting the dictionary into csv file and inserting it into the mongodb database
- **Pipeline.py** airflow pipeline: the script will run automatically once a day.
----
- **Web scraping notebook** https://www.kaggle.com/hachemsfar/immoscout-scraper / immoscout-scraper.ipynb
- **Analyzing scraped data** immoscout-Analyse.ipynb
- **Creating models to predict the price of the appartment or house (depend on many features like the postcode, living area, number of rooms...)** immoscout-Prediction (Berlin).ipynb/immoscout-Prediction (all germany cities).ipynb


![plot](https://github.com/hachemsfar/immobilienscout24-scraping-pipeline-anaylzing-prediction-/blob/main/mongodb%20database.JPG)


**Keywords:** Data engineer/Data science ; Machine Learning ; Web scraping; Data Visualization ; Python ; Airflow ; Mongodb ; matplotlib ; linear regression ; CSV format 

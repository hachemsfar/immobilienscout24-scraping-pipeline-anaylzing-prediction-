from utilities import scraping_wohnung_mieten,scraping_haus_mieten, scraping_haus_kaufen,scraping_wohnung_kaufen

def Extract_and_Transform():
    appartment_rent=scraping_wohnung_mieten()
    house_rent=scraping_haus_mieten()
    
    appartment_buy=scraping_wohnung_kaufen()
    house_buy=scraping_haus_kaufen()
    
    return([appartment_rent,house_rent,appartment_buy,house_buy])
if __name__ == '__main__':
    Extract_and_Transform()
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import csv


class Olx(scrapy.Spider):
    name = 'olx'

    url = 'https://www.olx.in/api/relevance/v4/search?category=1453&facet_limit=100&lang=en-IN&location=1000001&location_facet_limit=20&platform=web-desktop&relaxedFilters=true&user=18b2cf1f41ex2c0be382'

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }

    def __init__(self):
        with open('results.csv','w') as csv_file:
            csv_file.write('title,price,description,date,location\n')

    def start_requests(self):
        for page in range(0,5):
            yield scrapy.Request(url=self.url + '&page=' + str(page), headers = self.headers, callback=self.parse)



    def parse(self,response):
        data=response.text
        data = json.loads(data)         
        for offer in data['data']:
            items = {
                'title': offer['title'],
                'price': offer['price']['value']['display'],
                'description': offer['description'].replace("\n"," "),
                'date': offer['display_date'],
                'location': offer['locations_resolved']['SUBLOCALITY_LEVEL_1_name'] + ', ' +
                offer['locations_resolved']['ADMIN_LEVEL_3_name'] + ', ' +
                 offer['locations_resolved']['ADMIN_LEVEL_1_name'] + ', ' +
                offer['locations_resolved']['COUNTRY_name'] 
                

            }
            print(json.dumps(items,indent=2))
            with open('results.csv','a') as csv_file:
                writer = csv.DictWriter(csv_file,fieldnames=items.keys())
                writer.writerow(items)






#run scraper
process = CrawlerProcess()
process.crawl(Olx)
process.start()


#debug
# Olx.parse(Olx,'')
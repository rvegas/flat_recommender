from google.cloud import storage
from scrapy.crawler import CrawlerProcess
from datetime import datetime

import scrapy
import json
import tempfile
import googlemaps

TEMPORARY_FILE = tempfile.NamedTemporaryFile(delete=False, mode='w+t')
APIKEY = 'ENTERAPIKEYHERE'
gmaps = googlemaps.Client(key=APIKEY)

def upload_file_to_bucket(bucket_name, blob_file, destination_file_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_file_name)
    blob_source = bucket.blob('_source_' + destination_file_name)

    blob.upload_from_filename(blob_file.name, content_type='text/csv')
    blob_source.upload_from_filename(blob_file.name, content_type='text/csv')

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    # Podeis cambiar la url inicial por otra u otras paginas
    start_urls = ['https://www.yelp.es/madrid']

    def parse(self, response):
        # Aqui scrapeamos los datos y los imprimimos a un fichero
        title = response.css('title ::text').extract_first()
        if 'fotos' in title:
            parts = title.split(" - ")
            name = parts[0]
            fotos_y_resenas = parts[1]
            clase = parts[2]
            direccion = parts[3]
            fotos = fotos_y_resenas.split(" ")[0]
            resenas = 0
            if len(fotos_y_resenas.split(" ")) > 3:
                resenas = fotos_y_resenas.split(" ")[3]
            #print(f'"{name}","{clase}","{direccion}",{fotos},{resenas}')
            lat = 0
            lon = 0
            city = 'Madrid'
            if direccion != "":
                geocode_result = gmaps.geocode(direccion)
                if geocode_result and len(geocode_result) > 0:
                    lat = geocode_result[0]['geometry']['location']['lat']
                    lon = geocode_result[0]['geometry']['location']['lng']
            
            TEMPORARY_FILE.writelines(f'{name};{clase};{direccion};{city};{fotos};{resenas};{lat};{lon}\n')

        # Aqui hacemos crawling (con el follow)
        for next_page in response.css('div.recent-collections a.collection-card-container'):
            yield response.follow(next_page, self.parse)
        for next_page in response.css('div.collection-items ul.ylist div.photo-box a'):
            yield response.follow(next_page, self.parse)

process = CrawlerProcess({
    'USER_AGENT': 'RICARDO VEGAS CRAWLER ricardovegas@gmail.com'
})
process.crawl(BlogSpider)

def activate(request):
    now = datetime.now() 
    TEMPORARY_FILE.seek(0)
    request_json = request.get_json()
    BUCKET_NAME = 'bda5-keepcoding-ricardo1'
    DESTINATION_FILE_NAME = 'input/yelp/crawl.csv'
    process.start()
    
    TEMPORARY_FILE.seek(0)
    upload_file_to_bucket(BUCKET_NAME, TEMPORARY_FILE, DESTINATION_FILE_NAME)
    
    return "Success!"

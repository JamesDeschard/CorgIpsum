import itertools

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from main.models import ScrapedImageUrl

LENGTH_OF_URL_LIST = 42

class GetCorgis:

    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            } 

    def parse(self):
        data = requests.get(self.url, headers=self.headers)
        return BeautifulSoup(data.text, "html.parser")
    
    def get_image_links(self):
        data = self.parse()
        links = data.find_all('source')
        return links
    
    def clean_links(self):
        clean_links = []
        links = self.get_image_links()
        for i in range(len(links)):
            clean_link = links[i].__repr__().split(' ')[1][8:-3]
            clean_link = clean_link.replace('amp;', '')
            clean_links.append(clean_link)
        return clean_links
  

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not ScrapedImageUrl.objects.first():
            all_picture_urls = list()
            base_url = 'https://www.gettyimages.fr/photos/corgi-gallois?assettype=image&numberofpeople=none&phrase=corgi%20gallois&sort=mostpopular&license=rf%2Crm&page='

            for i in range(LENGTH_OF_URL_LIST):
                all_picture_urls.append(GetCorgis(f'{base_url}{i}').clean_links())
                
            save_corgi_list = ScrapedImageUrl( 
                                  title='Corgi Image List of Urls', 
                                  data=list(itertools.chain.from_iterable(all_picture_urls))
                                  )

            save_corgi_list.save()
            self.stdout.write(self.style.SUCCESS('Corgi Urls where successfully loaded to the database..!'))

        else:
            self.stdout.write(self.style.SUCCESS('List of urls is already completed!'))

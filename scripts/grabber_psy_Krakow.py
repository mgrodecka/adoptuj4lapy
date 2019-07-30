from bs4 import BeautifulSoup
import requests
from adoptuj.models import Animal

def run():
    class grabberKrakow:
        BASE_URL = 'http://www.schronisko.krakow.pl/'

        def __init__(self,root_file):
            self.root_file = root_file
            self.links = []

        def get_links(self):
            resp = requests.get(self.BASE_URL + self.root_file)
            soup = BeautifulSoup(resp.text,'html.parser')
            link_nodes = soup.select('a.news_short_more')
            linki = [ a['href'] for a in link_nodes]
            return linki

        def get_data_from_link(self,links):
            data = []
            for link in links:
                new_animal = Animal()
                new_animal.type = 1
                new_animal.status = 1
                new_animal.city = "Kraków"
                new_animal.shelter = "Krakowskie Towarzystwo Opieki Nad Zwierzętami"
                new_animal.shelter_group = 2
                record = {
                    'name': None,
                    'sex': None,
                    'age': None,
                    'color': None,
                    'description': None,
                    'vaccination': None,
                    'debug': None,
                    'ster': None,
                    'city': None,
                    'address': None,
                    'type': None,
                    'name': None,
                    'shelter': None,
                    'shelter_group': None,
                    'image': None,
                    'phone': None,
                    'mail': None,
                    'virtual_adoption': None,
                    'status': None
                }
                url = self.BASE_URL + link
                resp = requests.get(url)
                soup = BeautifulSoup(resp.text,'html.parser')
                new_animal.link = url

                # Imię
                try:
                    record['name'] = soup.select('div.default_description > p')[0].getText().strip()
                    name = record['name']
                    new_animal.name = name
                except Exception as e:
                    print('Błąd z ustalaniem imienia!',e)

                #Inne - BRAK
                new_animal.sex = 3
                new_animal.age_years = 0

                #opis
                try:
                    full_text = soup.select('div.default_description')[0]
                    opis = full_text.select('p')
                    opis = opis[6].getText().strip()
                    #text = "\n".join([node.getText() for node in opis])
                    #text = opis.strip()
                    new_animal.description = opis
                    #print(text[:30])
                except Exception as e:
                    print('Błąd z ustalaniem opisu!' + record['name'] ,e)

                #foto
                try:
                    img_url = soup.select('#photo0')[0]['href']
                    image_url = 'http://www.schronisko.krakow.pl' + img_url
                    new_animal.image = image_url
                    img_data = requests.get(image_url).content
                    record['img'] = img_data
                    name_filename = record['name'].replace(" ", "_")
                    name_filename = name_filename.replace("/", "_")
                    filename = "dog" + "_" + name + "_krakow"
                    new_animal.identifier = filename
                    #f = open('psy/'+filename,'wb')
                    #f.write(img_data)
                    #f.close()
                except Exception as e:
                    print('Błąd z pobraniem zdjecia!' + record['name'] ,e)
                data.append(record)
                new_animal.save()
            return data

    for page in range(11,20):
        grabberPsy= grabberKrakow('Adopcje/ZWIERZAKI_DO_ADOPCJI/Psy/?p={}'.format(page-1))
        links = grabberPsy.get_links()
        doggos = grabberPsy.get_data_from_link(links)

from bs4 import BeautifulSoup
import requests
from adoptuj.models import Animal

def run():
    class grabberCiapkowo:
        BASE_URL = 'http://www.ciapkowo.pl/'
        def __init__(self,root_file):
            self.root_file = root_file
            self.links = []

        def get_links(self):
            url = self.BASE_URL + self.root_file
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text,'html.parser')
            link_nodes = soup.select('h1.entry-title > a')
            linki = [ a['href'] for a in link_nodes]
            return linki

        def get_data_from_link(self,links):
            data = []
            for link in links:
                new_animal = Animal()
                new_animal.type = 2
                new_animal.status = 1
                new_animal.city = "Gdynia"
                new_animal.shelter = "Schronisko Ciapkowo w Gdyni"
                new_animal.shelter_group = 4
                new_animal.sex = 1
                new_animal.age_years = 0
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
                url = link
                resp = requests.get(url)
                soup = BeautifulSoup(resp.text,'html.parser')
                new_animal.link = url

                # Imię
                try:
                    record['name'] = soup.select('h1.entry-title')[0].getText().strip()
                    name = record['name']
                    new_animal.name = name
                except Exception as e:
                    print('Błąd z ustalaniem imienia!',e)

                #Opis:
                try:
                    try:
                        full_text = soup.select('div.entry-content')[0]
                        opis = full_text.select('p')
                        opis = opis[1:]
                        text = "\n".join([node.getText() for node in opis])
                        text = text.strip()
                        text = text[:text.lower().find(' #niekupujadoptuj')]
                    except Exception: pass
                    try:
                        full_text = soup.select('div.entry-content')[0]
                        opis = full_text.select('div.text_exposed')
                        opis = opis[1:]
                        text = "\n".join([node.getText() for node in opis])
                        text = text.strip()
                    except Exception: pass
                    new_animal.description = text
                except Exception: print('Błąd z pobraniem opisu!' + record['name'])

                #Inne - wiek, kastracja
                try:
                    full_text = soup.select('div.entry-content')[0]
                    base_info = full_text.select('div.text_exposed')
                    base_info = base_info[0]#.getText().strip()

                except Exception: pass
                try:
                    full_text = soup.select('div.entry-content')[0]
                    base_info = full_text.select('p')
                    base_info = base_info[0]#.getText().strip()
                except Exception: pass


                #foto
                try:
                    imgs = [node['href'] for node in soup.select('div.ngg-galleryoverview div.ngg-gallery-thumbnail-box div.ngg-gallery-thumbnail a')]
                    image_url = imgs[0]
                    new_animal.image = image_url
                    img_data = requests.get(image_url).content
                    record['img'] = img_data
                    name_filename = record['name'].replace(" ", "_")
                    name_filename = name_filename.replace("/", "_")
                    filename = "cat" + "_" + name + "_ciapkowo"
                    new_animal.identifier = filename
                    #f = open('koty/'+filename,'wb')
                    #f.write(img_data)
                    #f.close()
                except Exception as e:
                    print('Błąd z pobraniem zdjecia!' + record['name'] ,e)
                data.append(record)
                new_animal.save()
            return data

    for page in range(1,3):
        grabberKoty = grabberCiapkowo('kategoria/koty_do_adopcji/kocury/page/{}'.format(page))
        links = grabberKoty.get_links()
        koty = grabberKoty.get_data_from_link(links)

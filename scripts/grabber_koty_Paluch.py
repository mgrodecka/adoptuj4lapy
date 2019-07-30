from bs4 import BeautifulSoup
import requests
from adoptuj.models import Animal

def run():
    class grabberPaluch:
        BASE_URL = 'http://www.napaluchu.waw.pl/'

        def __init__(self,root_file):
            self.root_file = root_file
            self.links = []

        #pobranie linków do podstron zwierząt z listy wszytskich zwierzat
        def get_links(self):
            resp = requests.get(self.BASE_URL + self.root_file)
            soup = BeautifulSoup(resp.text,'html.parser')
            link_nodes = soup.select('.thumb > a')
            linki = [ a['href'] for a in link_nodes]
            return linki

        #pobranie danych ze strony każdego zwierzecia
        def get_data_from_link(self,links):
            data = []
            for link in links:
                new_animal = Animal()
                new_animal.type = 2
                new_animal.status = 1
                new_animal.city = "Warszawa"
                new_animal.shelter = "Schronisko Na Paluchu"
                new_animal.shelter_group = 1
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
                    record['name'] = soup.select('h5')[0].getText().strip()
                    name = record['name']
                    #name.encode('windows-1250').decode('utf-8')  <- NIE DZIAŁA
                    new_animal.name = name
                    print(name)
                except Exception as e:
                    print('Błąd z ustalaniem imienia!',e)

                # Opis
                try:
                    try: full_text = soup.select('div.main_content div.description')[0].getText().strip()
                    except Exception: full_text = ''
                    record['description'] = full_text
                    new_animal.description = full_text
                except Exception as e:
                    print('Błąd z ustalaniem opisu!' + record['name'] ,e)

                # Inne dane - płeć, wiek, rasa
                for field in soup.select('div.info span'):
                    try:
                        text = field.getText()
                        (k,v) = text.strip().split(':',2)
                        k = k.lower().strip()
                        v = v.strip()
                        if k == 'påeä':
                            v = v.lower().strip()
                            if v == 'samiec': record['sex'] = 1
                            else: record['sex'] = 2
                            new_animal.sex = record['sex']

                        elif k == 'wiek':
                            v = (v.lower().strip().split(' '))
                            if (v[1] == "rok") or (v[1] == "lat") or (v[1] == "lata"):
                                v = int(v[0])
                            else:
                                v = 1
                            record['age'] = v
                            new_animal.age = v
                            new_animal.age_years = v

                        elif k == 'rasa':
                            record['type'] = v
                            new_animal.breed = v
                    except Exception as e:
                        pass
                        
                #foto
                try:
                    imgs = []
                    try: imgs += [ node['src'] for node in soup.select('div#main_image_cont > a > img.main_img_one')][:1]
                    except Exception: pass

                    try: imgs += [ node['href'] for node in soup.select('div#main_image_cont > a')][:1]
                    except Exception: pass

                    try: imgs += [ node['href'] for node in soup.select('div.ani_images > div.ani_image_bottom > a')]
                    except Exception: pass

                    if len(imgs)>1: imgs = imgs[1:] # pierwsze to zwykle miniatura

                    imgs = [ i if i.startswith('http') else 'http://napaluchu.waw.pl/{}'.format(i) for i in imgs ]

                    img_url = imgs[0]
                    new_animal.image = img_url
                    img_data = requests.get(img_url).content
                    record['img'] = img_data
                    name_filename = record['name'].replace(" ", "_")
                    name_filename = name_filename.replace("/", "_")
                    filename = "cat" + "_" + name_filename + "_paluch"
                    new_animal.identifier = filename
                    #f = open('psy/'+filename,'wb')
                    #f.write(img_data)
                    #f.close()
                except Exception as e:
                    print('Błąd z pobraniem zdjecia!' + record['name'] ,e)
                data.append(record)
                new_animal.save()
            return data

    for page in range(1,10):
        grabberKoty = grabberPaluch('czekam_na_ciebie:{}/?sea=1&f[species_id]=2'.format(page))
        links = grabberKoty.get_links()
        koty = grabberKoty.get_data_from_link(links)

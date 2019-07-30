from bs4 import BeautifulSoup
import requests
from adoptuj.models import Animal

def run():
    class grabberMilanowek:
        BASE_URL = 'http://www.schroniskomilanowek.pl/'

        def __init__(self,root_file):
            self.root_file = root_file
            self.links = []

        #pobranie linków do podstron zwierząt z listy wszytskich zwierzat
        def get_links(self):
            resp = requests.get(self.BASE_URL + self.root_file)
            soup = BeautifulSoup(resp.text,'html.parser')
            link_nodes = soup.select('.spEntriesListCell > .spEntriesListTitle > a')
            linki = [ a['href'] for a in link_nodes]
            return linki

        #pobranie danych ze strony każdego zwierzecia
        def get_data_from_link(self,links):
            data = []
            for link in links:
                new_animal = Animal()
                new_animal.type = 2
                new_animal.status = 1
                record = {
                    'name': None,
                    'sex': None,
                    'age': None,
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
                    'mail': None
                }
                url = self.BASE_URL + link
                resp = requests.get(url)
                soup = BeautifulSoup(resp.text,'html.parser')
                new_animal.link = url

                # Imię
                try:
                    record['name'] = soup.select('h1.SPTitle')[0].getText().strip()
                    name = record['name']
                    new_animal.name = name
                except Exception as e:
                    print('Błąd z ustalaniem imienia!',e)

                # Opis
                try:
                    full_text = soup.select('.SPDetails')[0].getText().strip()
                    full_text = full_text[full_text.lower().find('opis:')+5:]
                    desc = full_text[:full_text.lower().find('kontakt:')]
                    desc = desc.strip()
                    record['description'] = desc
                    new_animal.description = desc
                except Exception as e:
                    print('Błąd z ustalaniem opisu!',e)

                # Kontakt - nieudane :(
                try:
                    full_text = soup.select('.SPDetails')[0].getText().strip()
                    full_text = full_text[full_text.lower().find('kontakt:')+8:]
                except Exception as e:
                    print('Błąd z ustalaniem kontaktu!',e)

                # Inne dane - płeć, wiek, rasa, miasto, sterylizacja, odrobaczenie, szczepienia
                for field in soup.select('div.spField'):
                    try:
                        text = field.getText()
                        (k,v) = text.strip().split(':',2)
                        k = k.lower().strip()
                        v = v.strip()
                        if k == 'płeć':
                            v = v.lower().strip()
                            if v == 'kot': record['sex'] = 1
                            else: record['sex'] = 2
                            new_animal.sex = record['sex']
                        elif k == 'wiek':
                            v = int(v.lower().strip().split(' ')[0])
                            record['age'] = v
                            new_animal.age = v
                            new_animal.age_years = v
                        elif k == 'rasa':
                            record['type'] = v
                            new_animal.breed = v
                        elif k == 'miasto':
                            record['city'] = v
                            new_animal.city = v
                            new_animal.shelter = "Schronisko w Milanówku"
                            new_animal.shelter_group = 1
                        elif k == 'sterylizacja':
                            record['ster'] = (v.lower() == 'tak')
                            new_animal.sterilization = record['ster']
                        elif k == 'szczepienie p. wściekliźnie':
                            record['vaccination'] = (v.lower() == 'tak')
                            new_animal.vaccination = record['vaccination']
                        elif k == 'odrobaczenie':
                            record['debug'] = (v.lower() == 'tak')
                            new_animal.deworming = record['debug']
                    except Exception as e:
                        pass

                #Zdjęcie
                try:
                    img_url = soup.select('div.spField > img.spFieldsData.field_photo1')[0]['src']
                    new_animal.image = img_url
                    img_data = requests.get(img_url).content
                    record['image'] = img_data
                    name_filename = record['name'].replace(" ", "_")
                    filename = "cat" + "_" + name_filename + "_milanowek"
                    new_animal.identifier = filename
                    #f = open('static/koty/'+filename,'wb')
                    #f.write(img_data)
                    #f.close()
                except Exception as e:
                    print('Błąd z pobraniem zdjecia!',e)
                data.append(record)
                new_animal.save()
            return data

    grabberKoty = grabberMilanowek('index.php?option=com_sobipro&sid=56&Itemid=12')
    links = grabberKoty.get_links()
    koty = grabberKoty.get_data_from_link(links)

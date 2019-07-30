from django.shortcuts import render, redirect, get_object_or_404
from adoptuj.forms import ContactForm
from django.views import View
from .models import Animal, SEX, TYPES
from django.core import mail
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


#wyświetlenie strony głównej
class ShowMainPage(View):
    def get(self, request):
        return render(request, "main.html")

#wysyłanie maila na podstawie formularza kontaktowego
class SendEmail(View):
    def get(self, request):
        form = ContactForm()
        return render(request, "kontakt.html", {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['imie']
            subject = form.cleaned_data['temat']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['wiadomosc']
            phone = form.cleaned_data['telefon']
            #przekazanie do tematu maila - adresu adresata i tematu
            subject = "adoptuj4lapy " + subject + " " + from_email
            #dodanie do treści maila numeru telefonu adresata
            message += " " + phone
            try:
                connection = mail.get_connection()
                # Manually open the connection
                connection.open()
                # Construct an email message that uses the connection
                email1 = mail.EmailMessage(subject, message, from_email, ['mgrodecka4@gmail.com'],
                    connection=connection,)
                # Send the email
                email1.send()
                connection.close()
            except Exception as e:
                print(e)
            return redirect('/') #przeniesienie na stronę główną
        return render(request, "kontakt.html", {'form': form})


#wyświetla zaadoptowane zwierzaki na podstawie wartości pola "status"
class ShowAdopted(View):
    def get(self, request):
        adopted = Animal.objects.filter(status=2)
        return render(request, "adoptowane.html", {"adopted": adopted})

#wyświetlenie listy schronisk
#schroniska dodawane są ręcznie w HTML
#  <- TO DO zaciąganie schronisk z tabeli z info o schroniskach
class ShowShelters(View):
    def get(self, request):
        return render(request, "lista_schronisk.html")

#wyświetlanie strony pojedynczego zwierzaka
class ShowOneAnimal(View):
    def get(self, request, animal_id): #, animal_id
        one_animal = get_object_or_404(Animal, identifier=animal_id)
        ctx = {"one_animal": one_animal, "gender": SEX[(one_animal.sex)-1][1],
         "type":TYPES[(one_animal.type)-1][1]}
        return render(request, "one_animal.html", ctx)

#wyświetlenie strony wyszukiwarki
class ShowAnimals(View):
    #funkcja pozwalająca na poprawne wyświetlenie płci
    def __helper(self,x):
        x.sex = SEX[x.sex - 1][1]
        return x


    #wyświetlenie formularza wyszukiwarki i wszystkich zwierząt do adopcji
    def get(self, request):
        animals = Animal.objects.filter(status=1).order_by('type')

        #paginacja - wyświelanie max 15 zwierzat na 1 stronie
        page = request.GET.get('page', 1)
        paginator = Paginator(animals, 15)
        try:
            page_animals = paginator.page(page)
        except PageNotAnInteger:
            page_animals = paginator.page(1)
        except EmptyPage:
            page_animals = paginator.page(paginator.num_pages)

        return render(request, "all_animals.html", {"page_animals": page_animals}) #[self.__helper(a) for a in page_animals]
                                                                                #zastosowanie powyższego rozwaliłp paginację

    #wyświetlenie wyników wyszukiwania
    def post(self, request):
        #tworzenie grupy filtrów
        filters = {}
        filters['status'] = 1
        city = request.POST.get("city")
        if city != '0':
            filters['shelter_group'] = city
        type = request.POST.get("pet_type")
        if type != '3':
            filters['type'] = type
        sex = request.POST.get("pet_sex")
        if sex != '3':
            filters['sex'] = sex
        age_start = request.POST.get("pet_age_start")
        if age_start != "":
            filters['age_years__gte'] = age_start
        age_end = request.POST.get("pet_age_end")
        if age_end != "":
            filters['age_years__lte'] = age_end
        page_animals = Animal.objects.filter(**filters)

        #paginacja
        page = request.GET.get('page', 1)
        paginator = Paginator(page_animals, 15)
        try:
            page_animals = paginator.page(page)
        except PageNotAnInteger:
            page_animals = paginator.page(1)
        except EmptyPage:
            page_animals = paginator.page(paginator.num_pages)

        return render(request, "all_animals.html", {"page_animals":page_animals })

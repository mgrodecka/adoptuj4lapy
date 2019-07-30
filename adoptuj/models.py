from django.db import models


#status zwierzęcia - pole status
STATUSES = (
    (1, "czeka na adopcje"),
    (2, "zaadoptowany"),
    (3, "za tęczowym mostem"),
)
# określenie grupy schronisk - pole shelter_group
SHELTERS = (
    (1, "Warszawa"),
    (2, "Kraków"),
    (3, "Wrocław"),
    (4, "Trójmiasto"),
    (5, "Poznań"),
    (6, "Łódź"),
    (7, "Katowice"),
    (8, "Lublin"),
    (0, "all"),
)
#określenie gatunku - pole type
TYPES = (
    (1, "dog"),
    (2, "cat"),
    (3, "both"),
)
#określenie płci - pole sex
SEX = (
    (1, "M"),
    (2, "F"),
    (3, "both"),
)

#model po zapisu danych na temat pobieranych zwierząt
class Animal(models.Model):
    identifier = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    type = models.IntegerField(choices=TYPES)
    breed = models.CharField(max_length=64)
    sex = models.IntegerField(choices=SEX)
    age = models.CharField(max_length=64, default=0)
    age_years = models.IntegerField(default=0)
    color = models.CharField(max_length=64)
    description = models.TextField()
    vaccination = models.BooleanField(default=False)
    deworming = models.BooleanField(default=False)
    sterilization = models.BooleanField(default=False)
    city = models.CharField(max_length=64)
    shelter = models.CharField(max_length=64)
    shelter_group = models.IntegerField(choices=SHELTERS)
    address = models.CharField(max_length=128)
    phone = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    link = models.CharField(max_length=256)
    image = models.CharField(max_length=256)
    virtual_adoption = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUSES)
    trained = models.BooleanField(default=False)
    accept_dogs = models.BooleanField(default=False)
    accept_cats = models.BooleanField(default=False)
    accept_children = models.BooleanField(default=False)
    added_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

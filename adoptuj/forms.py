from django import forms


#formularz kontaktowy - przekazuje dane do wysłania maila
class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    imie = forms.CharField(required=True)
    temat = forms.CharField(required=True)
    wiadomosc = forms.CharField(widget=forms.Textarea)
    telefon = forms.CharField(required=False)

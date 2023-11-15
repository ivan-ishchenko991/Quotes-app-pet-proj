from django.forms import ModelForm, CharField, TextInput, Textarea

from .models import Tag, Authors, Quotes


class AuthorForm(ModelForm):
    fullname = CharField(widget=TextInput(attrs={"class": "form-control"}))
    date_born = CharField(widget=TextInput(attrs={"class": "form-control"}))
    location_born = CharField(widget=TextInput(attrs={"class": "form-control"}))
    bio = CharField(widget=Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Authors
        fields = ['fullname', 'date_born', 'location_born', 'bio']


class QuoteForm(ModelForm):
    quote = CharField(widget=Textarea(attrs={"class": "form-control"}))

    class Meta:
        model = Quotes
        fields = ['quote']


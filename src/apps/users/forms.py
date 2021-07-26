from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, label=_("Username"))
    password = forms.CharField(widget=forms.PasswordInput, label=_('Password'), validators=[validate_password])

    remember_me = forms.BooleanField(required=False, initial=False, label=_("Remember me"))

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data['username']
        password = cleaned_data['password']

        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError(_("User not found."))

        self.cleaned_data['user'] = user


# form  = LoginForm(initial={'username': 'karabas'})

# class CarForm(forms.Form):
#     car_id = forms.IntegerField(label='Car', validators=[])
#     # car = forms.ModelChoiceField(queryset=Car.objects.filter(is_deleted=False))
#
#     def __init__(self, car_instance: Car, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._car = car_instance

# try:
#     Car.objects.get(id=42)
# except Car.ObjectDoesNotExist:
#     pass

class Article:
    def __init__(self, pages=None):
        self.pages = pages or []

        self.pages = [
            "asfas fasfasfas",
            "asfa sfasfa sfa s",
        ]
        self._count_pages = None

    def update_pages(self, pages):
        self.pages = pages or []
        self._count_pages = None

    @property
    def count_words(self):
        if self._count_pages is not None:
            self._count_pages = sum(
                page_count for page_count in (len(page.split(' ')) for page in self.pages)
            )
        return self._count_pages

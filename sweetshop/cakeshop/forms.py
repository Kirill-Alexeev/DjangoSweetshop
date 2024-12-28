from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Review
from datetime import date


class CheckoutForm(forms.Form):
    delivery_address = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "checkout__input",
                "placeholder": "Введите ваш адрес",
            }
        ),
        label="Адрес доставки",
    )
    execution_date = forms.DateField(
        required=True,
        widget=forms.DateInput(
            attrs={
                "class": "checkout__input",
                "type": "date",
            }
        ),
        label="Дата доставки",
    )

    def clean_execution_date(self):
        execution_date = self.cleaned_data.get("execution_date")
        if execution_date < date.today():
            raise forms.ValidationError("Дата доставки не может быть в прошлом.")
        return execution_date


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["review"]
        widgets = {
            "review": forms.Textarea(attrs={"class": "reviews__textarea", "rows": 4}),
        }
        labels = {
            "review": "Ваш отзыв",
        }

    def clean_review(self):
        review = self.cleaned_data.get("review")

        if not review.strip():
            raise forms.ValidationError("Отзыв не может быть пустым.")

        if len(review) < 10:
            raise forms.ValidationError("Отзыв слишком короткий. Минимум 10 символов.")
        if len(review) > 1000:
            raise forms.ValidationError("Отзыв слишком длинный. Максимум 500 символов.")

        return review


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={"class": "table__input"})
    )
    first_name = forms.CharField(
        label="Имя", widget=forms.TextInput(attrs={"class": "table__input"})
    )
    last_name = forms.CharField(
        label="Фамилия", widget=forms.TextInput(attrs={"class": "table__input"})
    )
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "table__input"})
    )
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "table__input"})
    )
    password2 = forms.CharField(
        label="Повтор пароля",
        widget=forms.PasswordInput(attrs={"class": "table__input"}),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if len(password) < 8:
            raise forms.ValidationError("Пароль должен быть не менее 8 символов.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну цифру.")
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("Пароль должен содержать хотя бы одну букву.")
        return password

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот Email уже зарегистрирован.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Пароли не совпадают.")
        return cleaned_data

from django import forms
from .models import Review


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

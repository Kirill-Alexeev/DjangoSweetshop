from django.shortcuts import render
from .models import Cake, Review
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import ReviewForm, RegisterUserForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login


def index(request):
    return render(
        request,
        "index.html",
        context={},
    )


class CakeListView(generic.ListView):
    model = Cake
    paginate_by = 12


class CakeDetailView(generic.DetailView):
    model = Cake

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = ReviewForm()
        return context


@login_required
def add_review(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.cake = cake
            review.save()
            return redirect("cake-detail", pk=cake.id)
    else:
        form = ReviewForm()
    return render(request, "cake_detail.html", {"form": form, "cake": cake})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user and not request.user.is_superuser:
        return HttpResponseForbidden("Вы не можете редактировать этот отзыв.")
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("cake-detail", pk=review.cake.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, "edit_review.html", {"form": form})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user and not request.user.is_superuser:
        return HttpResponseForbidden("Вы не можете удалить этот отзыв.")
    cake_id = review.cake.id
    review.delete()
    return redirect("cake-detail", pk=cake_id)


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterUserForm()

    return render(request, 'registration/register.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    next_page = reverse_lazy('index')


# Выход (используем готовый LogoutView)
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')
from django.shortcuts import render
from .models import Cake, Cart, CartItem, Order, OrderCake, Review
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
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = RegisterUserForm()

    return render(request, "registration/register.html", {"form": form})


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    next_page = reverse_lazy("index")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")


@login_required
def add_to_cart(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, cake=cake)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("cart_detail")


def cart_detail(request):
    cart = None
    total_cost = 0

    if request.user.is_authenticated:
        # Если пользователь авторизован, получить корзину
        cart, created = Cart.objects.get_or_create(user=request.user)
        total_cost = sum(item.total_price for item in cart.items.all())
    else:
        # Если пользователь не авторизован, корзина пуста
        message = "Войдите или зарегистрируйтесь, чтобы добавлять товары в корзину."
        return render(request, "cart_detail.html", {"message": message})

    return render(request, "cart_detail.html", {"cart": cart, "total_cost": total_cost})


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == "POST":
        address = request.POST["delivery_address"]
        execution_date = request.POST["execution_date"]

        # Создаем заказ
        order = Order(
            user=request.user,
            execution_date=execution_date,
            status="О",
            cost=sum(item.total_price for item in cart.items.all()),
            delivery_address=address,
        )
        order.save()  # Сохраняем объект Order в базе данных

        # Переносим торты из корзины в заказ
        for item in cart.items.all():
            order_cake = OrderCake(order=order, cake=item.cake, quantity=item.quantity)
            order_cake.save()

        # Очищаем корзину
        cart.items.all().delete()

        return redirect("order_detail", order_id=order.id)

    return render(request, "checkout.html", {"cart": cart})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "order_list.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "order_detail.html", {"order": order})

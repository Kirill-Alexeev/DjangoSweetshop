from .models import Cake, Cart, CartItem, Ingredient, Order, OrderCake, Review
from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import ReviewForm, RegisterUserForm, CheckoutForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.db.models import Q
from django.core.paginator import Paginator


# Домашняя страница
def index(request):
    return render(
        request,
        "index.html",
        context={},
    )


# Список всех десертов
def cakes(request):
    query = request.GET.get("q")  # Поисковый запрос
    filter_by = request.GET.get("filter")  # Фильтр
    ingredient_filter = request.GET.get("ingredient")  # Фильтр по ингредиенту

    # Базовый запрос для тортов
    cakes = Cake.objects.all()

    if ingredient_filter:
        if query:
            # Фильтрация по ингредиенту и поисковому запросу
            cakes = cakes.filter(
                Q(ingredients__id=ingredient_filter)
                & (Q(title__icontains=query) | Q(description__icontains=query))
            )
        else:
            # Только фильтрация по ингредиенту
            cakes = cakes.filter(ingredients__id=ingredient_filter)
    elif query:
        # Только фильтрация по запросу
        cakes = cakes.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Фильтрация по дополнительным критериям
    if filter_by == "price_asc":
        cakes = cakes.order_by("price")
    elif filter_by == "price_desc":
        cakes = cakes.order_by("-price")
    elif filter_by == "title":
        cakes = cakes.order_by("title")

    # Пагинация
    paginator = Paginator(cakes, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Все доступные ингредиенты
    ingredients = Ingredient.objects.all()

    context = {
        "page_obj": page_obj,
        "query": query,
        "filter_by": filter_by,
        "ingredients": ingredients,
        "selected_ingredient": ingredient_filter,  # Выбранный ингредиент
    }
    return render(request, "cakeshop/cake_list.html", context)


# Страница десерта
class CakeDetailView(generic.DetailView):
    model = Cake

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = ReviewForm()
        return context


# Добавление отзыва
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
    return render(
        request,
        "cakeshop/cake_detail.html",
        {
            "review_form": form,
            "cake": cake,
        },
    )


# Редактирование отзыва
@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Проверка прав пользователя
    if request.user != review.user and not request.user.is_superuser:
        return HttpResponseForbidden("Вы не можете редактировать этот отзыв.")

    # Обработка формы
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("cake-detail", pk=review.cake.id)
    else:
        form = ReviewForm(instance=review)

    # Передача формы и данных в шаблон
    return render(request, "edit_review.html", {"form": form, "review": review})


# Удаление отзыва
@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user and not request.user.is_superuser:
        return HttpResponseForbidden("Вы не можете удалить этот отзыв.")
    cake_id = review.cake.id
    review.delete()
    return redirect("cake-detail", pk=cake_id)


# Регистрация пользователя
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


# Авторизация пользователя
class UserLoginView(LoginView):
    template_name = "registration/login.html"
    next_page = reverse_lazy("index")


# Выход пользователя
class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")


# Добавление десерта в корзину
@login_required
def add_to_cart(request, cake_id):
    cake = get_object_or_404(Cake, id=cake_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, cake=cake)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("cart_detail")


# Корзина
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


# Оформление заказа
@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    total_cost = sum(item.total_price for item in cart.items.all())

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Данные из формы
            address = form.cleaned_data["delivery_address"]
            execution_date = form.cleaned_data["execution_date"]

            # Создание заказа
            order = Order(
                user=request.user,
                execution_date=execution_date,
                status="О",
                cost=total_cost,
                delivery_address=address,
            )
            order.save()

            # Перемещение товаров из корзины в заказ
            for item in cart.items.all():
                order_cake = OrderCake(
                    order=order, cake=item.cake, quantity=item.quantity
                )
                order_cake.save()

            # Очистка корзины
            cart.items.all().delete()

            return redirect("order_detail", order_id=order.id)
    else:
        form = CheckoutForm()

    return render(
        request, "checkout.html", {"cart": cart, "total_cost": total_cost, "form": form}
    )


# Список заказов пользователя
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "order_list.html", {"orders": orders})


# Страница одного заказа
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    order_items = []
    for order_item in order.ordercake_set.all():
        total_price = order_item.cake.price * order_item.quantity
        order_items.append(
            {
                "cake": order_item.cake,
                "quantity": order_item.quantity,
                "unit_price": order_item.cake.price,
                "total_price": total_price,
            }
        )

    return render(
        request,
        "order_detail.html",
        {
            "order": order,
            "order_items": order_items,
        },
    )

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Cake, Order, Review, Ingredient, OrderCake, Cart, CartItem


class IngredientInline(admin.TabularInline):
    model = Cake.ingredients.through
    extra = 0


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0


class OrderCakeInline(admin.TabularInline):
    model = OrderCake
    extra = 0


@admin.register(Ingredient)
class IngredientAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'title', 'units', 'count', 'created_at', 'updated_at')
    fields = ['id', 'title', 'units', 'count', ('created_at', 'updated_at')]
    readonly_fields = ('id', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('units',)
    list_per_page = 15


@admin.register(Cake)
class CakeAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'title', 'weight', 'price', 'created_at', 'updated_at')
    fields = ['id', 'title', 'weight', 'description', 'image', 'price', ('created_at', 'updated_at')]
    readonly_fields = ('id', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_filter = ('title', 'price',)
    filter_horizontal = ('ingredients',)
    date_hierarchy = 'created_at'
    inlines = [IngredientInline, ReviewInline]
    list_per_page = 10

    @admin.display(description="Количество символов", ordering='description')
    def brief_info(self, cake: Cake):
        return f"Описание содержит {len(cake.description)} символов."


@admin.register(Review)
class ReviewAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'user', 'cake', 'review', 'created_at')
    fields = ['id', 'user', 'cake', 'review', 'created_at']
    readonly_fields = ('id', 'created_at')
    date_hierarchy = 'created_at'
    search_fields = ('review',)
    raw_id_fields = ('user', 'cake')
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'user', 'execution_date', 'status', 'cost', 'delivery_address', 'created_at', 'updated_at')
    list_display_links = ('id', 'user')
    fields = ['id', 'user', 'execution_date', 'status', 'cost', 'delivery_address', ('created_at', 'updated_at')]
    readonly_fields = ('id', 'created_at', 'updated_at')
    search_fields = ('user__username', 'delivery_address')
    list_filter = ('status', 'execution_date')
    date_hierarchy = 'created_at'
    inlines = [OrderCakeInline]
    list_per_page = 10


@admin.register(OrderCake)
class OrderCakeAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'cake')
    fields = ['id', 'order', 'cake']
    readonly_fields = ('id',)
    raw_id_fields = ('order', 'cake')
    search_fields = ('order__id', 'cake__title')
    list_per_page = 15


@admin.register(Cart)
class CartAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    list_display_links = ('id', 'user',)
    fields = ['id', 'user', ('created_at', 'updated_at')]
    readonly_fields = ('id', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'
    list_per_page = 15


@admin.register(CartItem)
class CartItemAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'cart', 'cake', 'quantity')
    list_display_links = ('id',)
    fields = ['id', 'cart', 'cake', 'quantity']
    readonly_fields = ('id',)
    list_filter = ('cake',)
    raw_id_fields = ('cart', 'cake',)
    list_per_page = 10
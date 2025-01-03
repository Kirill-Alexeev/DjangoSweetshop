from rest_framework import viewsets
from .serializers import CakeSerializer, OrderSerializer
from .models import Cake, Order
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend


class CakeViewSet(viewsets.ModelViewSet):
    queryset = Cake.objects.all()
    serializer_class = CakeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'price', 'weight']

    @action(methods=["GET"], detail=False, url_path="cheaper-than")
    def get_cakes_cheaper_than(self, request):
        """
        Возвращает список тортов дешевле указанной цены.
        Пример запроса: /api/cakes/cheaper-than/?price=1000
        """
        price = request.query_params.get("price")
        if price:
            try:
                price = float(price)
                cakes = Cake.objects.filter(price__lt=price)
                serializer = self.get_serializer(cakes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response(
                    {"error": "Некорректная цена."}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"error": "Параметр 'price' обязателен."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['execution_date', 'status', 'cost', 'delivery_address']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        return Order.objects.none()

    @action(methods=["GET"], detail=False, url_path="pending-orders")
    def pending_orders(self, request):
        """
        Возвращает заказы со статусом "ожидается".
        Пример запроса: /api/orders/pending-orders/
        """
        orders = self.get_queryset().filter(status="О")
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True, url_path="update-status")
    def update_status(self, request, pk=None):
        """
        Обновляет статус конкретного заказа.
        Пример запроса: /api/orders/<id>/update-status/
        {
            "status": "З"
        }
        """
        order = self.get_object()
        status_value = request.data.get("status")
        if status_value in dict(Order._meta.get_field("status").choices).keys():
            order.status = status_value
            order.save()
            return Response(
                {"message": "Статус успешно обновлен."}, status=status.HTTP_200_OK
            )
        return Response(
            {
                "error": f"Неверное значение статуса. Возможные значения: {list(dict(Order._meta.get_field('status').choices).keys())}."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

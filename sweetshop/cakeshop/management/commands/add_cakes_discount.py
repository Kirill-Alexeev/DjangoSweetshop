from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from cakeshop.models import Cake


class Command(BaseCommand):
    help = "Обновляет цены на все торты в зависимости от их текущей стоимости"

    def add_arguments(self, parser):
        # Добавление аргумента `--discount` для передачи скидки
        parser.add_argument(
            "--discount",
            type=float,
            help="Процент скидки, который нужно применить к стоимости тортов.",
        )

    def handle(self, *args, **kwargs):
        discount = kwargs.get("discount")

        if discount is None:
            raise CommandError(
                "Пожалуйста, укажите параметр --discount, например: --discount=10"
            )

        if discount < 0 or discount > 100:
            raise CommandError("Скидка должна быть в диапазоне от 0 до 100.")

        discount = Decimal(discount)

        # Логика команды: Применить скидку ко всем тортам
        cakes = Cake.objects.all()
        for cake in cakes:
            old_price = cake.price
            new_price = old_price - (old_price * (discount / 100))
            cake.price = round(new_price, 2)
            cake.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f'Торт "{cake.title}" обновлён: {old_price} → {cake.price}'
                )
            )

        self.stdout.write(self.style.SUCCESS("Цены успешно обновлены!"))

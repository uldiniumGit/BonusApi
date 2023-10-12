from django.db import models
import uuid
import re
from django.core.exceptions import ValidationError


class Group(models.Model):
    type = models.CharField(max_length=255, unique=True, verbose_name="Тип бонусов")
    probability = models.IntegerField(verbose_name="Вероятность выпадения")

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Типы бонусов"
        verbose_name_plural = "Типы бонусов"


class Bonus(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название бонуса")
    value = models.CharField(max_length=255, verbose_name="Цена бонуса")
    type = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Тип бонуса")
    probability = models.IntegerField(verbose_name="Вероятность выпадения")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Бонусы"
        verbose_name_plural = "Бонусы"


class Roulette(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="id рулетки")
    name = models.CharField(max_length=255, verbose_name="Название рулетки")
    bonuses = models.ManyToManyField(Bonus)
    google_table = models.ForeignKey('GoogleSheet', on_delete=models.CASCADE, null=True,
                                     verbose_name="гугл таблица, соответствующая рулетке")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рулетки"
        verbose_name_plural = "Рулетки"


def google_sheet_name_validator(value: str) -> str:
    if not re.match(r"^[a-z][a-z0-9_]{2,}$", value):
        raise ValidationError(
            "Разрешено использовать только символы латинского алфавита в "
            "нижнем регистре, цифры (кроме первого символа) и знак "
            'подчеркивания "_", минимум 3 символа'
        )
    return value


class GoogleSheet(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=32,
        unique=True,
        validators=[google_sheet_name_validator],
    )
    title = models.CharField(verbose_name="Заголовок", max_length=128)
    key = models.CharField(verbose_name="Ключ", max_length=64, unique=True)

    # objects = managers.GoogleSheetManager()

    class Meta:
        verbose_name = "Google таблица"
        verbose_name_plural = "Google таблицы"
        db_table = "google_sheets"
        ordering = ("title",)

    def __str__(self):
        return str(self.title)

from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.TextField("Название")
    picture = models.ImageField("Изображение", null=True, upload_to="groups")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Вид"
        verbose_name_plural = "Виды"

    def __str__(self) -> str:
        return self.name


class Honey(models.Model):
    name = models.TextField("Название")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True)
    picture = models.ImageField("Изображение", null=True, upload_to="honey")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Stock(models.Model):
    name = models.TextField("Название")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True)
    count = models.IntegerField("Остаток(литры)", null=True)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Остаток"
        verbose_name_plural = "Остатки"


class Order(models.Model):
    name = models.TextField("Название")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True)
    count = models.IntegerField("Заказано(литры)", null=True)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Feedback(models.Model):
    name = models.TextField("Название")
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True)
    comment = models.TextField("Отзыв", null=True)
    picture = models.ImageField("Изображение", null=True, upload_to="feedback")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
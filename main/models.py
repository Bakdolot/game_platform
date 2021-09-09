# from django.db import models
# from django.utils.translation import ugettext_lazy as _
# from django.utils import timezone
# from django.contrib.auth.models import User






# class Battle(models.Model):
#     STATUS_CHOICES = (
#         ('1', _('В ожидании')),
#         ('2', _('В процессе')),
#         ('3', _('Закончено'))
#     )

#     title = models.CharField(verbose_name=_('Название'), max_length=200)
#     description = models.TextField(verbose_name=_('Описание'))
#     rate = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Сумма брони'))
#     start_date = models.DateTimeField(verbose_name=_('Время начало'), default=timezone.now())
#     owner = models.ForeignKey(User, verbose_name=_('Заказчик'), on_delete=models.CASCADE, related_name='owner')
#     # game = models.ForeignKey(, verbose_name=_('Игра'))
#     views = models.ManyToManyField(User, verbose_name=_('Просмотры'), related_name='views')
#     reposts = models.ManyToManyField(User, verbose_name=_('Репосты'), related_name='reposts')
#     create_at = models.DateTimeField(verbose_name=_('Дата создание'), auto_now_add=True)
#     status = models.CharField(choices=STATUS_CHOICES, verbose_name=_('Статус'), max_length=50)
#     is_published = models.BooleanField(verbose_name=_('Опубликован'), default=False)

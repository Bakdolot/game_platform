from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django_resized import ResizedImageField

class User(AbstractUser):
    phone = models.CharField(verbose_name=_('Телефон'),
                             max_length=12,
                             null=True, unique=True, validators=[
            RegexValidator(regex=r'^996\d{9}$',
                           message=_('Pass valid phone number'))
        ])
    otp = models.CharField(verbose_name=_('SMS code'), max_length=4)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.phone}->{self.username}'


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    first_name = models.CharField(max_length=25, blank=True, verbose_name=_('Имя'))
    last_name = models.CharField(max_length=25, blank=True, verbose_name=_('Фамилия'))
    image = models.ImageField(upload_to='user_image/', verbose_name=_('Фотография'))
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0,verbose_name=_('Баланс'))
    whatsapp_phone = models.CharField(max_length=20, blank=True, verbose_name=_('Ватсап номер'))
    telegram_phone = models.CharField(max_length=20, blank=True, verbose_name=_('Телеграм номер'))
    description = models.TextField(blank=True, verbose_name=_('О себе'))
    steem_account = models.CharField(max_length=50, blank=True, verbose_name=_('Стим аккаунт'))
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('Лайки'), related_name='UserProfileLikes')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('Дизлайки'), related_name='UserProfileDislikes')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Профиль пользователя')
        verbose_name_plural = _('Профили пользователей')


class Identification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    name = models.CharField(max_length=100, verbose_name=_('ФИО'))
    passport_number = models.IntegerField(verbose_name=_('Номер пасспорта'))
    tin = models.IntegerField(verbose_name=_('ИНН'))
    birth_date = models.DateField(verbose_name=_('Дата рождения'))
    country = models.CharField(max_length=15, verbose_name=_('Страна'))
    city = models.CharField(max_length=15, verbose_name=_('Город'))
    address = models.CharField(max_length=40, verbose_name=_('Адресс'))
    passport_image = models.ImageField(upload_to='user_passport_image', verbose_name=_('Фото пасспорта'))
    address_confirming = models.ImageField(upload_to='user_address_confirming', verbose_name=_('Документ подтверждаюший адресс проживания'))

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = _('Идентификация')
        verbose_name_plural = _('Идентификация')


class Notification(models.Model):
    TYPE_CHOICES = (
        ('1', _('Коментарий')),
        ('2', _('Сражение создано')),
        ('3', _('Сражение завершенно')),
        ('4', _('Сражение началось')),
        ('5', _('Баланс пополнен')),
        ('6', _('Сражение отменено')),
        ('7', _('Предложение на сражение'))
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    title = models.CharField(max_length=150, verbose_name=_('Название'))
    description = models.CharField(max_length=200, verbose_name=_('Описание'))
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name=_('Тип'))
    image = ResizedImageField(_("Изображение"), size=[150, 150], quality=100,
                              upload_to='notifications/', blank=True,
                              null=True)
    
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Создано'))

    def __str__(self):
        return f'{self.title} -> {self.user.username}'
    
    class Meta:
        verbose_name = _('Уведомления')
        verbose_name_plural = _('Уведомлении')
        ordering = ['-id']
    

class UserComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Пользователь'), related_name='UserCommentUser')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Владелец'), related_name='UserCommentOwner')
    text = models.TextField(max_length=500, verbose_name=_('Текст'))

    def __str__(self):
        return f'{self.owner} -> {self.user}'
    
    class Meta:
        verbose_name = _('Коментарий')
        verbose_name_plural = _('Коментарии')
        ordering = ['-id']


class UserScores(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    score_sum = models.IntegerField(default=0, verbose_name=_('Сумма всех оценок'))
    evaluators = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('Оценщики'), through='User_Evaluators', related_name='User_Evaluators')

    def __str__(self):
        return self.user
    
    class Meta:
        verbose_name = _('Оценка')
        verbose_name_plural = _('Оценки')


class User_Evaluators(models.Model):
    user = models.ForeignKey(UserScores, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Оценщик'))
    score = models.SmallIntegerField(verbose_name=_('Оценка'))

    def __str__(self):
        return f'{self.evaluator} -> {self.user}'
    
    class Meta:
        verbose_name = _('Оценка')
        verbose_name_plural = _('Оценки')
        unique_together = [['evaluator', 'user']]

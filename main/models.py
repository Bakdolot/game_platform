from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import OrderBy
from django.db.models.fields import related
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    name = models.CharField(verbose_name=_('Название'), max_length=200)

    def __str__ (self):
        return self.name

    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')


class Game(models.Model):
    name = models.CharField(verbose_name=_('Название'), max_length=200)
    border_image = models.ImageField(upload_to='gameimages', verbose_name=_('Картинка игры'))
    category = models.ForeignKey(Category, verbose_name=_('Категорий') , on_delete=models.SET_NULL, null=True)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('Подпсчики'), blank=True)
    icon = models.ImageField(upload_to='gameicons', verbose_name=_('Иконка игры'))

    def get_battles(self):
        return Battle.objects.filter(game__id=self.id).count()

    def get_followers(self):
        return self.followers.all().count()

    def __str__ (self):
        return self.name

    def get_battles(self):
        return Battle.objects.filter(game__id=self.id).count()

    def get_followers(self):
        return self.followers.all().count()

    def get_game_border(self):
        return self.border_image.url

    def get_category_name(self):
        return self.category.name
    
    class Meta:
        verbose_name = _('Игра')
        verbose_name_plural = _('Игры')
      


class Battle(models.Model):
    STATUS_CHOICES = (
        ('1', _('В ожидании')),
        ('2', _('В процессе')),
        ('3', _('Закончено'))
    )

    title = models.CharField(verbose_name=_('Название'), max_length=200)
    description = models.TextField(verbose_name=_('Описание'))
    rate = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_('Сумма брони'))
    start_date = models.DateTimeField(verbose_name=_('Время начало'), default=timezone.now())
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Заказчик'), on_delete=models.CASCADE)
    game = models.ForeignKey(Game, verbose_name=_('Игра'), on_delete=models.SET_NULL, null=True)
    views = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('Просмотры'), related_name='views', blank=True)
    reposts = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('Репосты'), related_name='reposts', blank=True)
    create_at = models.DateTimeField(verbose_name=_('Дата создание'), auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, verbose_name=_('Статус'), max_length=50)
    is_published = models.BooleanField(verbose_name=_('Опубликован'), default=False)

    class Meta:
        verbose_name = _('Битва')
        verbose_name_plural = _('Битвы')
        ordering = ['-create_at']

    def __str__ (self):
        return f'{self.id}'

    def get_views_count(self):
        return self.views.all().count()

    def get_reposts_count(self):
        return self.reposts.all().count()

    def get_game_icon(self):
        return self.game.icon.url
    
    def get_game_border(self):
        return self.game.border_image.url


class BattleMembers(models.Model):
    FORMAT_CHOICES = (
        ('1', '1x1'),
        ('2', '3x3'),
        ('3', '5x5'),
    )

    format = models.CharField(verbose_name=('Формат'), max_length=10, choices=FORMAT_CHOICES)
    battle = models.OneToOneField(Battle, verbose_name=_('Битва'), on_delete=models.CASCADE)
    team = models.CharField(verbose_name=_('Команда'), max_length=200)
    player_1 = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Игрок 1'), on_delete=models.SET_NULL, null=True, related_name='battle_member_player_1')
    player_2 = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Игрок 2'), on_delete=models.SET_NULL, null=True, blank=True, related_name='battle_member_player_2')
    player_3 = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Игрок 3'), on_delete=models.SET_NULL, null=True, blank=True, related_name='battle_member_player_3')
    player_4 = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Игрок 4'), on_delete=models.SET_NULL, null=True, blank=True, related_name='battle_member_player_4')
    player_5 = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Игрок 5'), on_delete=models.SET_NULL, null=True, blank=True, related_name='battle_member_player_5')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Заказчик'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Участники битвы')
        verbose_name_plural = _('Участники битвы')
        ordering = ['-id']
        
        
    def __str__ (self):
        return f'{self.owner.username} -> {self.battle}'

class BattleResponse(models.Model):
    battle = models.ForeignKey(Battle, on_delete=CASCADE, verbose_name=_('Битва'))
    description = models.TextField(verbose_name=_('Описание'))
    team = models.CharField(verbose_name=_('Команда'), max_length=200)
    player_1 = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Игрок 1'), on_delete=models.SET_NULL, null=True, related_name='battle_response_player_1')
    player_2 = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Игрок 2'), on_delete=models.SET_NULL, null=True, blank=True, related_name='battle_response_player_2')
    player_3 = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Игрок 3'), on_delete=models.SET_NULL, null=True, blank=True, related_name='battle_response_player_3')
    player_5 = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Игрок 5'), on_delete=models.SET_NULL, null=True, blank=True, related_name='battle_response_player_5')
    player_4 = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Игрок 4'), on_delete=models.SET_NULL, null=True, blank=True, related_name='battle_response_player_4')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Заказчик'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Предложение на битву')
        verbose_name_plural = _('Предложения на битву')
        ordering = ['-id']

    def __str__ (self):
        return f'{self.owner.username} -> {self.battle}'

class Questions(models.Model):
    title = models.CharField(verbose_name=_('Вопрос'), max_length=200)
    text = models.TextField(verbose_name=_('Текст'))

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')

    def __str__ (self):
        return self.title

class QuestionHelp(models.Model):
    email = models.EmailField(verbose_name=_('E-Mail'))
    text = models.TextField(verbose_name=_('Текст'))
    question = models.ForeignKey(Questions, verbose_name=_('Вопрос'), on_delete=models.CASCADE, related_name='question')

    class Meta:
        verbose_name = _('Помощь')
        verbose_name_plural = _('Помощь')

    def __str__ (self):
        return self.email

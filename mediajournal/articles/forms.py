from django import forms
from django.forms.models import inlineformset_factory

from .models import Article, ArticleImage, ArticleSection


class ArticleForm(forms.ModelForm):
    """
    Форма для создания и редактирования статьи.

    Эта форма используется для создания и редактирования статей. 
    Включает поля для заголовка, категории и текста.

    Атрибуты:
        Meta (class): Настройки для модели и полей формы.
    
    Методы:
        __init__(*args, **kwargs): Инициализация формы, установка атрибутов для виджетов полей.
    """
    class Meta:
        model = Article
        fields = ['title', 'category', 'text', ]

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму и устанавливает атрибуты для виджетов полей.
        """
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Заголовок статьи'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['category'].empty_label = 'Выберите раздел'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget.attrs['placeholder'] = 'Вступление'
        self.fields['text'].widget.attrs['class'] = 'form-control'
        


class ArticleSectionForm(forms.ModelForm):
    """
    Форма для создания и редактирования раздела статьи.

    Эта форма используется для создания и редактирования разделов в статье. Включает поля для заголовка, текста и цитаты.

    Атрибуты:
        Meta (class): Настройки для модели и полей формы.
    
    Методы:
        __init__(*args, **kwargs): Инициализация формы, установка атрибутов для виджетов полей.
    """
    class Meta:
        model = ArticleSection
        fields=['title', 'text', 'quote']

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму и устанавливает атрибуты для виджетов полей.
        """
        super(ArticleSectionForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Заголовок раздела (не обязательно)'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget.attrs['placeholder'] = 'Текст'
        self.fields['text'].widget.attrs['class'] = 'form-control'
        self.fields['quote'].widget.attrs['placeholder'] = 'Умная цитата (не обязательно)'
        self.fields['quote'].widget.attrs['class'] = 'form-control'


ArticleSectionFormSet = inlineformset_factory(Article, ArticleSection, form=ArticleSectionForm , fields=['title', 'text', 'quote'], extra=1, can_delete=False, max_num=5)

ArticleImageFormSet = inlineformset_factory(Article, ArticleImage, fields=['image'], extra=2, can_delete=False, max_num=5,)

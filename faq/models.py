from django.db import models

class FAQCategory(models.Model):
    name = models.CharField('Название категории', max_length=100)
    order = models.PositiveIntegerField('Порядок отображения', default=0)

    class Meta:
        verbose_name = 'Категория FAQ'
        verbose_name_plural = 'Категории FAQ'
        ordering = ['order']

    def __str__(self):
        return self.name

class FAQItem(models.Model):
    category = models.ForeignKey(
        FAQCategory,
        on_delete=models.CASCADE,
        verbose_name='Категория',
        related_name='questions'
    )
    question = models.CharField('Вопрос', max_length=255)
    answer = models.TextField('Ответ')
    order = models.PositiveIntegerField('Порядок отображения', default=0)
    updated_at = models.DateTimeField('Дата изменения', auto_now=True)

    class Meta:
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'
        ordering = ['category__order', 'order']

    def __str__(self):
        return self.question
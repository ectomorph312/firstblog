from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(verbose_name='Нравится', default=0)
    dislike = models.IntegerField(verbose_name='Не нравится', default=0)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', args=[str(self.id)])


class Comment(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments',null=True, blank=True)
    comment = models.TextField(max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    # def __str__(self):
    #     return self.comment

    # def get_absolute_url(self):
    #     return reverse('article_list')
    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'comment by {} on {}'.format(self.author, self.article)


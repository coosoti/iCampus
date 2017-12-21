from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('careers:all_careers_by_category', args=[self.slug])

class Career(models.Model):
    category = models.ForeignKey(Category, related_name='careers')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    name = models.CharField(max_length=200,db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    summary = models.TextField(blank=True)
    duties =  models.TextField(blank=True)
    learning_path =  models.TextField(blank=True)
    work_environment = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'), )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('careers:career_detail', args=[self.id, self.slug])

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type    




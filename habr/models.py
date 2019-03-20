from django.db import models
from django.urls import reverse
from django.conf.urls import url
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class Category(models.Model):

	name = models.CharField(max_length=50)
	slug = models.SlugField()

	def __str__(self):
		return self.name


	def get_absolute_url(self):
		return reverse('category-detail', kwargs={'slug': self.slug})

def generic_filename(instance, filename):
	filename = instance.slug + '.jpg'
	return "{0}/{1}".format(instance, filename)


class Article(models.Model):

	author = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	category = models.ForeignKey(Category,on_delete=models.CASCADE, null=True)
	title = models.CharField(max_length=120)
	slug = models.SlugField()
	image = models.ImageField(upload_to=generic_filename, blank=True, null=True)
	content = models.TextField()
	likes = models.PositiveIntegerField(default=0)
	comments = GenericRelation('comments')
	users_reaction = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='users_reaction', blank=True)
	
	def __str__(self):

		return self.title

	def get_absolute_url(self):
		return reverse('article-detail', kwargs={'slug': self.slug})



class Comments(models.Model):

	author = models.ForeignKey(settings.AUTH_USER_MODEL)
	comment = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')


class UserAccount(models.Model):

	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.EmailField()
	favorite_articles = models.ManyToManyField(Article, related_name='favorite_articles')
	my_article = models.ManyToManyField(Article)

	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse('account_view', kwargs={'user': user.username})

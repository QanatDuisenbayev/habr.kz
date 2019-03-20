from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import JsonResponse, HttpResponseRedirect
from habr.models import Article, Category, UserAccount
from habr.forms import CommentForm, RegistrationForm, LoginForm, ArticleCreateForm
from django.views import View
from django.urls import reverse
from habr.mixins import CategoryListMixin
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.db.models import Q

User = get_user_model()

class ArticleListView(ListView):

	model = Article
	template_name = 'index.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ArticleListView, self).get_context_data(*args, **kwargs)
		context['articles'] = self.model.objects.all()
		return context

class CategoryListView(ListView):

	model = Category
	template_name = 'index.html'

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryListView, self).get_context_data(*args, **kwargs)
		context['categories'] = self.model.objects.all()
		context['articles'] = Article.objects.all()
		return context


class CategoryDetailView(DetailView, CategoryListMixin):

	model = Category
	template_name = "category_detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
		context['category'] = self.get_object()
		context['articles_from_category'] = self.get_object().article_set.all()
		return context
	
class ArticleDetailView(DetailView, CategoryListMixin):
	
	model = Article
	template_name = "article_detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
		context['articles'] = self.model.objects.all()
		context['article'] = self.get_object()
		context['article_comments'] = self.get_object().comments.all()
		context['article'] = self.get_object()
		context['form'] = CommentForm()
		context['current_user'] = UserAccount.objects.get(user=self.request.user)

		return context

class ArticleCreate(View, CategoryListMixin):

	template_name = 'new_post.html'

	def get(self, request, *args, **kwargs):
		form = ArticleCreateForm(request.POST or None)
		context = {
			'form': form
		}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = ArticleCreateForm(request.POST or None)
		if form.is_valid():
			new_article = form.save(commit=False)
			category = form.cleaned_data['category']
			title = form.cleaned_data['title']
			slug = form.cleaned_data['slug']
			image = form.cleaned_data['image']
			content = form.cleaned_data['content']
			new_article.save()
			Article.objects.create(	   author = request.user,
									   category = new_article.category,
									   title = new_article.title,
									   slug = new_article.slug,
									   image = new_article.image,
									   content = new_article.content)
			return HttpResponseRedirect('/')
		context = {
			'form': form
		}
		return render(self.request, self.template_name, context)

class CreateCommentView(View):

	template_name = 'article_detail.html'

	def post(self, request, *args, **kwargs):
		article_id = self.request.POST.get('article_id')
		comment = self.request.POST.get('comment')
		article = Article.objects.get(id = article_id)
		new_comment = article.comments.create(author=request.user, comment = comment)
		comment = [{ 'author': new_comment.author.username, 'comment' : new_comment.comment, 'timestamp': new_comment.timestamp.strftime('%Y-%m-%d') }]
		return JsonResponse(comment, safe=False)


class UserReactionView(View):

	template_name = 'article_detail.html'

	def get(self, request, *args, **kwargs):
		article_id = self.request.GET.get('article_id')
		article = Article.objects.get(id=article_id)
		like = self.request.GET.get('like')
		if like and (request.user not in article.users_reaction.all()):
			article.likes += 1
			article.users_reaction.add(request.user)
			article.save()
		data = {
			'likes' : article.likes,
		}
		return JsonResponse(data)

class RegistrationView(View, CategoryListMixin):

	template_name = 'registration.html'

	def get(self, request, *args, **kwargs):

		form = RegistrationForm(request.POST or None)
		context = {
			'form': form
		}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = RegistrationForm(request.POST or None)
		if form.is_valid():
			new_user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			new_user.set_password(password)
			password_check = form.cleaned_data['password_check']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			email = form.cleaned_data['email']
			new_user.save()
			UserAccount.objects.create(user=User.objects.get(username=new_user.username),
									   first_name=new_user.first_name,
									   last_name = new_user.last_name,
									   email= new_user.email)
			return HttpResponseRedirect('/')
		context = {
			'form': form
		}
		return render(self.request, self.template_name, context)


class LoginView(View, CategoryListMixin):

	template_name = 'login.html'

	def get(self, request, *args, **kwargs):

		form = LoginForm(request.POST or None)
		context = {
			'form': form
		}
		return render(self.request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = LoginForm(request.POST or None)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user:
				login(self.request, user)
				return HttpResponseRedirect('/')
		context = {
			'form': form
		}
		return render(self.request, self.template_name, context)

		

class UserAccountView(DetailView, CategoryListMixin):

	template_name = 'user_account.html'

	def get(self, request, *args, **kwargs):
		user = self.kwargs.get('user')
		current_user = UserAccount.objects.get(user=User.objects.get(username=user))
		context = {
			'current_user' : current_user
		}
		return render(self.request, self.template_name, context)


class AddArticleToFavorites(View):
	template_name = 'article_detail.html'

	def get(self, request, *args, **kwargs):
		article_slug = self.request.GET.get('article_slug')
		article = Article.objects.get(slug=article_slug)
		current_user = UserAccount.objects.get(user=request.user)
		current_user.favorite_articles.add(article)
		current_user.save()
		return JsonResponse({'ok':'ok'})


class SearchView(View):

	template_name = 'search.html'

	def get(self, request, *args, **kwargs):
		query = self.request.GET.get('q')
		founded_articles = Article.objects.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query))
		context = {
			'founded_articles': founded_articles
		}
		return render(self.request, self.template_name, context)


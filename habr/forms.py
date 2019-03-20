from django import forms
from django.contrib.auth import get_user_model
from habr.models import Article, Category
User = get_user_model()

class CommentForm(forms.Form):

	comment = forms.CharField(widget=forms.Textarea)
	
class LoginForm(forms.Form):

	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		user = User.objects.get(username=username)
		if not user.check_password(password):
			raise forms.ValidationError('Құпия сөз қате!')

class RegistrationForm(forms.ModelForm):
	password_check = forms.CharField(widget=forms.PasswordInput)
	password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'password_check',
			'first_name',
			'last_name',
			'email',
		]
	def clean(self):
		password = self.cleaned_data['password']
		password_check = self.cleaned_data['password_check']
		if password != password_check:
			raise forms.ValidationError('Құпия сөздеріңіз сәйкес келмейді!')



class ArticleCreateForm(forms.ModelForm):

	class Meta:
		model = Article
		fields = [
			'category',
			'title',
			'slug',
			'image',
			'content',
		]
	def clean_slug(self):
		new_slug = self.cleaned_data['slug'].lower()
		if new_slug == 'create':
			raise ValidationError('Slug may not be "Create"')
		return new_slug
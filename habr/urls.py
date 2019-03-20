from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
#from . import views
#from django.views.generic import TemplateView
from habr.views import ( CategoryListView, 
						CategoryDetailView,
						ArticleDetailView,
						CreateCommentView,
						UserReactionView,
						RegistrationView,
						LoginView,
						UserAccountView,
						ArticleCreate,
						AddArticleToFavorites,
						SearchView
						)

urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='base_view'),
    url(r'^user_account/(?P<user>[-\w]+)/$', UserAccountView.as_view(), name='account_view'),
    url(r'^category/(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name='category-detail'),
	url(r'^add_comment/$', CreateCommentView.as_view(), name='add_comment'),
	url(r'^user_reaction/$', UserReactionView.as_view(), name='user_reaction'),
	url(r'^registration/$', RegistrationView.as_view(), name='registration'),
	url(r'^login_view/$', LoginView.as_view(), name = 'login_view'),
	url(r'^article_create/$', ArticleCreate.as_view(), name='new_post'),
	url(r'^add_to_favorites/$', AddArticleToFavorites.as_view(), name='add_to_favorites'),
	url(r'^logout/$', LogoutView.as_view(next_page=reverse_lazy('base_view')), name='logout_view'),
	url(r'^search/$', SearchView.as_view(),name='search-view'),
	url(r'^(?P<slug>[-\w]+)/$', ArticleDetailView.as_view(), name='article-detail'),

]

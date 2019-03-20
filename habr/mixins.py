from django.views.generic.list import MultipleObjectMixin
from habr.models import Category


class CategoryListMixin(MultipleObjectMixin):

	def get_context_data(self, *args, **kwargs):
		context = {}
		context['categories'] = Category.objects.all()
		context['category'] = self.get_object()
		return context
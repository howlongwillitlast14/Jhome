from django import forms

from .models import Article

class ArticleForm(forms.ModelForm):
	class Meta:##everything that is not on the form
		model = Article
		fields = ('title', 'body', 'pub_date')###To hid likes from the create article template


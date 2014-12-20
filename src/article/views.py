#python first
#3django second
#your apps

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from django.core.context_processors import csrf
from .forms import ArticleForm
from .models import Article
# Create your views here.

def articles(request):
	return render_to_response('articles.html/', {'articles': Article.objects.all() })

def article(request, article_id):
	return render_to_response('article.html/', {'article': Article.objects.get(id=article_id)})

def home(request):

	form = ArticleForm(request.POST or None)
	if form.is_valid():
		save_it = form.save(commit=False)
		save_it.save()
		return HttpResponseRedirect('/thank-you/')

	language = 'en-gb'
	session_language = 'en-gb'
	
	if 'lang' in request.COOKIES:
			language = request.COOKIES['lang']
	if 'lang' in request.session:
		session_language = request.session['lang']

	return render_to_response("signup.html", {'language': language,
												'session_language': session_language,
												'form': form},
						context_instance=RequestContext(request))

def thankyou(request):

	return render_to_response("thankyou.html", locals(),
						context_instance=RequestContext(request))

def aboutus(request):

	return render_to_response("aboutus.html", locals(),
						context_instance=RequestContext(request))


def language(request, language='en-gb'):

	response = HttpResponse("setting language to %s" % language)

	response.set_cookie('lang', language)

	request.session['lang'] = language
	return response

def create(request):
	if request.POST:
		form = ArticleForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/articles/all')
	else:
		form = ArticleForm()
	args = {}
	args.update(csrf(request))

	args['form'] = form
	return render_to_response('create_article.html', args)

def like_article(request, article_id):
	if article_id:
		a = Article.objects.get(id=article_id)
		count = a.likes
		count +=1
		a.likes = count
		a.save()## when saving, updating a record always remeber!!

	return HttpResponseRedirect('/articles/get/%s' % article_id)



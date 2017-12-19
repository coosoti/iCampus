from django.shortcuts import render, get_object_or_404
from .models import Category, Career

def all_careers(request, category_slug=None):
	category = None
	categories = Category.objects.all()
	careers = Career.objects.all()
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		careers = careers.filter(category=category)
	return render(request,
	              'careers/list.html',
	              {'category': category,
	                'categories': categories,
	                'careers': careers })

def career_detail(request, id, slug):
	career = get_object_or_404(Career, id=id, slug=slug)
	return render(request, 
		          'careers/detail.html',
		          {'career': career })

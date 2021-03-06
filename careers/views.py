from django.shortcuts import render, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from common.decorators import ajax_required
from .models import Category, Career, Task
from comments.forms import CommentForm
from comments.models import Comment
from actions.utils import create_action

import redis

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST,
	                  port=settings.REDIS_PORT,
	                  db=settings.REDIS_DB)

def all_careers(request, category_slug=None):
	category = None
	categories = Category.objects.all()
	careers = Career.objects.all()
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		careers = careers.filter(category=category)
	query = request.GET.get("q")	
	if query:
		careers = careers.filter(
					Q(name__icontains=query)|
					Q(summary__icontains=query)
					).distinct()

	paginator = Paginator(careers, 20)
	page = request.GET.get('page')

	try:
		careers = paginator.page(page)
	except PageNotAnInteger:
		careers = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			return HttpResponse('')
		careers = Paginator.page(paginator.num_pages)
	if request.is_ajax():
		return render(request,
			          'careers/list_ajax.html',
			          {'category': category,
			           'categories': categories,
			           'careers': careers,
			           'section': 'home' })

	return render(request,
				  'careers/list.html',
				  {'category': category,
					'categories': categories,
					'careers': careers,
					'section': 'home' })


def career_detail(request, id, slug):
	career = get_object_or_404(Career, id=id, slug=slug)

	# Handling comments
	instance = career # For the purpose of adding generic commenting system.
	initial_data = {
			"content_type": instance.get_content_type,
			"object_id": instance.id
	}
	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()


		new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj,
						)
		create_action(request.user, 'reviewed', career)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
	tasks = Task.objects.filter(career=career)	
	comments = instance.comments
	# total_views = r.incr('career:{}:views'.format(career.id))
	return render(request, 
				  'careers/detail.html',
				  {'career': career,
				  'comments': comments,
				  'comment_form': form,
				  # 'total_views': total_views,
				  'tasks': tasks })

@ajax_required
@login_required
@require_POST
def career_vote(request):
	career_id = request.POST.get('id')
	action = request.POST.get('action')
	if career_id and action:
		try:
			career = Career.objects.get(id=career_id)
			if action == 'like':
				career.upvotes.add(request.user)
			else:
				career.upvotes.remove(request.user)
			return JsonResponse({'status':'ok'})
		except:
			pass
	return JsonResponse({'status':'ko'})

# class CareerSearchListView(ListView):
#     model = Career
#     paginate_by = 10

#     def get_queryset(self):
#         qs = Blog.objects.published()
#         keywords = self.request.GET.get('q')
#         if keywords:
#             query = SearchQuery(keywords)
#             title_vector = SearchVector('title', weight='A')
#             content_vector = SearchVector('content', weight='B')
#             vectors = title_vector + content_vector
#             qs = qs.annotate(search=vectors).filter(search=query)
#             qs = qs.annotate(rank=SearchRank(vectors, query)).order_by('-rank')
#         return qs
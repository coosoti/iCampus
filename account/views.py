from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from common.decorators import ajax_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from actions.models import Action
from actions.utils import create_action

def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			profile = Profile.objects.create(user=new_user)
			create_action(new_user, 'has updated their account')
			return render(request,
						  'account/signup_success.html',
						  {'new_user': new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request, 
				  'account/signup.html',
				   {'user_form': user_form})			

@login_required
def dashboard(request):
	return render(request, 
				  'account/dashboard.html',
				  {'section': 'dashboard'})
@login_required
def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user, data=request.POST)
		profile_form = ProfileEditForm(
									 instance=request.user.profile,
									 data=request.POST,
									 files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Profile updated successfully')

		else:
			messages.error(request, 'Error updating your profile')	
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)

	return render(request,
				   'account/edit.html',
				   {'user_form': user_form,
				   'profile_form': profile_form})	
			
@login_required
def user_list(request):
	users = User.objects.filter(is_active=True)
	paginator = Paginator(users, 15)
	page = request.GET.get('page')
	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		if request.is_ajax():
			return HttpResponse('')
		users = Paginator.page(paginator.num_pages)
	if request.is_ajax():
		return render(request,
			          'account/user/list_ajax.html',
			          {'users': users,
			           'section': 'users' })

	return render(request, 'account/user/list.html', {'users': users, 'section': 'users' })


@login_required
def user_detail(request, username):
	user = get_object_or_404(User, username=username, is_active=True)
	actions = Action.objects.all().exclude(user=request.user)
	following_ids = request.user.following.values_list('id', flat=True)
	if following_ids:
		actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
		actions = actions[:10]
	return render(request, 'account/user/detail.html', {'actions': actions, 'user': user, 'section': 'user'})

@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, 
                	                          user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, 
                	                   user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})
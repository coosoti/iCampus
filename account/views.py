from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			profile = Profile.objects.create(user=new_user)
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
	return render(request, 'account/user/list.html', {'users': users, 'section': 'users' })


@login_required
def user_detail(request, username):
	user = get_object_or_404(User, username=username, is_active=True)
	return render(request, 'account/user/detail.html', {'user': user, 'section': 'users'})

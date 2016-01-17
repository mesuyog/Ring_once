from django.shortcuts import render

# Create your views here.

from login.forms import UserProfileForm,RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from .models import UserProfile
from django.shortcuts import get_object_or_404

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            )
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            #print profile_form.phone
            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']


            # Now we save the UserProfile model instance.
            profile.save()
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
        profile_form = UserProfileForm()
    variables = RequestContext(request, {
    'form': form,
    'profile_form': profile_form
    })

    return render_to_response(
    'registration/register.html',
    variables,
    )

def register_success(request):
    return render_to_response(
    'registration/success.html',
    )

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def home(request):
    #obj = get_object_or_404(UserProfile, pk=1)
    #print "1111111111111111111111111111111111111111111111",obj.phone
    obj = UserProfile.objects.all()
    #print obj.phone
    for p in obj:
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++",p.phone


    #print "++++++++++++++++++++++++++++++++++++++++++++++=",obj

    return render_to_response(
    'home.html',
    { 'user': request.user,
      'obj': obj}
    )

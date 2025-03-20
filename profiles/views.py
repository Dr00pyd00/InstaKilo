from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ProfileForm
from .models import ProfileModel
from django.contrib import messages
from typing import Dict
from django.http import HttpRequest, HttpResponse

# Create your views here.


# creation d'une page de profile personnalisée:
def ProfileCreate(request: HttpRequest) -> HttpResponse:
    profile_exists: ProfileModel = ProfileModel.objects.filter(user=request.user).exists()

    if profile_exists:
        return redirect('profiles:doublon')
    if request.method == 'POST':
        # ne pas oublier FILES pour les photos !!!
        form: ProfileForm = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            return redirect('main:home')
    else:
        form: ProfileForm = ProfileForm()
        ctx: Dict[str, ProfileForm] = {'form':form}
        return render(request, 'profiles/profile_edit.html', ctx)
    


    
def ProfilDoublon(request: HttpRequest) -> HttpResponse:
    return render(request, 'profiles/doublon_profile.html')
    




def ProfileShow(request: HttpRequest) -> HttpResponse:
    try:
        profile: ProfileModel = ProfileModel.objects.get(user=request.user)
        ctx: Dict[str, ProfileModel] = {'profile':profile}
        return render(request, 'profiles/profile_page.html', ctx)
    except ProfileModel.DoesNotExist:
        return render(request, 'profiles/profile_missing.html')
    



def ProfileEdit(request: HttpRequest) ->HttpResponse:
    if request.method == 'POST':
        profile: ProfileModel = ProfileModel.objects.get(user=request.user)
        form: ProfileForm = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profiles:my-profile')
    else:
        profile: ProfileModel = ProfileModel.objects.get(user=request.user)
        form: ProfileForm = ProfileForm(instance=profile)
        ctx: Dict[str, ProfileForm] = {'form':form}
        return render(request, 'profiles/profile_edit.html', ctx)
    



def ProfileDelete(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        if request.POST.get('delete'):
            profile: ProfileModel = ProfileModel.objects.get(user=request.user)
            profile.delete()
            messages.success(request, 'You deleted you profile page !')
        else:
            messages.warning(request, 'You canceled the delete of profile !')

        return redirect('main:home')
    
    return render(request, 'profiles/delete_profile.html')
from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from blog.models import Place
from blog.models import Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.decorators import not_logged_user
from django.contrib.auth.views import LoginView

@not_logged_user
def register(request):
    if request.method == "POST":
        #form = UserCreationForm(request.POST)
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, message=f"User {username} was created successfully.")
            return redirect("signin")
    else:
        form = UserRegistrationForm()
    context = {"form":form}
    return render(request, "users/signup.html", context)

class CustomLoginView(LoginView):
    """I created this custom login view to add the constraint that only
    not logged in users can access this view, which doesn't come by default in LoginView"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("blog_home")
        return super().dispatch(request, *args, **kwargs)

def custom_logout(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, message="You have successfully logged out.")
        return redirect("signin")
    messages.error(request, message="You can't log out this way.")
    return redirect("404")

@login_required
def profile(request, pk):
    context = {"categories":Category.objects.all()}
    if pk != request.user.pk:
        other_user = get_object_or_404(User, pk=pk)
        context["other_user"] = other_user
        places_i_reviewed = Place.objects.filter(review__user=other_user).order_by("id").distinct()
    else:
        places_i_reviewed = Place.objects.filter(review__user=request.user).order_by("id").distinct()

    places_i_reviewed_paginated = Paginator(places_i_reviewed, 2)
    try:
        page_obj = places_i_reviewed_paginated.get_page(request.GET.get("page"))
    except EmptyPage:
        page_obj = places_i_reviewed_paginated.get_page(1)
    except PageNotAnInteger:
        page_obj = places_i_reviewed_paginated.get_page(1)
    context["page_obj"] = page_obj
    return render(request, "users/profile.html", context)

@login_required
def update_user(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, message="La información se actualizo exitosamente! :)")
            return redirect("profile", u_form.instance.id)
        else:
            messages.error(request, message="La información provista no fue adecuada.")
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {"u_form":u_form, "p_form":p_form, "categories":Category.objects.all()}
    return render(request, "users/update_info.html", context)

@login_required
def delete_user(request):
    context = {"categories":Category.objects.all()}
    if request.method == "POST":
        if request.POST.get("btn-delete") == "pressed":
            user = get_object_or_404(User, pk=request.user.pk)
            logout(request)
            user.delete()
            messages.success(request, message="Your account was deleted successfully!")
            return redirect("signin")
    return render(request, "users/delete_user.html", context)




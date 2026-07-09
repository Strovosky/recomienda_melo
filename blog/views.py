from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from .models import Place, Review, Category, Like
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CreatePlace, ReviewForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


@login_required
def home(request):
    context = {"categories": Category.objects.all()}
    word = request.GET.get("seach_word")
    if word:
        w_found = Place.objects.filter(name__icontains=word)
        context["places"] = w_found
        return redirect("blog_places")
    else:        
        places = Place.objects.order_by("-id")[:5]
        context["places"] = places
    return render(request, "blog/index.html", context=context)

class PlaceListViewIndex(LoginRequiredMixin, ListView):
    model = Place
    template_name = "blog/index.html" #default one is: <app>/<model>_<viewtype>.html
    context_object_name = "places"

    def get_queryset(self):
        qs = super().get_queryset().order_by("-id")[:5]
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

def about(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, "blog/about.html", context)

def four_o_four(request):
    return render(request, "blog/404.html")

class PlaceDetailView(FormMixin, DetailView):
    model = Place
    template_name = "blog/detail_place.html"
    context_object_name = "place"
    form_class = ReviewForm

    def get_success_url(self):
        return redirect("detail", pk=self.object.pk).url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        if "form" not in context:
            context["form"] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form() 
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.place = self.object
            comment.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)
    
    
### Here we have the places list views ###
@login_required
def places_view(request):
    """This view will help display all the places that are gonna be reviewed"""
    context = {"categories":Category.objects.all(), "places":Place.objects.all()[::-1]}
    return render(request, "blog/places.html", context)

class PlaceListView(LoginRequiredMixin, ListView):
    """This view will help display all the places that are gonna be reviewed"""
    model = Place
    template_name = "blog/places.html"
    context_object_name = "places"
    ordering = ["-id"]
    paginate_by = 2

    def get_queryset(self):
        qs = super().get_queryset()
        word = self.request.GET.get("search_word")
        category = self.request.GET.get("category_opt")
        if word:
            qs = qs.filter(name__icontains=word)            
        if category:
            qs = qs.filter(category__name=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

### These are the views to create a new place ###
@login_required
def create_place_view(request):
    categories, places = Category.objects.all(), Place.objects.all()[::-1]
    context = {"categories":categories, "places":places}
    if request.method == "POST":
        if request.POST.get("create_place") == "pressed":
            form = CreatePlace(request.POST, request.FILES)
            if form.is_valid():
                place = form.save(commit=False)
                place.user = request.user
                place.save()
                messages.success(request, message="The place to review has been created successfully! :)")
                return redirect("detail", place.id)
            else:
                context["form"] = form
                return render(request, "blog/places.html", context)
    form = CreatePlace()
    context["form"] = form
    return render(request, "blog/places.html", context)

class CreatePlaceView(LoginRequiredMixin, CreateView):
    """This view will displayed the places to review paginated"""

    model = Place
    template_name = "blog/create_place.html"
    fields = ["name","address","phone","description","image"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


### These are the views to update an existing place ###

class UpdatePlaceView(LoginRequiredMixin, UpdateView):
    """We'll use this view to update infomrmacion of a specific Place instance"""
    model = Place
    template_name = "blog/update_place.html"
    fields = ["name", "address", "phone", "description", "image"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user.id != request.user.id:
            return redirect("detail", obj.id)
        return super().dispatch(request, *args, **kwargs)

class DeletePlaceView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """This view will delete a place"""
    model = Place
    template_name = "blog/delete_place_confirm.html"
    success_url = reverse_lazy("blog_places")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context
    
    def test_func(self):
        place = self.get_object()
        if place.user == self.request.user:
            return True
        return False
    
class CreateLikeView(LoginRequiredMixin, CreateView):
    class Meta:
        model = Like
        fields = []

    def form_valid(self, form):
        if form.is_valid():
            form.instance.user = self.request.user
            form.instance.place = Place.objects.get(id=self.request.kwargs["pk"])
        return super().form_valid(form)
    
def create_like_place_view(request, place_pk):
    """A user can like a place instance only once"""
    place = get_object_or_404(Place, pk=place_pk)
    like = Like.objects.filter(user=request.user, place=place)

    if not like.exists():
        like = Like.objects.create(user=request.user, place=place)
    
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)
    return redirect("blog_home") 
    









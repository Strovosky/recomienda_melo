from django.urls import path
from .views import (
    home,
    about,
    four_o_four,
    places_view,
    PlaceDetailView,
    PlaceListView,
    PlaceListViewIndex,
    CreatePlaceView,
    UpdatePlaceView,
    DeletePlaceView)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(route="", view=home, name="blog_home"),
    path(route="about/", view=about, name="blog_about"),
    path(route="404/", view=four_o_four, name="404"),
    path(route="detail/<int:pk>/", view=PlaceDetailView.as_view(), name="detail"),
    #path(route="places/", view=places_view, name="blog_places"),
    path(route="places/", view=PlaceListView.as_view(), name="blog_places"),
    path(route="update_place/<int:pk>/", view=UpdatePlaceView.as_view(), name="blog_update_place"),
    path(route="delete_place/<int:pk>/", view=DeletePlaceView.as_view(), name="blog_delete_place"),
    path(route="create_place/", view=CreatePlaceView.as_view(), name="blog_create_place")
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


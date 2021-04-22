from django.urls import path
from django.contrib.auth.decorators import login_required

#Custom Imports
from .views import ( IndexView,
					SubjectsView, ProfileDetailView,
					ImporterView )

app_name = 'dashboard'

# URLs dashboard
urlpatterns = [
    path('', login_required(IndexView.as_view()), name='index'),
    path('subjects', login_required(SubjectsView.as_view()), name='subjects'),
    path('profile/<int:pk>/', login_required(ProfileDetailView.as_view()),  name='profile'),
    path('importer', login_required(ImporterView.as_view()), name='importer'),

]

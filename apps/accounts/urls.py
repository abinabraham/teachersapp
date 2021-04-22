from django.urls import path

#Custom Imports
from .views import ( AccountLoginView,
                     LogoutView )

app_name = 'accounts'
urlpatterns = [
            # Login, logout and register doesn't require login
            path('login/', AccountLoginView.as_view(), name='login'),
            path('logout/', LogoutView.as_view(), name='logout'),           
        ]

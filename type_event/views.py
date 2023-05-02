from django.views.generic import RedirectView
from django.contrib.auth import logout
from django.shortcuts import redirect

class HomePageView(RedirectView):
    url = 'users/login/'


def logout_view(request):
    logout(request)
    return redirect('home')

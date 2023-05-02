from django.views.generic import RedirectView

class HomePageView(RedirectView):
    url = 'users/login/'
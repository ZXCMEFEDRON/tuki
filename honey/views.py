from django.http import HttpResponse
from django.views import View

from honey.models import Honey

class ShowHoneyView(View):
    def get(request, *args, **kwargs):
        honey = Honey.objects.all()

        results = ""
        for s in honey:
            result += s.name + "<br>"

        return HttpResponse(result)
# Create your views here.
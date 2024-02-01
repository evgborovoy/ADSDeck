from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class Root(View):
    def get(self, request):
        if request.method == "GET":
            response = {
                "status": "ok"
            }
            return JsonResponse(response, safe=False)

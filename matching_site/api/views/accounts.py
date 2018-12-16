import json

from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse

from accounts.forms import ProfileImageForm
from accounts.models import ProfileImage

def upload_profile_image(request):
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES)
        print(request.POST)
        print(request.FILES)
        if form.is_valid():
            new_pic = form.save()
            return JsonResponse(dict(
                image_link=new_pic.image.url, 
                image_name=new_pic.image.name
            ))
        else:
            print(form.errors)
            return HttpResponseBadRequest(reason='File uploaded is not a valid image.')
    return HttpResponseNotAllowed(['POST'])

                
            
            
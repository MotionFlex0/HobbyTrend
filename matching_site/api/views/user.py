import json

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse

from accounts.models import UserProfile

# Send information related to the logged in user in JSON format
@login_required
def me(request):
    return JsonResponse(request.user.as_json())

# Add and remove hobbies for the logged in user
@login_required
def my_hobbies(request):
    if request.method == 'POST':
        if 'hobby' in request.POST:
            request.user.add_hobby(request.POST['hobby'])
    elif request.method == 'DELETE':
        request_json = json.loads(request.body.decode(encoding='utf-8'))
        if 'hobby' in request_json:
            request.user.remove_hobby(request_json['hobby'])

    return JsonResponse(request.user.hobbies_as_json())

#Returns information about another user
@login_required
def user_req(request, user_id):
    if user_id == None:
        return JsonResponse({})
    try:
        user_obj = UserProfile.objects.filter(id=user_id).get()
    except ObjectDoesNotExist:
        raise Http404('Unknown user selected')  

    if (request.method == 'GET'):    
        return JsonResponse(user_obj.as_json())


#This returns a JSON of all the user who have similar interest ; It also filters based on gender and age
@login_required
def common_interest_users(request):
    users = {}
    sorted_users = {}
    
    count = 0
    for u in UserProfile.objects.all():
        if u.pk != request.user.pk:
            users[count] = u.as_json()
            users[count]["age"] = u.calc_age()
            users[count]["common_hobbies"] = compare_interest(request, u)
            count += 1

    if 'gender' in request.GET:
        genderFilter = request.GET['gender']
    else:
        genderFilter = ""

    if 'minAge' in request.GET:
        minAgeFilter = int(request.GET['minAge'])
    else:
        minAgeFilter = 0

    if 'maxAge' in request.GET:
        maxAgeFilter = int(request.GET['maxAge'])
    else:
        maxAgeFilter = 99    

    for k in list(users.keys()):
        if genderFilter == "None" or genderFilter != "Both" and genderFilter != users[k]['gender'] or minAgeFilter >= int(users[k]['age']) or maxAgeFilter <= int(users[k]['age']):
            del users[k] 

    finalLength = 0
    for u in sorted(users.keys(), key=lambda x: users[x]['common_hobbies'], reverse=True):
        sorted_users[finalLength] = users[u]
        finalLength += 1
        
    sorted_users['length'] = finalLength 
    return JsonResponse(sorted_users)

#Helper function. It compared the interest of the logged in user, and another user - returning how similar they are
def compare_interest(request, other_user):
    count = 0
    for h in request.user.hobbies.all():
        if other_user.hobbies.filter(pk=h.pk):
            count += 1
    return count
from xml.parsers.expat import model
from django.shortcuts import render
from django.template.loader import render_to_string
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from userapp.models import UserProfile
# from dashboard.views import AjaxableResponseMixin
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


# need to add csrf_protect decorator in all ajax requests
# generate seperate csrftokens for each requests including login
@csrf_exempt
def LoginStatusQuery(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            csrf_token = get_token(request)
            server_reponse = {'status':1,'csrftoken':csrf_token}
            print('user is logged in')
            return JsonResponse(server_reponse)
        else:
            print('Login is required')
            auth_form = AuthenticationForm()
            login_modal = render_to_string('userapp/login_modal.html',{'auth_form':auth_form},request)
            server_reponse = {'status':2,'login_modal':login_modal}
            return JsonResponse(server_reponse)

def ModalLogin(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            username = request.POST['username']
            password = request.POST['password']
            user_account = authenticate(username=username,password=password)
            if user_account is not None:
                print("User is Authenticated")
                login(request,user_account)
                print("User is signed in")
                # csrf_token = RequestContext(request)
                csrf_token = get_token(request)
                SERVER_RESPONSE = {'status':1,'csrftoken':csrf_token}
                return JsonResponse(SERVER_RESPONSE)
            else:
                print("Invalid User")
                SERVER_RESPONSE = {'status':0}
                return JsonResponse(SERVER_RESPONSE)

class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    context_object_name = "userprofile"
    template_name = "userapp/userprofile.html"

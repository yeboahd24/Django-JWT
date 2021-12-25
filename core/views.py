from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from core.serializers import UserRegistrationSerializer, UserLoginSerializer
from .models import UserProfile
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from .forms import SignupForm, LoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

class UserProfileView(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'full_name': user_profile.full_name,
                    'email': user_profile.email,
                     }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)




class UserRegistrationView(CreateAPIView):

    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User registered  successfully',
            }
        status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

class UserLoginView(RetrieveAPIView):

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)




def signup(request):
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        form.full_name = request.POST.get('full_name', '')
        form.email = request.POST.get('email', '')
        form.password = request.POST.get('password', '')
        form.password2 = request.POST.get('password2', '')
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # NB: we are using the HttpResponse here for the mean time
            # This is just for testing purposes
            return redirect('user_login')
        else:
            return HttpResponse('Invalid form')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        form.email = request.POST.get('email', '')
        form.password = request.POST.get('password', '')

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd['email'], password=cd['password'])
            if user is None:
                return HttpResponse('Invalid login')

            if not user.is_active:
                return HttpResponse('Disabled account')

            login(request, user)
            # return redirect('home')
            return HttpResponse('Successfully login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
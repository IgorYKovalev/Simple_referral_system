# from django.contrib.auth import authenticate, login, logout
# from django.shortcuts import render, redirect
#
# from .forms import UserRegisterForm, UserProfileForm, CodeForm
# from .models import CustomUser
# from referral.models import ReferralUser
#
#
# def index(request):
#     if request.user.is_authenticated:
#         return redirect('app_auth:profile')
#     else:
#         return render(request, 'app_auth/index.html')
#
#
# def register_view(request):
#     form = UserRegisterForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         phone_number = form.cleaned_data['phone_number']
#         user, created = CustomUser.objects.get_or_create(phone_number=phone_number)
#         login(request, user, backend='app_auth.backends.UserModelBackend')
#         return redirect('app_auth:verified')
#     return render(request, 'app_auth/register.html', {'form': form})
#
#
# def verified_view(request):
#     form = CodeForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         user = request.user
#         password = form.cleaned_data['password_phone']
#         if str(password) == user.password_phone:
#             login(request, user, backend='app_auth.backends.UserModelBackend')
#             return redirect('app_auth:profile')
#         else:
#             return redirect('app_auth:index')
#     return render(request, 'app_auth/verified.html', {'form': form})
#
#
# def profile_view(request):
#     form = UserProfileForm(request.POST or None)
#     user = request.user
#     referred = user.referred.select_related('he_invited_me').first()
#     referrer = user.referrer.select_related('i_invited').filter(he_invited_me=request.user).order_by('id')
#     context = {'form': form, 'referrer': referrer, 'he_invited_me': referred}
#     return render(request, 'app_auth/profile.html', context)
#
#
# def invite_referral(request):
#     form = UserProfileForm(request.POST)
#     if request.method == 'POST' and form.is_valid():
#         invite_code = form.cleaned_data['invite_code']
#         referrer_user = CustomUser.objects.filter(invite_code=invite_code).first()
#         my_referrer = request.user
#         if referrer_user and referrer_user != my_referrer:
#             ReferralUser.objects.get_or_create(i_invited=my_referrer, he_invited_me=referrer_user)
#     return redirect('app_auth:profile')
#
#
# def user_logout(request):
#     logout(request)
#     return redirect('app_auth:index')

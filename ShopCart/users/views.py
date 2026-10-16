from django.shortcuts import render,redirect
from django.contrib.auth import login
from .forms import RegisterForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache

def signup(request):
    if request.user.is_authenticated: return redirect('home')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(); login(request,user); return redirect('cart')
    return render(request,'registration/signup.html',{'form':form})

@never_cache
@require_POST
def session_activity(request):
    """Keep an authenticated session alive when the user is active."""
    if not request.user.is_authenticated:
        return JsonResponse({"authenticated": False}, status=401)
    return JsonResponse({"authenticated": True})


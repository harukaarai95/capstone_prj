# from django.shortcuts import render

# from django.http import HttpResponse
# from django.template import loader
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'index.html')

@login_required
def staff_home(request):
    if request.user.role != 'CUSTOMER':
        return render(request, 'staff.html')
    else:
        return redirect('home')
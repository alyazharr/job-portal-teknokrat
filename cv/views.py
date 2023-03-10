from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from jobseeker.models import CV

# Create your views here.

@login_required(login_url='/login/')
def profile(request):
    user = request.user
    cv = CV.objects.get(users_id=user.id)
    context = {
        'cv': cv
    }
    return render(request, 'profile.html', context)
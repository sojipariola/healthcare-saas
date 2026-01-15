from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def billing_dashboard(request):
    return render(request, "billing/dashboard.html")

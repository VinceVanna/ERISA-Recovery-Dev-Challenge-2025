from django.shortcuts import render
from django.http import HttpResponse
from .models import ClaimList

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def hello(request):
    return HttpResponse("<p>Hello from HTMX!</p>")

def load_claim_list(request):
    get_all_claims = ClaimList.objects.all()
    return render(request, 'core/claim_list_page/claim_list_table.html', {'claims': get_all_claims})

def display_claim_list(request):
    return render(request, 'core/claim_list_page/claim_list_page.html')
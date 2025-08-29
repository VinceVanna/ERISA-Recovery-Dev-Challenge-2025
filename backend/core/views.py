from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ClaimList, ClaimDetail

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

def load_claim_detail(request):
    get_all_claim_detail = ClaimDetail.objects.all()
    return render(request, 'core/claim_list_page/claim_detail_table.html', {'claim_detail': get_all_claim_detail})

def display_claim_detail(request):
    return render(request, 'core/claim_list_page/claim_detail.html')

def search_claim_detail(request, claim_id):
    get_detail = get_object_or_404(ClaimDetail, claim_id__id=claim_id)
    return render(request, 'core/claim_list_page/claim_detail_tab.html', {'detail': get_detail})
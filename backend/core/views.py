from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import ClaimList, ClaimDetail, Employee
from django.db.models import Q
from django.contrib.auth.hashers import check_password, make_password

# Create your views here.
def load_claim_list(request):
    query = request.GET.get('search','')
    get_all_claims = ClaimList.objects.filter(
        Q(id__icontains=query) | Q(patient_name__icontains=query)
    )
    return render(request, 'core/claim_list_page/claim_list_table.html', {'claims': get_all_claims})

def display_claim_list(request):
    return render(request, 'core/claim_list_page/claim_list_page.html')

def load_claim_detail(request):
    get_all_claim_detail = ClaimDetail.objects.all()
    return render(request, 'core/claim_list_page/claim_detail_table.html', {'claim_detail': get_all_claim_detail})

def display_claim_detail(request):
    return render(request, 'core/claim_list_page/claim_detail.html')

def search_claim_detail(request, claim_id):
    get_claim = get_object_or_404(ClaimList, id=claim_id)
    get_detail = get_object_or_404(ClaimDetail, claim_id__id=claim_id)
    context = {
        'claim': get_claim,
        'detail': get_detail
    }
    return render(request, 'core/claim_list_page/claim_detail_tab.html', context)

def load_navbar(request):
    return render(request, 'core/navbar.html')

def load_login_card(request):
    return render(request, 'core/login_page/login_card.html')

def login_page(request):
    return render(request, 'core/login_page/login_page.html')

def load_register_card(request):
    return render(request, 'core/register_page/register_card.html')

def register_page(request):
    return render(request, 'core/register_page/register_page.html')

def employee_login(request):
    if request == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            employee = Employee.objects.get(username=username)

            if check_password(password, employee.password):
                request.session['employee_id'] = employee.id
                return HttpResponse('<script>window.location.href="/claim_list/";</script>')
            else:
                return HttpResponse("Invalid Password", status=401)
        except Employee.DoesNotExist:
            return HttpResponse("Employee Not found or wrong username or password", status=401)
    return login_page(request)

def create_employee(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        employee_type = request.POST.get("employee_type")

        if Employee.objects.filter(employee_username=username).exists():
            return HttpResponse("Username already exists, please choose a different username", status=400)
        
        Employee.objects.create(
            employee_username=username,
            employee_password=make_password(password),
            employee_first_name=first_name,
            employee_last_name=last_name,
            employee_type=employee_type
        )
        return HttpResponse('<div class="text-green-600 font-semibold">New User Created!</div>')
    return register_page(request)

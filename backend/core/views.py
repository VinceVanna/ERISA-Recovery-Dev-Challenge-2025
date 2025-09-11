from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import ClaimList, ClaimDetail, Employee, Flag, Annotation
from django.db.models import Q
from django.contrib.auth.hashers import check_password, make_password

# Create your views here.
def load_claim_list(request):
    employee_id = request.session.get('employee_id')
    query = request.GET.get('search','')
    get_all_claims = ClaimList.objects.filter(
        Q(id__icontains=query) | Q(patient_name__icontains=query)
    )

    get_all_flagged = set(
        Flag.objects.filter(employee_id=employee_id).values_list('claim_id', flat=True)
    )

    return render(request, 'core/claim_list_page/claim_list_table.html', {'claims': get_all_claims, 'flagged': get_all_flagged})

def display_claim_list(request):
    employee_id = request.session.get('employee_id')
    return render(request, 'core/claim_list_page/claim_list_page.html', {'employee_id': employee_id})

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
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            employee = Employee.objects.get(employee_username=username)

            if check_password(password, employee.employee_password):
                request.session['employee_id'] = employee.id
                request.session['employee_type'] = employee.employee_type
                response = HttpResponse()
                response['HX-Redirect'] = '/claim_list/'
                return response
            else:
                return HttpResponse("Invalid Password")
        except Employee.DoesNotExist:
            return HttpResponse("Employee Not found or wrong username or password")
    return load_claim_list(request)

def employee_logout(request):
    if 'employee_id' in request.session:
        del request.session['employee_id']
        del request.session['employee_type']
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


def toggle_flag(request, claim_id):
    employee_id = request.session.get('employee_id')

    if not employee_id:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    try:
        employee = Employee.objects.get(id=employee_id)
        claim = ClaimList.objects.get(id=claim_id)
    except Employee.DoesNotExist:
        return JsonResponse({'error': 'Employee not found'}, status=404)
    except ClaimList.DoesNotExist:
        return JsonResponse({'error': 'Claim not found'}, status=404)

    flag, created = Flag.objects.get_or_create(claim_id=claim, employee_id=employee)
    if not created:
        flag.delete()
        return JsonResponse({'flagged': False})
    return JsonResponse({'flagged': True})

def save_annotation(request):
    claim_id = request.POST.get("selectedClaimID")
    employee_id = request.POST.get("selectedEmployeeID")
    content=request.POST.get("annotationContent")

    print(f"{claim_id} {employee_id} {content}")

    try:
        claim = ClaimList.objects.get(id=claim_id)
        employee = Employee.objects.get(id=employee_id)
    except ClaimList.DoesNotExist:
        return JsonResponse({"error": "Claim not found"}, status=404)
    except Employee.DoesNotExist:
        return JsonResponse({"error": "Employee not found"}, status=404)


    annotation, created = Annotation.objects.update_or_create(
        claim_id=claim,
        employee_id = employee,
        defaults={
            "content": content
        }
    )

    return JsonResponse({"success": True, "action": "updated"})

def get_annotation(request, claim_id):
    employee_id = request.session.get('employee_id')

    try:
        annotation = Annotation.objects.get(claim_id=claim_id, employee_id=employee_id)
        return JsonResponse({'annotation': annotation.content})
    except Annotation.DoesNotExist:
        return JsonResponse({'annotation': ""})


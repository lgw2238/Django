from django.shortcuts import render, redirect
from .models import *
from sendEmail.views import *
from random import *
import hashlib



# main views.py


# Create your views here.
def index(request):
    if 'user_name' in request.session.keys():
        return render(request, 'main/index.html')
    else :
        return redirect('main/signin')

def signup(request):
    return render(request, 'main/signup.html')

def signin(request):
    return render(request, 'main/signin.html')

def verifyCode(request):
    return render(request, 'main/verifyCode.html')

def verify(request):
    return redirect('main_index')

def result(request):
    if 'user_name' in request.session.keys():
        content = {}
        content['grade_calculate_dic'] = request.session['grade_calculate_dic']
        content['email_domain_dic'] = request.session['email_domain_dic']
        del request.session['grade_calculate_dic']
        del request.session['email_domain_dic']
        return render(request, 'main/result.html', content)
    else:
        return redirect('main_signin')
    #return render(request, 'main/reuslt.html')


# 정보를 받아오면 인증하는 곳으로 보내줘야함
def join(request):
    #print(request)  # cmd 창에서 확인 <WSGIRequest: POST '/signup/join'>
    name = request.POST['signupName']
    email = request.POST['signupEmail']
    pw = request.POST['signupPW']


    # pw 암호화 (SHA256)
    encode_pw = pw.encode()
    encrypted_pw = hashlib.sha256(encode_pw).hexdigest()
    #print('encrypted_pw', encrypted_pw)
    
    #회원 등록
    user = User(user_name=name, user_email=email, user_password=encrypted_pw)
    user.save()

    # 인증 코드 생성 - 4자리 정수로 생성 - 랜덤
    # randint(시작번호, 끝번호)
    code = randint(1000, 9999)

    # 생성된 번호를 쿠키에 저장
    response = redirect('main_verifyCode')
    # 저장 + 주소 지정
    # set_cookie는 반드시 이름이 있어야함 - 이름 : code
    response.set_cookie('code', code)
    response.set_cookie('user_id', user.id)

    # 인증 코드 - 이메일로 전송
    send_result = send(email, code)
    if send_result:
        return response
    else:
        return HttpResponse('이메일 발송에 실패했습니다.')



    # return redirect('main_verifyCode')
    # return response


def verify(request):
    user_code = request.POST['verifyCode']
    cookie_code = request.COOKIES.get('code')
    #print(user_code, cookie_code)

    if user_code == cookie_code:
        user = User.objects.get(id=request.COOKIES.get('user_id'))
        user.user_validate = 1
        user.save()
        response = redirect('main_index')
        response.delete_cookie('code')
        response.delete_cookie('user_id')
        #response.set_cookie('user', user)
        request.session['user_emial'] = user.user_email
        request.session['user_name'] = user.user_name

        return response
    else:
        redirect('main_verifyCode')

def logout(request):
    del request.session['user_email']
    del request.session['user_name']
    return redirect('main_signin')

def login(request):
    loginEmail = request.POST['loginEmail']
    loginPw = request.POST['loginPW']
    
    # 회원등록여부 체크
    try:
        user = User.objects.get(user_email=loginEmail)
    except Exception as e:
        print('e : ', e)
        return redirect('main_loginFail')

    encode_pw = loginPw.encode()
    encrypted_pw = hashlib.sha256(encode_pw).hexdigest()


    # 비밀번호 일치 여부 (암호화 된 비밀번호)
    if user.user_password == encrypted_pw:
        request.session['user_name'] = user.user_name
        request.session['user_email'] = user.user_email
        return redirect('main_index')
    else:
        return redirect('main_loginFail')

def loginFail(request):
    return render(request, 'main/loginFail.html')
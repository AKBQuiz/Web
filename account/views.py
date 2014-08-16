from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def info(request):
    profile = request.user.get_profile()
    return render_to_response('profile.html',profile);


@login_required
def editinfo(request):
    return HttpResponse();

def login(request):
    from account.forms import LoginForm
    from django.contrib.auth.views import login as login_
    return login_(request=request,template_name = 'login.html',authentication_form=LoginForm)
    pass

def register(request):
    from account.forms import UserRegForm
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse('userinfo'))
    else:
        form = UserRegForm()
    return render_to_response("register.html", {'form': form,} ,context_instance = RequestContext(request))

def password_reset_confirm(request,uidb36,token):
    from account.forms import PasswordSetForm
    from django.contrib.auth.views import password_reset_confirm as _password_reset_confirm
    return _password_reset_confirm(request=request, uidb36=uidb36, token=token,
                           template_name='password-reset-confirm.html',
                           set_password_form=PasswordSetForm,)
    pass

def password_change(request):
    from account.forms import PasswordChangeForm
    from django.contrib.auth.views import password_change as _password_change
    return _password_change(request = request,template_name = 'password-change.html', password_change_form = PasswordChangeForm)
    pass

def sns_signin(request,sns):
    if sns == 'weibo':
        from TaskManager.weibo import APIError, APIClient
        client = APIClient()
        return HttpResponseRedirect(client.get_authorize_url())
    elif sns == 'qq':
        from TaskManager.qq import APIError, APIClient
        client = APIClient()
        return HttpResponseRedirect(client.get_authorize_url())
    elif sns == 'renren':
        from TaskManager.renren import APIError, APIClient
        client = APIClient()
        return HttpResponseRedirect(client.get_authorize_url())
    else:
        return HttpResponseRedirect(reverse('sns_notsupport'))

    pass

def sns_callback(request,sns):
    from account.models import UserProfile
    from account.utils import create_user, login_by_profile
    # get user info from sns site
    if sns == 'weibo':
        from TaskManager.weibo import APIError, APIClient

        code = request.GET.get('code')
        client = APIClient()
        tokendict = client.request_access_token(code)
        client.set_access_token(tokendict.access_token, tokendict.expires_in)

        sns_user = client.users.show.get(uid = tokendict.uid)

        userinfo = dict(
            uid = sns_user.id, \
            domain = sns_user.domain, \
            name = sns_user.name, \
            nickname = sns_user.screen_name, \
            avatar_url = sns_user.avatar_large or sns_user.profile_image_url, \
            homepage = 'http://weibo.com/%s' % sns_user.domain, \
            auth_token = tokendict.access_token, \
            expired_time = tokendict.expires_in)

        try:
            userProfile = UserProfile.objects.get(weibo_id = tokendict.uid)
        except UserProfile.DoesNotExist:
            content = create_user(request, userinfo, sns)
            return render_to_response("snsreg-success.html", content,context_instance = RequestContext(request))

        login_by_profile(request,userProfile)
        return HttpResponseRedirect(reverse('userinfo'))

    elif sns == 'qq':
        from TaskManager.qq import APIError, APIClient
        code = request.GET.get('code')
        client = APIClient()
        tokendict = client.request_access_token(code)
        r = client.request_openid(tokendict.access_token)
        tokendict.uid = r.openid
        client.set_access_token(tokendict.access_token, tokendict.uid, tokendict.expires_in)

        sns_user = client.user.get_info.get(openid = tokendict.uid)
        sns_user = sns_user.data

        userinfo = dict(
            uid = sns_user.openid , \
            name = sns_user.name, \
            nickname = sns_user.nick, \
            avatar_url = '%s/100'% (sns_user.head), \
            homepage = sns_user.homepage, \
            auth_token = tokendict.access_token, \
            expired_time = tokendict.expires_in)

        try:
            userProfile = UserProfile.objects.get(qq_id = tokendict.uid)
        except UserProfile.DoesNotExist:
            content = create_user(request, userinfo, sns)
            return render_to_response("snsreg-success.html", content, context_instance = RequestContext(request))

        login_by_profile(request, userProfile)
        return HttpResponseRedirect(reverse('userinfo'))

    elif sns == 'renren':
        from TaskManager.renren import APIError, APIClient
        from account.utils import multi_get_letter

        code = request.GET.get('code')
        client = APIClient()
        tokendict = client.request_access_token(code)
        sns_user = tokendict.user

        for avatar in sns_user.avatar:
            if avatar['type'] == 'large':
                avatar_url = avatar['url']
                break;
                pass
            pass
        userinfo = dict(
            uid = sns_user.id , \
            name = multi_get_letter(sns_user.name), \
            nickname = sns_user.name, \
            avatar_url = avatar_url, \
            homepage = 'http://www.renren.com', \
            auth_token = tokendict.access_token, \
            expired_time = tokendict.expires_in)

        try:
            userProfile = UserProfile.objects.get(renren_id = sns_user.id)
        except UserProfile.DoesNotExist:
            content = create_user(request, userinfo, sns)
            return render_to_response("snsreg-success.html", content,context_instance = RequestContext(request))

        login_by_profile(request, userProfile)
        return HttpResponseRedirect(reverse('userinfo'))
    else:
        return HttpResponseRedirect(reverse('sns_notsupport'))

    pass

def snsreg_success(request):
    content = {
        'username': 'CuGBabyBeaR-test', \
        'password': 'a-password-not-exist', \
        'snsname':'weibo', \
        'avatar_url':'http://tp4.sinaimg.cn/1450372003/180/5621738859/1', \
        'sns_url': 'http://weibo.com/%s' % 'duoz', \
        'snsusername':'CuGBabyBeaR', \
    }
    return render_to_response("snsreg-success.html", content,context_instance = RequestContext(request))

def sns_notsupport(request):
    return render_to_response("sns-notsupport.html", context_instance = RequestContext(request))
    pass



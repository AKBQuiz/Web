def unique_username_creater(username):
    import re
    import random
    from django.utils.encoding import smart_unicode
    from django.contrib.auth.models import User
    # Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters
    regex = re.compile(r'[^\w.@+-]')
    username = smart_unicode(username)
    username = regex.sub('_',username)
    if len(username) < 3:
        username = username + '%s' % random.randint(100,999);
        pass
    is_duplicate = True
    while is_duplicate:
        try:
            user = User.objects.get(username = username);
        except User.DoesNotExist:
            is_duplicate = False;
            return username
        unique_num = random.randint(0,9);
        username = '%s%s' % (username,unique_num);
        pass
    return username

def password_creater(n):
    import random
    import string
    return ''.join(random.sample( string.ascii_lowercase + string.digits , n));

def login_by_profile(request, userProfile):
    from django.contrib.auth import login as login_ 
    user = userProfile.user
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login_(request, user)
    pass

def create_user(request, userinfo,sns):
    import json
    from django.contrib.auth import login as login_ 
    from django.contrib.auth.models import User
    from django.utils.translation import ugettext as _
    
    # create user
    username = unique_username_creater(userinfo['name'])
    password = password_creater(8)
    user = User.objects.create(username = username)
    user.set_password(password)
    user.save()

    # setprofile
    profile = user.get_profile()
    profile.display_name = userinfo['nickname']
    profile.avatar = userinfo['avatar_url']
    if sns == 'weibo':
        snsname = _('Weibo')
        profile.weibo_id = userinfo['uid']
        profile.weibo_info = json.dumps(userinfo)
    elif sns == 'qq':
        snsname = _('QQ')
        profile.qq_id = userinfo['uid']
        profile.qq_info = json.dumps(userinfo)
    elif sns == 'renren':
        snsname = _('RenRen')
        profile.renren_id = userinfo['uid']
        profile.renren_info = json.dumps(userinfo)
        pass
    profile.save()

    # login and response
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login_(request, user)

    return {
                'username': username, \
                'password': password, \
                'snsname': snsname, \
                'avatar_url':userinfo['avatar_url'], \
                'sns_url':userinfo['homepage'], \
                'snsusername':userinfo['name'], \
            }
    pass

def multi_get_letter(str_input, uppercase = False): 
     
    if isinstance(str_input, unicode): 
        unicode_str = str_input 
    else: 
        try: 
            unicode_str = str_input.decode('utf8') 
        except: 
            try: 
                unicode_str = str_input.decode('gbk') 
            except: 
                print 'unknown coding' 
                return 
     
    return_list = [] 
    for one_unicode in unicode_str: 
        return_list.append(get_letter(one_unicode))
    res = ''.join(return_list)
    if uppercase:
        res = res.upper()
        pass
    return res 
 
def get_letter(unicode1): 
    str1 = unicode1.encode('gbk') 
    try:         
        ord(str1) 
        return str1 
    except: 
        asc = ord(str1[0]) * 256 + ord(str1[1]) - 65536 
        if -20319 <= asc <= -20284: 
            return 'a' 
        if -20283 <= asc <= -19776: 
            return 'b' 
        if -19775 <= asc <= -19219: 
            return 'c' 
        if -19218 <= asc <= -18711: 
            return 'd' 
        if -18710 <= asc <= -18527: 
            return 'e' 
        if -18526 <= asc <= -18240: 
            return 'f' 
        if -18239 <= asc <= -17923: 
            return 'g' 
        if -17922 <= asc <= -17418: 
            return 'h' 
        if -17417 <= asc <= -16475: 
            return 'j' 
        if -16474 <= asc <= -16213: 
            return 'k' 
        if -16212 <= asc <= -15641: 
            return 'l' 
        if -15640 <= asc <= -15166: 
            return 'm' 
        if -15165 <= asc <= -14923: 
            return 'n' 
        if -14922 <= asc <= -14915: 
            return 'o' 
        if -14914 <= asc <= -14631: 
            return 'p' 
        if -14630 <= asc <= -14150: 
            return 'q' 
        if -14149 <= asc <= -14091: 
            return 'r' 
        if -14090 <= asc <= -13119: 
            return 's' 
        if -13118 <= asc <= -12839: 
            return 't' 
        if -12838 <= asc <= -12557: 
            return 'w' 
        if -12556 <= asc <= -11848: 
            return 'x' 
        if -11847 <= asc <= -11056: 
            return 'y' 
        if -11055 <= asc <= -10247: 
            return 'z' 
        return '' 
    
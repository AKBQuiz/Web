from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext

@csrf_exempt
def quizgame(request):
    return render_to_response('quizgame.html', {"nav_active":0}, context_instance = RequestContext(request))

def collect(request):
    return render_to_response('collect.html', {"nav_active":0}, context_instance = RequestContext(request))

def query(request):
    return render_to_response('query.html')
# APIs
def api_quiz_get(request):
    if request.method == "GET":
        from quiz.getter import QuizGetter
        g = QuizGetter()
        g.requestHandler(request.GET)
        return HttpResponse(g.getQuizStr(), mimetype = g.getMimetype())

@csrf_exempt
def api_quiz_submit(request):
    if request.method == 'POST':
        import json
        quiz =json.loads(request.raw_post_data)
        author = quiz.get('author',None)
        difficulty = quiz.get('difficulty',0)
        question = quiz.get('question',None)
        answer = quiz.get('answer',None)
        wrong = quiz.get('wrong',None)
        group = quiz.get('group',None)

        if not author:
            return HttpResponse('error: missing author info')
        elif not 2 <= len(author) < 32:
            return HttpResponse('error: incorrect author name length')

        if not 0 <= difficulty <= 5:
            return HttpResponse('error: difficulty not allowed')

        if not question:
            return HttpResponse('error: missing question content')
        elif not 7 <= len(question) <= 200:
            return HttpResponse('error: incorrect question content length')
            pass

        if not answer:
            return HttpResponse('error: missing answer content')
        elif not 2 <= len(answer) <= 50:
            return HttpResponse('error: incorrect answer content length')
            pass

        if not wrong:
            return HttpResponse('error: missing alternative content')
        else:
            for i in wrong:
                if not i:
                    return HttpResponse('error: missing alternative content')
                elif not 2 <= len(i) < 50:
                    return HttpResponse('error: incorrect alternative content length')
                    pass

        from memberinfo.models import Group
        groups = []
        for i,f in enumerate(group):
            if f:
                g = None
                if i == 0:
                    g = Group.objects.get(groupname = 'AKB48')
                elif i == 1:
                    g = Group.objects.get(groupname = 'SKE48')
                elif i == 2:
                    g = Group.objects.get(groupname = 'NMB48')
                elif i == 3:
                    g = Group.objects.get(groupname = 'HKT48')
                elif i == 4:
                    g = Group.objects.get(groupname = 'NGZK46')
                elif i == 5:
                    g = Group.objects.get(groupname = 'SDN48')
                elif i == 6:
                    g = Group.objects.get(groupname = 'JKT48')
                elif i == 7:
                    g = Group.objects.get(groupname = 'SNH48')
                    pass
                if g:
                    groups.append(g)
                    pass
                pass
            pass
        if len(groups) < 1:
            return HttpResponse('error: missing correlation groups')
            pass

        if quiz.get('istest', False):
            return HttpResponse('test pass! {author: %s, difficulty: %s, correlation: %s, question: %s, answer: %s, alternative: %s }' %
                (author, difficulty, groups, question, answer, wrong))

        from quiz.models import Quiz
        q = Quiz.objects.create(
            author_text = author,
            question = question,
            answer = answer,
            wrong_1 = wrong[0],
            wrong_2 = wrong[1],
            wrong_3 = wrong[2],
            difficulty = difficulty,
            state = 0)
        for g in groups:
            q.correlation.add(g)
            pass
        q.save()

        return HttpResponse('success')

    else:
        return HttpResponse('error: use post please')

    from quiz.models import Quiz
    pass

def api_quiz_comment(request):
    return HttpResponse('success')
    pass

def api_member_info(request):
    pass

def api_member_birthday(request):
    pass

def api_member_age(request):
    pass

def api_member_gen(request):
    pass

def api_team_list(request):
    pass

def api_team_member(request):
    pass

def api_single_list(request):
    pass

def api_single_info(request):
    pass

def api_single_member(request):
    pass




from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .models import QuestionSub, AnswerSub, Question, Subscore
from django.http import HttpResponseRedirect
from . import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from mcq.models import Mcqscore
listofuserobject = {}
count = models.QuestionSub.objects.all().count()
c = 1
ques_list2 = []
ques_list = QuestionSub.objects.all()
list1 = {}
list3 = {}
list4 = {}
users = User.objects.all()
list2 = []
onetime = 0


def createobject():

    if not len(Subscore.objects.all()):
        listtemp = Subscore.objects.all()
        listofuserobject.clear()
        for j in listtemp:
            listofuserobject.update({j.usersub: j.subscore})
        for i in users:
            obh = Mcqscore()
            obj = Subscore()
            obh.user = obj.user = i
            obh.usermcq = obj.usersub = i.username
            obj.subscore = obh.mcqscore = 0
            obh.save()
            obj.save()
            listofuserobject.update({obj.usersub: obj.subscore})
    else:
        listtemp = Subscore.objects.all()
        listofuserobject.clear()
        for j in listtemp:
            listofuserobject.update({j.usersub: j.subscore})

        for i in users:
            if i.username not in listofuserobject.keys():
                print(i.username)
                obh = Mcqscore()
                obj = Subscore()
                obh.user = obj.user = i
                obh.usermcq = obj.usersub = i.username
                obj.subscore = obh.mcqscore = 0
                obh.save()
                obj.save()
                listofuserobject.update({obj.usersub: obj.subscore})


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = QuestionSub
    template_name = 'subjective/detail.html'




def first(request):
    ques_list = QuestionSub.objects.all()
    import random
    hh=len(ques_list)
    data = list(range(0, hh))
    random.shuffle(data)
    k=0
    for i in ques_list:
        ques_list2.append(ques_list[data[k]])
        k += 1
    return HttpResponseRedirect(reverse('subjective:detail', args=(ques_list2[0].id,)))


def ques_ans(request, ques_id):

    kl=0
    for i in ques_list2:
        kl+=1
        j = request.user
        if i in list1.keys() and j == list1[i]:
            continue
        else:
            if request.method == "POST":
                choice = request.POST['answer']
                ans = AnswerSub()
                ans.user = request.user
                ans.ans_text = choice
                ans.user_ans =u= request.user
                ans.question = i
                ans.is_attempted += 1
                print(list1)
                if ques_id in list3.keys() and u == list3[ques_id]:
                    print("d")
                    kl-=1
                    #return HttpResponseRedirect(reverse('subjective:detail', args=(ques_list2[kl].id,)))
                else:
                    list1[i] = j
                    if j not in list4.keys():
                        list4[j] = 1
                    else:
                        list4[j] +=1
                    ans.save()
                    j = request.user
                    print(j)
                    list3[ques_id]=j


                if list4[j] < len(ques_list):
                    return HttpResponseRedirect(reverse('subjective:detail', args=(ques_list2[kl].id,)))
        a = AnswerSub.objects.filter(user_ans=ans.user_ans)
        return render(request, 'quizover.html', {'a': a})



def checksubanswer(request):
    users = User.objects.all()
    return render(request, 'subjective/checksubanswer.html', {'user' : users })


def displayans(request, uas):
    answer1 = AnswerSub.objects.filter(user_ans=uas)
    return render(request,'subjective/usersubanswer.html',{'answer' : answer1,'uas':uas })

def updatemarks(request,answer):
        ans = AnswerSub.objects.get(pk=answer)
        if ans in list2:
            None
        else:
            list2.append(ans)
            if request.method == 'GET':
                mq = request.GET['marks']
            for i in listofuserobject:
                if i == ans.user_ans:
                    listofuserobject[i]+=int(mq)
                    kkk = Subscore.objects.get(usersub=i)
                    ans.answermarks=int(mq)
                    ans.save()
                    kkk.subscore=listofuserobject[i]
                    kkk.save()
        return render(request, 'subjective/checksubanswer.html', {'user' : users })


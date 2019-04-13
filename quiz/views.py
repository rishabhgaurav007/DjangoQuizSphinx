import random

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render,render_to_response
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import FormView
from .forms import QuestionForm
from .models import Quiz, Category,Sitting,Question,UserProgress
from subjective.models import Subscore
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from subjective.models import QuestionSub, AnswerSub ,Subscore
from mcq.models import Mcqscore
from django.http import HttpResponseRedirect, HttpResponse
from subjective import models

from django.urls import reverse_lazy, reverse
from mcq.models import Mcqscore

a = UserProgress()

def index(request):
    return render(request, 'index.html', {})


class QuizListView(ListView):
    model = Quiz

    def get_queryset(self):
        queryset = super(QuizListView, self).get_queryset()
        return queryset.filter(draft=False)


class CategoriesListView(ListView):
    model = Category


class ViewQuizListByCategory(ListView):
    model = Quiz
    template_name = 'view_quiz_category.html'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            category=self.kwargs['category_name']
        )

        return super(ViewQuizListByCategory, self).\
            dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewQuizListByCategory, self)\
            .get_context_data(**kwargs)

        context['category'] = self.category
        return context

    def get_queryset(self):
        queryset = super(ViewQuizListByCategory, self).get_queryset()
        return queryset.filter(category=self.category, draft=False)


class QuizTake(FormView):
    form_class = QuestionForm
    template_name = 'question.html'

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, url=self.kwargs['quiz_name'])
        if self.quiz.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        self.logged_in_user = self.request.user.is_authenticated

        if self.logged_in_user:
            self.sitting = Sitting.objects.user_sitting(request.user,
                                                        self.quiz)
        if self.sitting is False:
            return render(request, 'single_complete.html')

        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=QuestionForm):
        if self.logged_in_user:
            self.question = self.sitting.get_first_question()
            self.progress = self.sitting.progress()
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        if self.logged_in_user:
            self.form_valid_user(form)
            if self.sitting.get_first_question() is False:
                return self.final_result_user()
        self.request.POST = {}

        return super(QuizTake, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['quiz'] = self.quiz
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
        if hasattr(self, 'progress'):
            context['progress'] = self.progress
        return context

    def form_valid_user(self, form):
        #progress, c = Progress.objects.get_or_create(user=self.request.user)
        guess = form.cleaned_data['answers']
        is_correct = self.question.check_if_correct(guess)

        if is_correct is True:
            self.sitting.add_to_score(1, self.question)
            #progress.update_score(self.question, 1, 1)
        else:
            self.sitting.add_incorrect_question(self.question)
           # progress.update_score(self.question, 0, 1)

        if self.quiz.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_question': self.question,
                             'answers': self.question.get_answers(),
                             'question_type': {self.question
                                               .__class__.__name__: True}}
        else:
            self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

    def final_result_user(self):
        results = {
            'quiz': self.quiz,
            'score': self.sitting.get_current_score,
            'max_score': self.sitting.get_max_score,
            'percent': self.sitting.get_percent_correct,
            'sitting': self.sitting,
            'previous': self.previous,
        }

        self.sitting.mark_quiz_complete()

        if self.quiz.answers_at_end:
            results['questions'] =\
                self.sitting.get_questions(with_answers=True)
            results['incorrect_questions'] =\
                self.sitting.get_incorrect_questions

        if self.quiz.exam_paper is False:
            self.sitting.delete()

        return render(self.request, 'result.html', results)


@login_required
def ProgressView(request):
    from subjective.views import createobject
    createobject()
    curr_user = request.user
    marks = 0
    if len(Subscore.objects.all()):
        try:
            a2 = Subscore.objects.get(user=curr_user)
            if a2:
                marks += a2.subscore
        except:
            a2 = Subscore()
            a2.user = request.user
            a2.usersub = request.user
            a2.subscore = 0
            a2.save()
            marks += a2.subscore


    if len(Mcqscore.objects.all()):
        try:
            a1 = Mcqscore.objects.get(user=curr_user)
            if a1:
                marks += a1.mcqscore
        except:
            a1 = Mcqscore()
            a1.user=request.user
            a1.usermcq=request.user
            a1.mcqscore = 0
            a1.save()
            marks += a1.mcqscore
    return render(request, 'progress.html', {"user": request.user, "marks":marks})

def LeaderBoard(request):
    from subjective.views import createobject
    createobject()
    rank = Subscore.objects.all()
    obj = Mcqscore.objects.all()

    kj=0
    print(obj)
    if len(rank)>0:
        for i in rank:
            print("j")

            for j in obj:
                if j.usermcq == i.usersub:
                    print(rank[kj].subscore)
                    rank[kj].subscore += j.mcqscore
                    print(rank[kj].subscore)
            kj+=1
        newlist = sorted(rank, key=lambda x: x.subscore, reverse=True)
    elif len(obj)>0:
        for i in obj:
            print("j")
            for j in rank:
                if j.usersub == i.usermcq:
                    #print(rank[kj].subscore)
                    obj[kj].mcqscore += j.subscore
                    #print(rank[kj].subscore)
            kj += 1
        newlist = sorted(obj, key=lambda x: x.mcqscore, reverse=True)

    # To return a new list, use the sorted() built-in function...
    if (len(obj)==0 and len(rank)==0):
        return render(request, 'leaderboard1.html')
    print(newlist)
    return render(request,'leaderboard.html', {'newlist':newlist})

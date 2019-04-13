from django.db import models
from django.urls import reverse
from quiz.models import Question
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import User



# Create your models here.



class QuestionSub(Question):

    def check_if_correct(self, guess):
        return False

    def get_answers(self):
        return False

    def get_answers_list(self):
        return False

    def answer_choice_to_string(self, guess):
        return str(guess)

    def get_absolute_url(self):
        return reverse('subjective:detail', kwargs={'pk', self.pk})

    #def __str__(self):
        #return self.content

    '''class Meta:
        verbose_name = "Subjective Question"
        verbose_name_plural = "Subjective Questions"'''




class AnswerSub(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)
    user_ans = models.CharField(verbose_name='userbyans', max_length=2000)
    question = models.ForeignKey(QuestionSub, on_delete=models.CASCADE)
    ans_text = models.CharField(max_length=3000, verbose_name='your answer')
    is_attempted = models.IntegerField(default=1)
    answermarks = models.IntegerField(default=0)

    def __str__(self):
        return self.ans_text


class Subscore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("User"), on_delete=models.CASCADE)
    usersub = models.CharField(verbose_name='usersub', max_length=2000)
    subscore = models.IntegerField(verbose_name='userscore', default=0)

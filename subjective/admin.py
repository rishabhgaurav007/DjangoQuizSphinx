from django.contrib import admin

# Register your models here.
from .models import QuestionSub, AnswerSub, Subscore
admin.site.register(AnswerSub)
admin.site.register(QuestionSub)
admin.site.register(Subscore)
# **Django quiz app**


## **Build Status

This is a configurable quiz app for Django.

**Current features

**Features of each quiz:

Question order randomisation.
Storing of quiz results under each user.
Correct answers can be shown after each question or all at once at the end.
Logged in users can return to an incomplete quiz to finish it and non-logged in users can complete a quiz if their session persists.
The quiz can be limited to one attempt per user.
Questions can be given a category.
Success rate for each category can be monitored on a progress page.(from end underdevelopment)
Explanation for each question result can be given.
Multiple choice question type.
Subjective question type.
Display an image alongside the question.
A marking page which lists completed quizzes, can be filtered by quiz or user, and is used to mark essay questions.
For MCQ type questions and answers in random order for each user.

**requirements 

see requirements.txt in project file

**installations

1.Clone the  repo and download . It will be downloaded in zip format.
2.Activate djenv source
Change your directory to django_projects.
3.$ django-admin startproject Sphinx
4.Go in Sphinx folder that you created and delete all its content.
5.Unzip the repo github and copy all the files inside the DjangoQuizSphinx
6.Paste the copied files and folders to the Sphinx folder that you created.
7.Install from requirements.txt if needed else you are all set to go
7.create a superuser (already created : username= admin , password = Qwerty@123)
8.python manage.py runserver

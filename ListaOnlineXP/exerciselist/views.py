from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from forms import GetCodeForm
from models import ExerciseList
from course.models import Course
from authentication.views import get_student, get_admin

import os.path
from subprocess import Popen, PIPE
import shlex


def get_code(request):
    values = {}
    values.update(csrf(request))
    if request.method == 'GET':
        form = GetCodeForm()
    else:
        form = GetCodeForm(request.POST)
        if form.is_valid():

            code_file = open("/Users/hugo/ListaOnlineXP/ListaOnlineXP/java/Code.java", 'w')
            code_file.write(request.POST['code'])
            code_file.close()

            test_file = open("/Users/hugo/ListaOnlineXP/ListaOnlineXP/java/TestCode.java", 'w')
            test_file.write(request.POST['test'])
            test_file.close()

            path = "/Users/hugo/ListaOnlineXP/ListaOnlineXP/java/"

            test_command = "java -Dfile.encoding=utf-8 -classpath " + path +  " JavaTester  /Users/hugo/ListaOnlineXP/ListaOnlineXP/java/Code.java /Users/hugo/ListaOnlineXP/ListaOnlineXP/java/TestCode.java " + path

            test_args = shlex.split(test_command)

            test = Popen(test_args, stdout=PIPE, stderr=PIPE)
            test_output = test.stdout.read()

            values["test_output"] = test_output
            values["test_command"] = test_command

    values['form'] = form
    return render_to_response('get_code.html', values)
    
def exercise_list(request, course_id, list_id):
    values = {}
    values.update(csrf(request))
    try:
        course = Course.objects.get(id=int(course_id))
        exercise_list = ExerciseList.objects.get(id=int(list_id))
    except:
        raise Http404
    if (exercise_list is not None) and (course is not None):
        if (exercise_list.course == course):
            student = get_student(request)
            admin = get_admin(request)
            course = exercise_list.course
            questions = list(exercise_list.questions.all())
            values['exercise_list'] = exercise_list
            values['questions'] = questions
            values['student'] = student
            if student is not None:
                if course in student.courses.all():
                    return render_to_response('exercise_list.html', values)
                else:
                    return HttpResponseRedirect('/')                
#           elif admin is not None:
#               values['admin'] = admin 
#               values['students'] = course.student_set.all()
#               return render_to_response('teacher_course.html', values)
            else:
                return HttpResponseRedirect('/login')
        else:
            return HttpResponseRedirect('/')   
    raise Http404            
    
    


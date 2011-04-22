from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from forms import GetCodeForm

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


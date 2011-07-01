# -*- coding: utf-8 -*-

import os.path
from subprocess import Popen, PIPE
import shlex

def manage_uploads_filenames(instance, filename):
    exercise_list_id = instance.exercise_list_solution.exercise_list.pk
    group_id = instance.exercise_list_solution.group.pk

    return "uploads" + "/exercise_list_" + str(exercise_list_id) + "/group_" + str(group_id) + "/" + filename

def test_code(test, code):

    path = os.path.dirname(__file__) + "/java/"

    code_file = open(path + "Code.java", 'w')
    code_file.write(code)
    code_file.close()

    test_file = open(path + "TestCode.java", 'w')
    test_file.write(test)
    test_file.close()

    test_command = "java -Dfile.encoding=utf-8 -classpath " + path + "tools.jar:" + path + " JavaTester  " + path + "Code.java " + path + "TestCode.java " + path

    test_args = shlex.split(test_command)

    test = Popen(test_args, stdout=PIPE, stderr=PIPE)
    test_output = test.stdout.read()

    result_code, separator, result_message = test_output.partition("!:!")
    result_message, separator, result_message_remainder = result_message.partition("\n")

        

    if result_code == "CODE_ERROR":
        return False, "Erro no código: " + result_message
    elif result_code == "TEST_ERROR":
        return False, result_message + result_message_remainder
    elif result_code == "CORRECT":
        return True, "Sucesso: " + result_message
    elif result_code == "TESTCODE_ERROR":
        return False, "Erro: " + result_message
    elif result_code == "SYSTEM_ERROR":
        return False, "Erro do sistema: " + result_message
    elif result_code == "UNKNOWN_SYSTEM_ERROR":
        return False, "Erro desconhecido: " + result_message
    else:
        return False, "Erro do sistema: o sistema de testes retornou uma resposta inesperada."

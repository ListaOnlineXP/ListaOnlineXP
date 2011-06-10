# -*- coding: utf-8 -*-

def manage_uploads_filenames(instance, filename):
    exercise_list_id = instance.exercise_list_solution.exercise_list.pk
    group_id = instance.exercise_list_solution.group.pk

    return "uploads" + "/exercise_list_" + str(exercise_list_id) + "/group_" + str(group_id) + "/" + filename

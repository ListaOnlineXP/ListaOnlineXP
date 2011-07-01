# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from authentication.models import Group
from course.models import Course
import datetime
import random

from utilities import manage_uploads_filenames

class ExerciseList(models.Model):
    name = models.CharField(blank=False, max_length=100, verbose_name="titulo")
    course = models.ForeignKey(Course, verbose_name='curso')
    pub_date = models.DateField(default=datetime.datetime.today, verbose_name='data de publicação')
    due_date = models.DateField(default=(datetime.datetime.today() + datetime.timedelta(days=7)), verbose_name='data de entrega')
    questions = models.ManyToManyField('Question', through='ExerciseListQuestionThrough', verbose_name='questões')
    min_number_of_students = models.PositiveIntegerField(verbose_name='número mínimo de alunos', default=1)
    max_number_of_students = models.PositiveIntegerField(verbose_name='número máximo de alunos', default=1)
    create_random_groups = models.BooleanField(verbose_name='criar grupos aleatoriamente', default=True)
    topics = models.ManyToManyField('Topic', blank=True, verbose_name='tópicos')

    def save(self, **kwargs):
        super(ExerciseList, self).save(**kwargs)
        randomize = self.create_random_groups or (self.max_number_of_students==1)
        students = []
        for student in self.course.student.all():
            has_group = Group.objects.filter(solution__exercise_list=self, students=student).count()
            if not has_group:
                students.append(student)
        if randomize:
            random.shuffle(students)
        while students:
            solution = ExerciseListSolution(exercise_list=self, finalized=False)
            solution.save()
            solution.populate_blank()
            solution.save()
            group = Group(solution = solution)
            group.save()
            if randomize:
                for student in students[:self.max_number_of_students]:
                    group.students.add(student)
            group.save()
            students = students[self.max_number_of_students:]

    def get_multiple_choice_questions(self):
        return MultipleChoiceQuestion.objects.filter(exerciselist=self)

    def get_java_questions(self):
        return JavaQuestion.objects.filter(exerciselist=self)

    def get_discursive_questions(self):
        return DiscursiveQuestion.objects.filter(exerciselist=self)

    def mean(self):
        solutions = ExerciseListSolution.objects.filter(exercise_list=self)
        total_score = 0
        for solution in solutions:
            if solution.score is not None:
                total_score += solution.score
        if solutions.count() != 0:
            return total_score/solutions.count()
        else:
            return 0

    def question_mean(self, question):
        solutions = ExerciseListSolution.objects.filter(exercise_list=self)
        answers = [solution.answer_set.get(question_answered=question) for solution in solutions]
        total_score = 0
        for answer in answers:
            if answer.score is not None:
                total_score += answer.score
        if solutions.count() != 0:
            return total_score/solutions.count()
        else:
            return 0

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    
    name = models.CharField(max_length=100, verbose_name='nome')

    def __unicode__(self):
        return self.name


class Topic(models.Model):
    
    name = models.CharField(max_length=100, verbose_name='nome')
    
    def __unicode__(self):
        return self.name


class Question(models.Model):

    text = models.TextField('enunciado')
    QUESTION_TYPE_CHOICES = (
        ('TF', 'True/False'),
        ('DI', 'Discursive'),
        ('JA', 'Java'),
        ('MU', 'Multiple'),
        ('FI', 'File'),
    )

    type = models.CharField(max_length=2, choices=QUESTION_TYPE_CHOICES, blank=True, verbose_name='tipo')
    tags = models.ManyToManyField(Tag, blank=True)

    def __unicode__(self):
        return self.text

    def casted(self):
        """
        Returns the specific kind of question.
        For instance, a Question that is also a
        Multiple Choice Question will return it's
        Multiple Choice Question object once this
        method is called.
        Ex: question = Question.objects.get(pk=1).casted()
        might return a MultipleChoiceQuestion object,
        of a DiscursiveQuestion object, depending
        on what kind of question it actually is.
        """

        try:
            if self.type == 'TF':
                return self.truefalsequestion
            elif self.type == 'DI':
                return self.discursivequestion
            elif self.type == 'JA':
                return self.javaquestion
            elif self.type == 'MU':
                return self.multiplechoicequestion
            elif self.type == 'FI':
                return self.filequestion

        except:
            raise


class ExerciseListSolution(models.Model):

    exercise_list = models.ForeignKey(ExerciseList, verbose_name='lista de exercício')
    finalized = models.BooleanField(False)
    score = models.FloatField(null=True, blank=True, verbose_name='nota')
    chosen_topic = models.OneToOneField(Topic, null=True, blank=True, verbose_name='tópico escolhido')

    def get_answers(self):
        return Answer.objects.filter(exercise_list_solution=self)

    def get_not_corrected_answers(self):
        return Answer.objects.filter(exercise_list_solution=self, score=None)

    def get_group(self):
        return Group.objects.get(solution=self)

    def populate_blank(self, *args, **kargs):
        """
        This will go through the questions in the exercise_list
        associated with this ExerciseListSolution and create
        empty answers to each question that does not exist yet
        """

        questions = self.exercise_list.questions.all()
        for question in questions:
            
            if question.type == 'JA':
                answer, answer_created = JavaAnswer.objects.get_or_create(exercise_list_solution=self, question_answered=question)
            elif question.type == 'DI':
                answer, answer_created = DiscursiveAnswer.objects.get_or_create(exercise_list_solution=self, question_answered=question)
            elif question.type == 'MU':
                answer, answer_created = MultipleChoiceAnswer.objects.get_or_create(exercise_list_solution=self, question_answered=question)
            elif question.type == 'TF':
                answer, answer_created = TrueFalseAnswer.objects.get_or_create(exercise_list_solution=self, question_answered=question)
                for truefalsequestion_item in answer.question_answered.casted().truefalseitem_set.all():
                    truefalseanswer_item, truefalseanswer_item_created = TrueFalseAnswerItem.objects.get_or_create(answer_group=answer, item_answered=truefalsequestion_item)
                    if truefalseanswer_item_created:
                        truefalseanswer_item.given_answer = False
            elif question.type == 'FI':
                answer, answer_created = FileAnswer.objects.get_or_create(exercise_list_solution=self, question_answered=question)

            if answer_created:
                self.answer_set.add(answer)

        self.save()

    # Updates the score of the exercise list solution by correcting each solution
    def correct(self):
        score = 0.0
        max_score = 0
        for answer in self.get_answers():
            weight = ExerciseListQuestionThrough.objects.get(exerciselist=self.exercise_list, question=answer.question_answered).weight
            max_score += 100*weight
            # types with auto correction
            if answer.type == 'MU' or answer.type == 'TF' or answer.type == 'JA':
                casted_answer = answer.casted()
                score += weight * casted_answer.correct()

        self.score = 100*score/max_score
        self.save()

    # Updates de score based on the scores in the answers
    # This function should be used after a custom correction made by a teacher
    def update_score(self):
        score = 0.0
        max_score = 0
        for answer in self.get_answers():
            weight = ExerciseListQuestionThrough.objects.get(exerciselist=self.exercise_list, question=answer.question_answered).weight
            max_score += 100*weight
            if answer.score is not None:
                score += answer.score
        self.score = 100*score/max_score
        self.save()


class Answer(models.Model):

    exercise_list_solution = models.ForeignKey(ExerciseListSolution, editable=False, verbose_name='lista de solução')
    question_answered = models.ForeignKey(Question, editable=False, verbose_name='questão respondida')
    score = models.FloatField(null=True, blank=True, default=None, verbose_name='nota')
    comment = models.TextField(null=True, blank=True, verbose_name='comentário')

    ANSWER_TYPE_CHOICES = (
        ('TF', 'True/False'),
        ('DI', 'Discursive'),
        ('JA', 'Java'),
        ('MU', 'Multiple'),
        ('FI', 'File'),
    )

    type = models.CharField(max_length=2, choices=ANSWER_TYPE_CHOICES, blank=True)


    def casted(self):
        """
        Returns the specific kind of answer.
        For instance, an Answer that is also a
        Multiple Choice Answer will return it's
        Multiple Choice Answer object once this
        method is called.
        Ex: question = Answer.objects.get(pk=1).casted()
        might return a MultipleChoiceAnswer object,
        of a DiscursiveAnswer object, depending
        on what kind of question it actually is.
        """

        try:
            if self.type == 'TF':
                return self.truefalseanswer
            elif self.type == 'DI':
                return self.discursiveanswer
            elif self.type == 'JA':
                return self.javaanswer
            elif self.type == 'MU':
                return self.multiplechoiceanswer
            elif self.type == 'FI':
                return self.fileanswer

        except:
            raise


class DiscursiveQuestion(Question):

    def __init__(self, *args, **kargs):
        super(DiscursiveQuestion, self).__init__(*args, **kargs)
        self.type = 'DI'


class DiscursiveAnswer(Answer):

    text = models.TextField(blank=True, verbose_name='resposta')

    def __init__(self, *args, **kargs):
        super(DiscursiveAnswer, self).__init__(*args, **kargs)
        self.type = 'DI'

    def __unicode__(self):
        return self.text


class JavaQuestion(Question):

    criteria = models.TextField(verbose_name='critério')

    def __init__(self, *args, **kargs):
        super(JavaQuestion, self).__init__(*args, **kargs)
        self.type = 'JA'


class JavaAnswer(Answer):

    code = models.TextField(blank=True, verbose_name='código')
    last_submit_success = models.BooleanField(default=False, verbose_name='sucesso no último envio')
    last_submit_message = models.CharField(max_length=1000, default="Não houve submissão de resposta até o momento.", verbose_name='mensagem da última submissão')

    def __init__(self, *args, **kargs):
        super(JavaAnswer, self).__init__(*args, **kargs)
        self.type = 'JA'

    # Returns 100 score only if all of tests passed
    def correct(self):
        if self.last_submit_success:
            self.score = 100.0
            self.save()
            return 100.0
        else:
            return 0.0

    def __unicode__(self):
        return self.code


class MultipleChoiceQuestion(Question):

    def get_correct_alternative(self):
        #Returns the multiple choice question's correct answer object
        return MultipleChoiceCorrectAlternative.objects.get(question=self)

    def get_alternatives(self):
        #Returns a QuerySet with all of the multiplechoice question's alternatives
        return MultipleChoiceAlternative.objects.filter(Q(multiplechoicecorrectalternative__question=self) | Q(multiplechoicewrongalternative__question=self))

    def __init__(self, *args, **kargs):
        super(MultipleChoiceQuestion, self).__init__(*args, **kargs)
        self.type = 'MU'


class MultipleChoiceAlternative(models.Model):

    text = models.CharField(blank=False, max_length=300, verbose_name='texto da alternativa')

    def __unicode__(self):
        return self.text


class MultipleChoiceCorrectAlternative(MultipleChoiceAlternative):

    question = models.OneToOneField(MultipleChoiceQuestion, verbose_name='questão')


class MultipleChoiceWrongAlternative(MultipleChoiceAlternative):

    question = models.ForeignKey(MultipleChoiceQuestion, verbose_name='questão')


class MultipleChoiceAnswer(Answer):

    chosen_alternative = models.ForeignKey(MultipleChoiceAlternative, blank=True, null=True, verbose_name='alternativa escolhida')

    def __init__(self, *args, **kargs):
        super(MultipleChoiceAnswer, self).__init__(*args, **kargs)
        self.type = 'MU'

    # Returns the score of the answered question
    def correct(self):
        self.score = 0.0
        if self.chosen_alternative is not None and self.chosen_alternative.id == self.question_answered.casted().get_correct_alternative().id:
            self.score = 100.0
        self.save()
        return self.score

    def __unicode__(self):
        return self.chosen_alternative


class TrueFalseQuestion(Question):

    def __init__(self, *args, **kargs):
        super(TrueFalseQuestion, self).__init__(*args, **kargs)
        self.type = 'TF'


class TrueFalseItem(models.Model):
    question = models.ForeignKey(TrueFalseQuestion, verbose_name='questão')
    text = models.TextField('texto do item')
    is_correct = models.BooleanField(u"correto")

    def __unicode__(self):
        return self.text


class TrueFalseAnswer(Answer):

    def __init__(self, *args, **kargs):
        super(TrueFalseAnswer, self).__init__(*args, **kargs)
        self.type = 'TF'

    def correct(self):
        score = 0.0
        items = TrueFalseAnswerItem.objects.filter(answer_group=self)
        for i in items:
            if i.given_answer == i.item_answered.is_correct:
                score += 1
        self.score = 100.0*score/len(items)
        self.save()
        return self.score

    def __unicode__(self):
        items = TrueFalseAnswerItem.objects.filter(answer_group=self)
        return [i.__unicode__() for i in items]


class TrueFalseAnswerItem(models.Model):
    answer_group = models.ForeignKey(TrueFalseAnswer)
    given_answer = models.BooleanField(verbose_name='resposta dada')
    item_answered = models.ForeignKey(TrueFalseItem, verbose_name='item respondido')

    def __unicode__(self):
        if self.given_answer == True:
            return (self.item_answered.__unicode__(), 'Marcado')
        return (self.item_answered.__unicode__(), 'Desmarcado')


class FileQuestion(Question):

    def __init__(self, *args, **kargs):
        super(FileQuestion, self).__init__(*args, **kargs)
        self.type = 'FI'



class FileAnswer(Answer):
    file = models.FileField(upload_to = manage_uploads_filenames, blank=True, verbose_name='arquivo')

    def __init__(self, *args, **kargs):
        super(FileAnswer, self).__init__(*args, **kargs)
        self.type = 'FI'

    def __unicode__(self):
        return self.file
    

#Through model which creates an ordered relationship between
#questions and exercise-lists. Related doc:
#http://docs.djangoproject.com/en/1.3/topics/db/models/#extra-fields-on-many-to-many-relationships
class ExerciseListQuestionThrough(models.Model):
    exerciselist = models.ForeignKey(ExerciseList)
    question = models.ForeignKey(Question)
    order = models.PositiveIntegerField(verbose_name='ordem')
    weight = models.PositiveIntegerField(verbose_name='peso')

    class Meta:
        ordering = ('order', )

# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
import datetime


class ExerciseList(models.Model):
    name = models.CharField(blank=False, max_length=100)
    course = models.ForeignKey('course.Course')
    pub_date = models.DateField(default=datetime.datetime.today)
    due_date = models.DateField(default=(datetime.datetime.today() + datetime.timedelta(days=7)))
    questions = models.ManyToManyField('Question', through='ExerciseListQuestionThrough')

    def get_multiple_choice_questions(self):
        return MultipleChoiceQuestion.objects.filter(exerciselist=self)

    def get_java_questions(self):
        return JavaQuestion.objects.filter(exerciselist=self)

    def get_discursive_questions(self):
        return DiscursiveQuestion.objects.filter(exerciselist=self)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Question(models.Model):

    text = models.TextField()
    QUESTION_TYPE_CHOICES = (
        ('TF', 'True/False'),
        ('DI', 'Discursive'),
        ('JA', 'Java'),
        ('MU', 'Multiple'),
    )

    type = models.CharField(max_length=2, choices=QUESTION_TYPE_CHOICES, blank=True)
    tags = models.ManyToManyField(Tag)

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

        except:
            raise


class ExerciseListSolution(models.Model):

    student = models.ForeignKey('authentication.Student')
    exercise_list = models.ForeignKey(ExerciseList)
    finalized = models.BooleanField(False)

    def get_answers(self):
        return Answer.objects.filter(exercise_list_solution=self)

    def populate_blank(self, *args, **kargs):
        """
        This will go through the questions in the exercise_list
        associated with this ExerciseListSolution and create
        empty answers to each question that does not exist yet
        """

        questions = self.exercise_list.questions.all()
        for question in questions:
            
            if question.type == 'JA':
                answer, answer_created = JavaQuestionAnswer.objects.get_or_create(exercise_list_solution=self, question_answered=question)
            elif question.type == 'DI':
                answer, answer_created = DiscursiveQuestionAnswer.objects.get_or_create(exercise_list_solution=self, question_answered=question)
            elif question.type == 'MU':
                answer, answer_created = MultipleChoiceQuestionAnswer.objects.get_or_create(exercise_list_solution=self, question_answered=question)
            elif question.type == 'TF':
                answer, answer_created = TrueFalseAnswer.objects.get_or_create(exercise_list_solution=self, question_answered=question)
                for truefalsequestion_item in answer.question_answered.casted().truefalseitem_set.all():
                    truefalseanswer_item, truefalseanswer_item_created = TrueFalseAnswerItem.objects.get_or_create(answer_group=answer, item_answered=truefalsequestion_item, given_answer = False)

            if answer_created:
                self.answer_set.add(answer)

        self.save()


class Answer(models.Model):

    exercise_list_solution = models.ForeignKey(ExerciseListSolution, editable=False)
    question_answered = models.ForeignKey(Question, editable=False)

    ANSWER_TYPE_CHOICES = (
        ('TF', 'True/False'),
        ('DI', 'Discursive'),
        ('JA', 'Java'),
        ('MU', 'Multiple'),
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
        might return a MultipleChoiceQuestionAnswer object,
        of a DiscursiveQuestionAnswer object, depending
        on what kind of question it actually is.
        """

        try:
            if self.type == 'TF':
                return self.truefalseanswer
            elif self.type == 'DI':
                return self.discursivequestionanswer
            elif self.type == 'JA':
                return self.javaquestionanswer
            elif self.type == 'MU':
                return self.multiplechoicequestionanswer

        except:
            raise


class DiscursiveQuestion(Question):

    def __init__(self, *args, **kargs):
        super(DiscursiveQuestion, self).__init__(*args, **kargs)
        self.type = 'DI'


class DiscursiveQuestionAnswer(Answer):

    text = models.TextField(blank=True)

    def __init__(self, *args, **kargs):
        super(DiscursiveQuestionAnswer, self).__init__(*args, **kargs)
        self.type = 'DI'


class JavaQuestion(Question):

    criteria = models.TextField()

    def __init__(self, *args, **kargs):
        super(JavaQuestion, self).__init__(*args, **kargs)
        self.type = 'JA'


class JavaQuestionAnswer(Answer):

    code = models.TextField(blank=True)

    def __init__(self, *args, **kargs):
        super(JavaQuestionAnswer, self).__init__(*args, **kargs)
        self.type = 'JA'


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

    text = models.CharField(blank=False, max_length=300)

    def __unicode__(self):
        return self.text


class MultipleChoiceCorrectAlternative(MultipleChoiceAlternative):

    question = models.OneToOneField(MultipleChoiceQuestion)


class MultipleChoiceWrongAlternative(MultipleChoiceAlternative):

    question = models.ForeignKey(MultipleChoiceQuestion)


class MultipleChoiceQuestionAnswer(Answer):

    chosen_alternative = models.ForeignKey(MultipleChoiceAlternative, blank=True, null=True)

    def __init__(self, *args, **kargs):
        super(MultipleChoiceQuestionAnswer, self).__init__(*args, **kargs)
        self.type = 'MU'


class TrueFalseQuestion(Question):

    def __init__(self, *args, **kargs):
        super(TrueFalseQuestion, self).__init__(*args, **kargs)
        self.type = 'TF'


class TrueFalseItem(models.Model):
    question = models.ForeignKey(TrueFalseQuestion)
    text = models.TextField()
    truefalse = models.BooleanField()


class TrueFalseAnswer(Answer):

    def __init__(self, *args, **kargs):
        super(TrueFalseAnswer, self).__init__(*args, **kargs)
        self.type = 'TF'


class TrueFalseAnswerItem(models.Model):
    answer_group = models.ForeignKey(TrueFalseAnswer)
    item_answered = models.ForeignKey(TrueFalseItem)
    given_answer = models.BooleanField()


#Through model which creates an ordered relationship between
#questions and exercise-lists. Related doc:
#http://docs.djangoproject.com/en/1.3/topics/db/models/#extra-fields-on-many-to-many-relationships
class ExerciseListQuestionThrough(models.Model):
    exerciselist = models.ForeignKey(ExerciseList)
    question = models.ForeignKey(Question)
    order = models.PositiveIntegerField()
    weight = models.PositiveIntegerField()

    class Meta:
        ordering = ('order', )

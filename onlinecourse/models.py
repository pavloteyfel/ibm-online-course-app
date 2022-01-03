import sys

from django.db.models.deletion import CASCADE
from django.utils.timezone import now

try:
    from django.db import models
except ImportError:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

import uuid

from django.conf import settings


class Instructor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    full_time = models.BooleanField(default=True)
    total_learners = models.IntegerField()

    def __str__(self):
        return self.user.username


class Learner(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    STUDENT = "student"
    DEVELOPER = "developer"
    DATA_SCIENTIST = "data_scientist"
    DATABASE_ADMIN = "dba"
    OCCUPATION_CHOICES = [
        (STUDENT, "Student"),
        (DEVELOPER, "Developer"),
        (DATA_SCIENTIST, "Data Scientist"),
        (DATABASE_ADMIN, "Database Admin"),
    ]
    occupation = models.CharField(
        null=False, max_length=20, choices=OCCUPATION_CHOICES, default=STUDENT
    )
    social_link = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.username}, {self.occupation}"


class Choice(models.Model):
    choice_text = models.CharField(max_length=255, null=False)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.choice_text} ({self.is_correct})"


class Question(models.Model):
    question_text = models.CharField(max_length=254, null=False)
    grade = models.IntegerField(default=1)
    choices = models.ManyToManyField(Choice)

    def is_get_score(self, selected_ids):
        all_answers = self.choices.filter(is_correct=True).count()
        selected_correct = self.choices.filter(
            is_correct=True, id__in=selected_ids
        ).count()
        return all_answers == selected_correct

    def __str__(self):
        return f"{self.question_text}"


class Course(models.Model):
    name = models.CharField(null=False, max_length=30, default="online course")
    image = models.ImageField(upload_to="course_images/")
    description = models.CharField(max_length=1000)
    pub_date = models.DateField(null=True)
    instructors = models.ManyToManyField(Instructor)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Enrollment")
    total_enrollment = models.IntegerField(default=0)
    questions = models.ManyToManyField(Question)
    is_enrolled = False

    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}"


class Lesson(models.Model):
    title = models.CharField(max_length=200, default="title")
    order = models.IntegerField(default=0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Lesson: ({self.order}) {self.title}"


class Enrollment(models.Model):
    AUDIT = "audit"
    HONOR = "honor"
    BETA = "BETA"
    COURSE_MODES = [(AUDIT, "Audit"), (HONOR, "Honor"), (BETA, "BETA")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateField(default=now)
    mode = models.CharField(max_length=5, choices=COURSE_MODES, default=AUDIT)
    rating = models.FloatField(default=5.0)


class Submission(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=CASCADE)
    choices = models.ManyToManyField(Choice)

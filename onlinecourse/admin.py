from django.contrib import admin

from .models import Choice, Course, Instructor, Learner, Lesson, Question


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


class ChoiceInLine(admin.StackedInline):
    model = Choice
    extra = 5


class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ("name", "pub_date")
    list_filter = ["pub_date"]
    search_fields = ["name", "description"]


class LessonAdmin(admin.ModelAdmin):
    list_display = ["title"]


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text"]
    inline = [ChoiceInLine]


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Choice)

from django.contrib import admin
from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "category", "correct_option")
    list_filter = ("category",)
    search_fields = ("text",)

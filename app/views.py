from django.shortcuts import render
from django.contrib.auth.models import User
import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate

from .serializers import SignupSerializer, QuestionSerializer
from .models import Question


# -------- SIGNUP ----------
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Signup successful"})
    return Response(serializer.errors, status=400)


# -------- SIGNIN ----------
@api_view(["POST"])
@permission_classes([AllowAny])
def signin(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid email or password"}, status=400)

    # Authenticate using stored username
    user = authenticate(username=user_obj.username, password=password)

    if user is None:
        return Response({"error": "Invalid email or password"}, status=400)

    return Response({ "message": "Login successful" })

# -------- GET 100 MIXED QUESTIONS ----------
@api_view(["GET"])
@permission_classes([AllowAny])
def get_questions(request):
    per_cat = 25
    
    categories = [
        Question.CATEGORY_APTITUDE,
        Question.CATEGORY_JAVA,
        Question.CATEGORY_REASONING,
        Question.CATEGORY_PYTHON,
    ]

    lists = []
    for cat in categories:
        qs = list(Question.objects.filter(category=cat))
        random.shuffle(qs)
        lists.append(qs[:per_cat])

    mixed = []
    for i in range(per_cat):
        for group in lists:
            mixed.append(group[i])

    serializer = QuestionSerializer(mixed, many=True)
    return Response(serializer.data)


# -------- SUBMIT ANSWERS ----------
@api_view(["POST"])
@permission_classes([AllowAny])
def submit_quiz(request):
    answers = request.data.get("answers", {})  # {question_id: "a"}

    qids = list(answers.keys())

    questions = Question.objects.filter(id__in=qids)

    score = 0
    for q in questions:
        if answers[str(q.id)] == q.correct_option:
            score += 1

    return Response({
        "total_questions": len(questions),
        "score": score
    })


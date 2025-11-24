from django.shortcuts import render
from django.contrib.auth.models import User
import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate

from .serializers import SignupSerializer, QuestionSerializer
from .models import Question,TestResult


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
    answers = request.data.get("answers", {})  # {"1": "a"}

    if not answers:
        return Response({"error": "No answers provided"}, status=400)

    # Convert question IDs from string -> int
    try:
        qids = [int(qid) for qid in answers.keys()]
    except:
        return Response({"error": "Invalid question IDs"}, status=400)

    questions = Question.objects.filter(id__in=qids)
    total = len(questions)

    if total == 0:
        return Response({"error": "No valid questions found"}, status=400)

    score = 0
    for q in questions:
        if answers.get(str(q.id)) == q.correct_option:
            score += 1

    # Percentage
    percentage = (score / total) * 100

    # Result message
    result_msg = (
        "You are selected. Congratulations!"
        if percentage >= 50
        else "Sorry, try again next time."
    )

    # -------- SAVE RESULT IN DATABASE --------
    TestResult.objects.create(
        user=request.user if request.user.is_authenticated else None,
        total_questions=total,
        correct_answers=score,
        percentage=round(percentage, 2),
        status_message=result_msg
    )

    return Response({
        "total_questions": total,
        "score": score,
        "percentage": round(percentage, 2),
        "message": result_msg
    })
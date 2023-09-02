from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.http import HttpResponseRedirect
from django.middleware import csrf
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recruitment.models import ApplicantResume, Candidate, Company, Vacancy
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

from .filters import ResumeFilterSet, VacancyFilterSet
from .serializers import (
    CandidateSerializer,
    CandidatesSerializer,
    CompanySerializer,
    CompanyShortSerializer,
    ResumeSerializer,
    ResumesSerializer,
    UserSerializer,
    UserSignupSerializer,
    VacanciesSerializer,
    VacancySerializer,
)
from .utils import send_mail_to_user


def get_tokens_for_user(user):
    """Получение токенов для пользователя."""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class LoginView(APIView):
    """Аутентификация пользователя."""

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """POST запрос на получение токенов."""
        data = request.data
        response = Response()
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=data["access"],
                    expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                csrf.get_token(request)
                response.data = {"Success": "Login successfully", "data": data}
                return response
            else:
                return Response(
                    {"No active": "This account is not active!!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"Invalid": "Invalid email or password!!"},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserSignupView(APIView):
    """Регистрация пользователя."""

    pagination_class = None
    permission_classes = [AllowAny]

    def post(self, request):
        """POST запрос создания пользователя."""
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_mail_to_user(user.id, user.confirmation_code, user.email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    """Выход пользователя."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """POST запрос выхода пользователя."""
        logout(request)
        response = HttpResponseRedirect(f"http://{settings.DOMAIN_NAME}/login/")
        response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        return response


class EmailConfirmationView(APIView):
    """Подтверждение email пользователя."""

    pagination_class = None
    permission_classes = [AllowAny]

    def get(self, request, user_id, confirmation_code):
        """GET запрос подтверждения email."""
        user = get_object_or_404(User, pk=user_id)
        if user.confirmation_code == confirmation_code:
            user.email_status = True
            user.save()
            return HttpResponseRedirect(f"http://{settings.DOMAIN_NAME}/login/")
        return Response(
            {"status": "Неверная ссылка!"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(ModelViewSet):
    """Вьюсет для модели пользователей."""

    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"
    lookup_value_regex = r"[0-9]+"
    http_method_names = [
        "get",
    ]


class VacancyViewSet(ModelViewSet):
    """Вьюсет для модели вакансий."""

    queryset = Vacancy.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = VacancyFilterSet
    search_fields = (
        "vacancy_title",
        "company__company_title",
        "city",
        "technology_stack",
    )
    ordering_fields = (
        "vacancy_status",
        "deadline",
        "pub_date",
    )
    ordering = ("pub_date",)

    def get_serializer_class(self):
        """Функция определяющая сериализатор в зависимости от действия."""
        if self.action == "list":
            return VacanciesSerializer
        return VacancySerializer

    def perform_create(self, serializer):
        """Переопределение метода create для записи информация о пользователе."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        """Переопределение метода update для записи информация о пользователе."""
        serializer.save(author=self.request.user)


class ResumeViewSet(ModelViewSet):
    """Вьюсет для модели резюме."""

    queryset = ApplicantResume.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = ResumeFilterSet
    search_fields = (
        "job_title",
        "town",
        "current_job",
    )
    ordering_fields = (
        "applicant",
        "work_experiences",
        "interview_status",
        "current_company",
        "pub_date",
    )
    ordering = ("pub_date",)

    def get_serializer_class(self):
        """Функция определяющая сериализатор в зависимости от действия."""
        if self.action == "list":
            return ResumesSerializer
        return ResumeSerializer


class CandidateViewSet(ModelViewSet):
    """Вьюсет для модели Candidate."""

    queryset = Candidate.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    search_fields = (
        "first_name",
        "last_name",
        "city",
        "last_job",
        "cur_position",
        "phone_number",
        "email",
        "telegram",
        "employment_type",
        "schedule_work",
        "education",
        "interview_status",
    )
    ordering_fields = (
        "last_name",
        "city",
        "last_job",
        "cur_position",
        "salary_expectations",
        "vacancy",
        "employment_type",
        "schedule_work",
        "work_experiences",
        "education",
        "interview_status",
        "pub_date",
    )
    ordering = ("pub_date",)

    def get_serializer_class(self):
        """Функция определяющая сериализатор в зависимости от действия."""
        if self.action == "list":
            return CandidatesSerializer
        return CandidateSerializer


class CompanyViewSet(ModelViewSet):
    """Вьюсет для модели Company."""

    queryset = Company.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_fields = ("company_address",)
    search_fields = (
        "company_title",
        "company_address",
    )
    ordering_fields = (
        "company_title",
        "company_address",
    )
    ordering = ("company_title",)

    def get_serializer_class(self):
        """Функция определяющая сериализатор в зависимости от действия."""
        if self.action == "list":
            return CompanyShortSerializer
        return CompanySerializer

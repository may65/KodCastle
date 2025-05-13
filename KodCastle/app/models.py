# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(
        _('роль'),
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )
    email = models.EmailField(_('email'), unique=True)
    created_at = models.DateTimeField(_('дата регистрации'), auto_now_add=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',  # Уникальное имя
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',  # Уникальное имя
        related_query_name='user',
    )

class Course(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Начинающий'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    )

    title = models.CharField(_('название'), max_length=100)
    description = models.TextField(_('описание'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_courses')
    category = models.CharField(_('категория'), max_length=50)
    level = models.CharField(_('уровень'), max_length=20, choices=LEVEL_CHOICES)
    duration = models.PositiveIntegerField(_('длительность (минуты)'))
    price = models.DecimalField(_('цена'), max_digits=10, decimal_places=2, default=0)
    image_url = models.URLField(_('обложка'), max_length=255, blank=True)
    students = models.ManyToManyField(User, through='Enrollment', related_name='enrolled_courses')

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(_('название'), max_length=100)
    content = models.TextField(_('содержание'))
    position = models.PositiveIntegerField(_('позиция'))

    class Meta:
        ordering = ['position']


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(_('название'), max_length=100)
    video_url = models.URLField(_('видео'), max_length=255, blank=True)
    text_content = models.TextField(_('текст'))
    order_number = models.PositiveIntegerField(_('порядковый номер'))

    class Meta:
        ordering = ['order_number']


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(_('дата регистрации'), auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')


class Assignment(models.Model):
    SOLUTION_TYPES = (
        ('code', 'Код'),
        ('multiple_choice', 'Тестовый опрос'),
    )

    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments')
    task_text = models.TextField(_('текст задания'))
    solution_type = models.CharField(
        _('тип решения'),
        max_length=20,
        choices=SOLUTION_TYPES,
        default='code'
    )


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(_('время отправки'), auto_now_add=True)
    grade = models.FloatField(_('оценка'), null=True, blank=True)
    feedback = models.TextField(_('комментарий'), blank=True)

    class Meta:
        unique_together = ('assignment', 'user')


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_modules = models.ManyToManyField(Module, blank=True)
    score = models.FloatField(_('баллы'), default=0)

    @property
    def completion_percentage(self):
        total_modules = self.course.modules.count()
        completed = self.completed_modules.count()
        return (completed / total_modules * 100) if total_modules else 0
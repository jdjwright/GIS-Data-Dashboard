from django.core.exceptions import PermissionDenied
from school.models import Student, Teacher, ClassGroup
from django.contrib.auth.models import User


def teacher_only(function):
    def wrap(request, *args, **kwargs):

        if request.user.groups.filter(name='Teachers').exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def admin_only(function):
    def wrap(request, *args, **kwargs):

        if request.user.groups.filter(name='Administrators').exists():
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def teacher_or_own_only(function):
    """display only if viewing student's own work or if requesting user is a teacher"""

    def wrap(request, *args, **kwargs):

        if request.user.groups.filter(name='Teachers').exists():
            return function(request, *args, **kwargs)

        # TODO: check this works
        requested_student = Student.objects.get(pk=kwargs['pk'])
        if request.user == requested_student.user:
            return function(request, *args, **kwargs)

        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def teacher_or_own_classgroup(function):
    def wrap(request, *args, **kwargs):

        if request.user.groups.filter(name='Teachers').exists():
            return function(request, *args, **kwargs)

        student = Student.objects.get(user=request.user)
        if student.classgroups.filter(pk=kwargs['classgroup_pk']):
            return function(request, *args, **kwargs)

        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def teacer_or_lm_only(function):
    """ restrict viewing to the requesting (teacher) user or their line managers only"""

    def wrap(request, *args, **kwargs):
        requested_teacher = Teacher.objects.get(pk=kwargs['teacher_pk'])
        requesting_user = request.user # Remember that LMs are defined by a foreign key to a USER, not TEACHER.
        if requested_teacher.user == requesting_user:
            return function(request, *args, **kwargs)

        linemanagers= [requested_teacher]
        current_teacher = requested_teacher
        while True:

            if current_teacher.line_manager:
                linemanagers.append(current_teacher.line_manager)
                if requesting_user in linemanagers:
                    return function(request, *args, **kwargs)
                else:
                    current_teacher = current_teacher.line_manager
            else:
                raise PermissionDenied

        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def own_or_teacher_only(function):
    """
    Restrict editing to either the currently logged-in student or any teacher
    :param function:
    :return:
    """

    def wrap(request, *args, **kwargs):
        requsted_student = Student.objects.get(pk=kwargs['student_pk'])
        requesting_user = request.user

        if requesting_user.groups.filter(name='Teachers'):
            return function(request, *args, **kwargs)

        if requesting_user == requsted_student.user:
            return function(request, *args, **kwargs)

        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
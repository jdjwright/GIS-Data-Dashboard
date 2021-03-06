from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from tracker.forms import *
from tracker.charts import CohortPointGraph, CohortSubTopicChart, StudentChart, StudentSubTopicGraph
from journal.forms import StudentJournalEntryLarge
from journal.functions import move_mark_reflection_to_journal_student_mptt
from osd.decorators import *
from django.urls import reverse, reverse_lazy
from journal.models import StudentJournalEntry
from django.contrib import messages
from timetable.models import Lesson, LessonResources
import logging
from tracker.functions.adddata import *
import os

logger = logging.getLogger(__name__)


@login_required()
def splash(request):
    if request.user.groups.filter(name='Students'):
        student = Student.objects.get(user=request.user)
        classgroups = ClassGroup.objects.filter(student=student)
        first_syllabus = classgroups[0].mptt_syllabustaught.all()[0]
        tree_root = first_syllabus.get_root()
        return redirect(reverse('tracker:student_ratings', args=(student.pk, tree_root.pk)))

    if request.user.groups.filter(name='Teachers'):
        teacher = Teacher.objects.get(user=request.user)

        # Show the teacher's students
        return redirect(reverse('tracker:new_teacher_overview', args=(teacher.pk,)))


@own_or_teacher_only
def student_profile(request, student_pk):
    # For the first (classgroups) table
    student = Student.objects.get(pk=student_pk)
    classes = student.classgroups.all()
    data = {'student': student,
            'sittings': Sitting.objects.filter(classgroup__in=classes),
            'classes': classes}

    # To get the assessments the student has sat:

    sittings = Sitting.objects.filter(classgroup__in=classes)
    scores = []
    for sitting in sittings:
        scores.append(sitting.student_total(student))
    sitting_data = list(zip(sittings, scores))
    data['sitting_data'] = sitting_data

    # Get syllabus ratings:

    syllabuss_learned = []
    for classgroup in student.classgroups.all().distinct():
        syllabuss_learned.append(classgroup.syllabustaught.all())

    for syllabus in syllabuss_learned:
        points_learned = SyllabusPoint.objects.filter(topic__syllabus__in=syllabus).order_by('number').order_by(
            'topic').order_by('topic__syllabus')

    student_ratings = []
    for point in points_learned:
        x = point.get_student_rating(student)
        student_ratings.append(x)

    syllabus_data = list(zip(points_learned, student_ratings))

    data['syllabus_data'] = syllabus_data

    return render(request, 'tracker/splash_student.html', data)


@login_required
def syllabus_detail(request, pk):
    syllabus = get_object_or_404(Syllabus, pk=pk)
    topics = SyllabusTopic.objects.filter(syllabus=syllabus)
    allpoints = []
    for topic in topics:
        # get a list of topics, for each topic get all the syllabus points
        points = SyllabusPoint.objects.filter(topic=topic)
        for point in points:
            allpoints.append(point)

    if request.user.groups.filter(name='Students'):
        return render(request, 'tracker/syllabusdetail.html', {'syllabus': syllabus,
                                                               'specpoints': allpoints})

    if request.user.groups.filter(name='Teachers'):

        students = Student.objects.all().filter(classgroups__syllabustaught=syllabus).order_by('user__last_name')

        ratings = []
        for topic in topics:
            row = []
            for student in students:
                row.append(topic.studentAverageRating(student))
            ratings.append(row)
        student_topic_data = list(zip(topics, ratings))

        return render(request, 'tracker/syllabus_teacher_detail.html', {'syllabus': syllabus,
                                                                        'specpoints': allpoints,
                                                                        'student_topic_data': student_topic_data,
                                                                        'students': students})
# CSV Uplods


@admin_only
def import_spec_points(request):
    # Deal with getting a CSV file

    if request.method == 'POST':
        csvform = CSVDocForm(request.POST, request.FILES)
        if csvform.is_valid():
            file = csvform.save()
            path = file.document.path
            processSpecification(path)
            os.remove(path)
            file.delete()
            return redirect('syllabuses')
    else:
        csvform = CSVDocForm()
    return render(request, 'school/model_form_upload.html', {'csvform': csvform})

def construction(request):
    return render(request, 'school/404.html', {})


@own_or_teacher_only
def input_marks(request, sitting_pk, student_pk):
    # Get the main data we'll need
    sitting = Sitting.objects.get(pk=sitting_pk)
    student = Student.objects.get(pk=student_pk)

    questions = Question.objects.filter(exam=sitting.exam).order_by('qorder')
    marks = []
    for question in questions:
        marks.append(Mark.objects.get_or_create(sitting=sitting, student=student, question=question))
    # Formset to enter the student's mark
    MarkFormset = modelformset_factory(Mark, fields=('score', 'notes'), extra=0, widgets={
        'score': forms.Textarea(attrs={'rows': 1, 'cols': 2, 'class': 'mark-box'}),
    })

    marks = Mark.objects.filter(student=student, sitting=sitting).order_by('question__qorder')
    formset = MarkFormset(queryset=marks)

    if request.method == 'POST':

        formset = MarkFormset(request.POST)

        if formset.is_valid():
            formset.save(commit=False)
            n = 0  # Loop counter

            for mark in marks:  # TODO: move this to the __clean__ method of formset
                # Check marks are correct:
                if formset[n].cleaned_data['score'] is not None:
                    if formset[n].cleaned_data['score'] > mark.question.maxscore:
                        formset[n].add_error('score', 'Score is greater than the maximum for this question')
                        messages.add_message(request, messages.ERROR,
                                             'You have entered a score bigger than the maximum for at least one quesiton!')
                else:
                    formset[n].add_error('score', 'Please set a score')
                    messages.add_message(request, messages.ERROR,
                                         "You have left at least one score blank. Please enter 0 if you didn't get that mark")
                n = n + 1
            # Call is_valid() again. This will return false if we've added an error (from too high score) above.
            if formset.is_valid():
                formset.save()  # Data is now saved.

                # Now we insert the notes into the journals.

                move_mark_reflection_to_journal_student_mptt(student, sitting)

                if request.user.groups.filter(name='Students'):
                    return redirect(reverse('tracker:student_sitting_summary', args=[sitting_pk, student_pk]))

                if request.user.groups.filter(name='Teachers'):
                    return redirect(reverse('tracker:student_sitting_summary', args=[sitting_pk, student_pk]))

            else:  # Either an initial validation error or the mark checking picked up too high a score
                data = list(zip(questions, formset))
                return render(request, 'tracker/exam_scores.html', {'data': data,
                                                                    'sitting': sitting,
                                                                    'marks': marks,
                                                                    'student': student,
                                                                    'formset': formset}, )

        else:
            data = list(zip(questions, formset))
            return render(request, 'tracker/exam_scores.html', {'data': data,
                                                                'sitting': sitting,
                                                                'marks': marks,
                                                                'student': student,
                                                                'formset': formset}, )

    else:
        data = list(zip(questions, formset))
        return render(request, 'tracker/exam_scores.html', {'data': data,
                                                            'sitting': sitting,
                                                            'marks': marks,
                                                            'student': student,
                                                            'formset': formset}, )


@own_or_teacher_only
def student_sitting_summary(request, sitting_pk, student_pk):
    student = Student.objects.get(pk=student_pk)
    sitting = Sitting.objects.get(pk=sitting_pk)

    marks = Mark.objects.filter(sitting=sitting).filter(student=student_pk).order_by('question__qorder')

    syllabus_point_tested = SyllabusPoint.objects.filter(question__mark__in=marks).distinct().order_by(
        'number').order_by('topic')

    student_ratings = []
    for point in syllabus_point_tested:
        x = point.get_student_rating(student)
        student_ratings.append(x)

    point_notes = []
    for point in syllabus_point_tested:
        point_marks = Mark.objects.filter(student=student).filter(sitting=sitting).filter(
            question__syllabuspoint=point)
        single_note = []
        for mark in point_marks:
            single_note.append(mark.notes)
        single_note = list(filter(None, single_note))
        point_notes.append(single_note)

    point_journal = []

    for point in syllabus_point_tested:
        journal_entry, created = StudentJournalEntry.objects.get_or_create(student=student, syllabus_point=point)

    # Create a formset to store the journal items in.
    journal_formset = modelformset_factory(StudentJournalEntry, extra=0, fields=('entry',))

    if request.method == 'POST':

        # Populate the formset with POSTed data:
        point_journal_formset = journal_formset(request.POST)

        if point_journal_formset.is_valid():
            point_journal_formset.save()

            return redirect(reverse('tracker:tracker_overview'))

        else:

            syllabus_data = list(zip(syllabus_point_tested, student_ratings, point_notes, point_journal_formset))

            topics_tested = SyllabusTopic.objects.filter(syllabuspoint__question__mark__in=marks).distinct()
            topic_average_marks = []
            for topic in topics_tested:
                topic_average_marks.append(topic.studentAverageRating(student))

            topic_data = list(zip(topics_tested, topic_average_marks))

            return render(request, 'tracker/student_sitting_summary.html', {'student': student,
                                                                            'sitting': sitting,
                                                                            'marks': marks,
                                                                            'syllabus_data': syllabus_data,
                                                                            'topic_data': topic_data,
                                                                            'point_journal_formset': point_journal_formset})

    else:

        point_journal_formset = journal_formset(
            queryset=StudentJournalEntry.objects.filter(student=student,
                                                        syllabus_point__in=syllabus_point_tested).order_by(
                'syllabus_point__number').order_by('syllabus_point__topic'))

        syllabus_data = list(zip(syllabus_point_tested, student_ratings, point_notes, point_journal_formset))

        topics_tested = SyllabusTopic.objects.filter(syllabuspoint__question__mark__in=marks).distinct()
        topic_average_marks = []
        for topic in topics_tested:
            topic_average_marks.append(topic.studentAverageRating(student))

        topic_data = list(zip(topics_tested, topic_average_marks))

        return render(request, 'tracker/student_sitting_summary.html', {'student': student,
                                                                        'sitting': sitting,
                                                                        'marks': marks,
                                                                        'syllabus_data': syllabus_data,
                                                                        'topic_data': topic_data,
                                                                        'point_journal_formset': point_journal_formset})


@own_or_teacher_only
def student_topic_overview(request, topic_pk, student_pk):
    student = Student.objects.get(pk=student_pk)
    topic = SyllabusTopic.objects.get(pk=topic_pk)

    sub_topic_data = topic.studentSubTopicData(student)

    return render(request, 'tracker/student_topic_overview.html', {'student': student,
                                                                   'topic': topic,
                                                                   'sub_topic_data': sub_topic_data})


@own_or_teacher_only
def student_sub_topic_overview(request, sub_topic_pk, student_pk):
    student = Student.objects.get(pk=student_pk)
    sub_topic = SyllabusSubTopic.objects.get(pk=sub_topic_pk)

    point_data = sub_topic.student_sub_topic_data(student)
    # Remember, get_or_create returns a tuple; the object, and a TRUE or FALSE depending on whether it was created.
    journal, created = StudentJournalEntry.objects.get_or_create(student=student, syllabus_sub_topic=sub_topic)

    if request.method == 'POST':
        journal_form = StudentJournalEntryLarge(request.POST)
        if journal_form.is_valid():
            journal_entry = StudentJournalEntry.objects.get(student=student, syllabus_sub_topic=sub_topic)
            journal_entry.entry = journal_form.cleaned_data['entry']
            journal_entry.save()
            parent_topic_pk = sub_topic.topic.pk
            return redirect(reverse('tracker:student_topic_overview', args=(parent_topic_pk, student_pk)))

        else:
            return render(request, 'tracker/student_sub_topic_overview.html', {'student': student,
                                                                               'sub_topic': sub_topic,
                                                                               'point_data': point_data,
                                                                               'journal_form': journal_form})

    else:

        journal_form = StudentJournalEntryLarge(instance=journal)

        return render(request, 'tracker/student_sub_topic_overview.html', {'student': student,
                                                                           'sub_topic': sub_topic,
                                                                           'point_data': point_data,
                                                                           'journal_form': journal_form})


@own_or_teacher_only
def small_assessment_list(request, point_pk, student_pk):
    '''Create a small window showing which assessments are testing a certain syllabus point.'''

    student = Student.objects.get(pk=student_pk)
    point = SyllabusPoint.objects.get(pk=point_pk)

    assessments = point.student_assesments(student)

    return render(request, 'tracker/small_assessment_list.html', {'student': student,
                                                                  'point': point,
                                                                  'assessments': assessments})


def classgroup_sub_topic_completion(request, classgroup_pk, sub_topic_pk):
    classgroup = ClassGroup.objects.get(pk=classgroup_pk)
    sub_topic = SyllabusSubTopic.objects.get(pk=sub_topic_pk)

    syllabus_points = sub_topic.syllabus_points()
    data = []

    for point in syllabus_points:
        row = [point]

        if point.has_been_taught(classgroup):
            row.append(point.lessons_taught(classgroup))
        else:
            row.append(False)
        if point.has_been_assessed(classgroup):
            row.append(point.classgroup_assessments(classgroup))
        else:
            row.append(False)

        data.append(row)

    return render(request, 'tracker/classgroup_sub_topic_completion.html', {'classgroup': classgroup,
                                                                            'sub_topic': sub_topic,
                                                                            'data': data})


def classgroup_syllabus_completion(request, classgroup_pk, syllabus_pk):
    classgroup = ClassGroup.objects.get(pk=classgroup_pk)
    syllabus = Syllabus.objects.get(pk=syllabus_pk)
    topics = SyllabusTopic.objects.filter(syllabus=syllabus)

    data = []
    for topic in topics:
        row = [topic]
        row.append(topic.classgroup_percentage_taught(classgroup))
        row.append(topic.classgroup_percentage_assessed(classgroup))
        data.append(row)
    return render(request, 'tracker/classgroup_syllabus_completion.html', {'classgroup': classgroup,
                                                                           'syllabus': syllabus,
                                                                           'data': data})


@admin_only
def chart_test(request):
    chart = CohortPointGraph()
    points = SyllabusPoint.objects.filter(topic__pk=1)
    chart.syllabus_areas = points
    chart.students = Student.objects.filter(classgroups__groupname="10B/Ph2")
    return render(request, 'tracker/chart_test.html', {'chart': chart})


@admin_only
def rating_ouput_check(request, classgroup_pk, topic_pk):
    classgroup = ClassGroup.objects.get(pk=classgroup_pk)
    students = Student.objects.filter(classgroups=classgroup)
    topic = SyllabusTopic.objects.get(pk=topic_pk)
    points = SyllabusSubTopic.objects.filter(topic=topic)

    data = []

    # Construct first row
    row = [""]
    for student in students:
        row.append(student)
    row.append("4-5")
    data.append(row)

    for point in points:
        row = []
        row.append(point)
        for student in students:
            row.append(point.get_student_rating(student).rating)
        row.append(point.cohort_rating_number(students, 4, 5))
        data.append(row)

    return render(request, 'tracker/rating_output_check.html', {'data': data})


@admin_only
def sub_topic_chart_test(request):
    chart = CohortSubTopicChart()
    points = SyllabusSubTopic.objects.filter(topic__pk=1)
    chart.syllabus_areas = points
    chart.students = Student.objects.filter(classgroups__groupname="10B/Ph2")
    return render(request, 'tracker/chart_test.html', {'chart': chart})


@own_or_teacher_only
def sub_topic_student_graph_check(request, student_pk, sub_topic_pk):
    student = Student.objects.filter(pk=student_pk)
    topic = SyllabusTopic.objects.get(pk=sub_topic_pk)
    points = SyllabusSubTopic.objects.filter(topic=topic)
    chart = StudentChart()
    chart.students = student
    chart.syllabus_areas = points

    return render(request, "tracker/student_s_topic_chart_test.html", {'student': student,
                                                                       'sub_topic': topic,
                                                                       'chart': chart})


@admin_only
def single_sub_topic_graph_check(request, student_pk, sub_topic_pk):
    student = Student.objects.filter(pk=student_pk)
    points = SyllabusSubTopic.objects.filter(pk=sub_topic_pk)
    chart = StudentSubTopicGraph()
    chart.students = student
    chart.syllabus_areas = points

    return render(request, "tracker/student_single_s_topic_chart.html", {'student': student,
                                                                         'sub_topic': points,
                                                                         'chart': chart})


@admin_only
def set_current_ratings(request):
    set_current_student_point_ratings()


@own_or_teacher_only
def student_ratings(request, student_pk, syllabus_pk):
    student = Student.objects.get(pk=student_pk)
    syllabus = MPTTSyllabus.objects.get(pk=syllabus_pk)

    # For the back buttons:

    if not syllabus.is_root_node():
        parent = syllabus.get_ancestors(ascending=True)[0]
    else:
        parent = False

    # Create a bunch of buttons for each classgroup the student is in,
    # so that a teacher can return to the overview for that group.

    classgroups = ClassGroup.objects.filter(student=student,
                                            mptt_syllabustaught__in=syllabus.get_ancestors(include_self=True),
                                            archived=False)
    # We only want to enable the group overview buttons for teachers:
    if request.user.groups.filter(name='Teachers').exists():
        isteacher = True
    else:
        isteacher = False

    student_as_queryset = Student.objects.filter(pk=student_pk)

    # Data for an overview bar:
    overview_data = syllabus.group_ratings_data(students=student_as_queryset)

    # Data for sub-point raings:

    sub_topic_data = []
    for point in syllabus.get_children():
        row = []
        row.append(point)

        row.append(point.group_ratings_data(student_as_queryset))

        # Add some lessons and resource:
        lessons = Lesson.objects.filter(mptt_syllabus_points=point, classgroup__in=student.classgroups.all())
        resources = []

        # Only allow students to see the correct resources:
        if isteacher:

            for lesson in lessons:
                resources.append(lesson.resources())
        else:
            for lesson in lessons:
                resources.append(lesson.student_viewable_resources())
        row.append(lessons)
        row.append(resources)

        sub_topic_data.append(row)

    # If we're at the second-to-last level, we will
    # have to display the journal etc.
    # If not, we just want the data on the topic.
    test = syllabus.get_descendant_count()
    if syllabus.get_children()[0].get_descendant_count() != 0:
        # We are not at the bottom, so no journal, and let's show assessments:

        assessments = Sitting.objects.filter(classgroup__student=student, classgroup__in=classgroups).order_by(
            'datesat').reverse()
        assessment_data = []
        for assessment in assessments:
            row = []
            row.append(assessment)
            row.append(assessment.student_total(student))
            assessment_data.append(row)
        return render(request, 'tracker/student_ratings_mptt.html', {'student': student,
                                                                     'syllabus': syllabus,
                                                                     'sub_topic_data': sub_topic_data,
                                                                     'parent': parent,
                                                                     'isteacher': isteacher,
                                                                     'classgroups': classgroups,
                                                                     'assessment_data': assessment_data})
    else:
        # we are at the bottom, so need a journal.
        journal, created = StudentJournalEntry.objects.get_or_create(student=student, mptt_syllabus=syllabus)

        if request.method == 'POST':
            journal_form = StudentJournalEntryLarge(request.POST, instance=journal)
            if journal_form.is_valid():
                journal_entry = StudentJournalEntry.objects.get(student=student, mptt_syllabus=syllabus)
                journal_entry.entry = journal_form.cleaned_data['entry']
                journal_entry.save()
                messages.add_message(request, messages.SUCCESS, 'Journal saved.')
            else:
                messages.add(request, messages.ERROR, 'Something went wrong, and your journal has not been saved.')

        else:
            journal_form = StudentJournalEntryLarge(instance=journal)

        return render(request, 'tracker/student_ratings_mptt_w_journal.html', {'student': student,
                                                                               'syllabus': syllabus,
                                                                               'sub_topic_data': sub_topic_data,
                                                                               'parent': parent,
                                                                               'isteacher': isteacher,
                                                                               'classgroups': classgroups,
                                                                               'journal_form': journal_form})


@teacher_only
def student_standardised_data(request, student_pk):
    student = Student.objects.get(pk=student_pk)
    standardised_data = []

    pass_parents = StandardisedData.objects.get(name="PASS")
    pass_data_objects = pass_parents.get_children()

    CAT4_parent = StandardisedData.objects.get(name="CAT4")
    CAT4_data_objects = CAT4_parent.get_children()

    pass_data = StandardisedResult.objects.filter(student=student, standardised_data__in=pass_data_objects)
    CAT4_data = StandardisedResult.objects.filter(student=student, standardised_data__in=CAT4_data_objects)

    standardised_data.append(pass_data)
    standardised_data.append(CAT4_data)

    assessments = Sitting.objects.filter(classgroup__student=student).order_by('datesat').reverse()

    return render(request, 'tracker/student_standardised_overview.html', {'student': student,
                                                                          'standardised_data': standardised_data,
                                                                          'assessments': assessments})


@teacher_only
def cohort_standardised_data_vs_target(request, cohort_pk):
    cohort = Student.objects.all()
    IGCSE_parent = StandardisedData.objects.get(name="IGCSE Grades")
    IGCSE_data_objects = IGCSE_parent.get_children()

    IGCSE_graph_data = []
    for subject in IGCSE_data_objects:
        row = subject.cohort_target_vs_current_data(cohort)
        row.append("/" + str(row[0]) + "/")
        IGCSE_graph_data.append(row)

    return render(request, 'tracker/cohort_std_data_vs_tgt.html', {'IGCSE_graph_data': IGCSE_graph_data})


@teacher_only
def school_standardised_data_vs_target(request, pastoral_pk, academic_pk):
    """ Display clickable radial graphs for a cohort, as narrowed by both their pastoral and academic position in the data structure. """


    # 1. GET THE SUB-LEVELS FOR EACH REQUESTED VIEW: **
    pastoral_level = PastoralStructure.objects.get(pk=pastoral_pk)
    pastroal_sub_levels = pastoral_level.get_children()

    academic_level = AcademicStructure.objects.get(pk=academic_pk)
    academic_sub_levels = academic_level.get_children()

    # 2. Get the students for our current level
    students = Student.objects.filter(classgroups__academicstructure__in=academic_level.get_descendants(include_self=True),
                                      tutorgroup__pastoral_link__in=pastoral_level.get_descendants(include_self=True))

    # KPIs for the whole-cohort overview

    pastroal_kpis = KPIPair.objects.filter(pastoralstructure=pastoral_level)

    # KPIs for the individual sub-group residuals:
    group_kpis=pastoral_level.all_kpis()
    # 3. Generate the average residual for each sub-level

    # GEnerate graphs:
    pastoral_data = generate_kpi_graph_for_cohort(students, pastroal_kpis)

    group_breakdown = generate_sub_pastoral_graph(pastoral_level=pastoral_level,
                                                 kpis=group_kpis,
                                                  academic_level=academic_level)
    return render(request, 'tracker/school_overview.html', {'pastoral_level': pastoral_level,
                                                            'academic_level': academic_level,
                                                            'pastoral_data': pastoral_data,
                                                            'group_breakdown': group_breakdown,
                                                            'pastoral_sub_levels': pastroal_sub_levels})


def generate_kpi_graph_for_cohort(cohort=Student.objects.all(), kpis=KPIPair.objects.all()):
    """ Returns graph data as a list for a KPI pair"""
    data = []
    for pair in kpis:
        row = {'kpi_pair': pair}
        result = pair.student_result
        averages = StandardisedResult.objects.filter(student__in=cohort, standardised_data=result).aggregate(avg_tg=Avg('target'), avg_result=Avg('result'))
        row['avg_target'] = averages['avg_tg']
        row['avg_result'] = averages['avg_result']
        data.append(row)

    return data


# def generate_sub_pastoral_graph(pastoral_level=PastoralStructure.objects.all()[0], kpis=StandardisedData.objects.all(),
#                                 academic_level=AcademicStructure.objects.all()[0]):
#     next_levels = pastoral_level.get_children()
#
#     data = []
#     for group in next_levels:
#         students = group.students()
#         row = {'group': group}
#
#         # Add the link code
#         row['link'] = reverse('tracker:school_standardised_overview', args=[group.pk, academic_level.pk])
#
#         averages = StandardisedResult.objects.filter(student__in=students, standardised_data__in=kpis).aggregate(residual=Avg('residual'))
#         row['avg_residual'] = averages['residual']
#         data.append(row)
#
#     return data

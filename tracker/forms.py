from django import forms
from dal import autocomplete
from django.forms import modelformset_factory
from .models import *
from mptt.forms import TreeNodeChoiceField
from django.forms import formset_factory
from searchableselect.widgets import SearchableSelect


class CSVDetailsForm(forms.Form):
    topic = forms.ModelChoiceField(label='Topic', queryset=SyllabusTopic.objects.all())


class CSVDocForm(forms.ModelForm):
    class Meta:
        model = CSVDoc
        fields = ('description', 'document', )


class questionsForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('',)
        widgets = {
            'syllabuspoint': SearchableSelect(model='tracker.SyllabusPoint', search_field='syllabusText', many=True, limit=10)
        }


class NewExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ('name', 'syllabus',)
        widgets = {
            'syllabus': autocomplete.ModelSelect2Multiple(url='tracker:syllabus-autocomplete')
        }


class SetQuestions(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['qorder', 'qnumber', 'maxscore', 'MPTTsyllabuspoint', 'exam']
        widgets = {
            'MPTTsyllabuspoint': autocomplete.ModelSelect2Multiple(url='tracker:mptt_syllabus_autocomplete',
                                                               forward=['parent'],
                                                               ),
            'exam': forms.HiddenInput()
        }

    class Media:
        js = (
            'https://code.jquery.com/jquery-3.2.1.min.js',
        )


class SyllabusPoint(forms.ModelForm):

    class Meta:
        model = SyllabusPoint
        fields = ['topic', 'sub_topic', 'number', 'syllabusText']

class NewSittingForm(forms.Form):

    classgroup = forms.ModelChoiceField(ClassGroup.objects.all(),
                                        widget=autocomplete.ModelSelect2(url='tracker:classgroups-autocomplete'))
    date = forms.DateField(widget=forms.SelectDateWidget)


class MarkForm(forms.ModelForm):

    class Meta:
        model = Mark
        fields = ['score']


class MPTTSyllabusForm(forms.Form):

    parent = TreeNodeChoiceField(queryset=MPTTSyllabus.objects.all(), required=False)


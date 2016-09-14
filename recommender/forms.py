from django import forms
from .models import *


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='PDF requried')


def get_my_choices():
    global bn
    for v in FormForChoseDepartment.objects.values('MyChoice'):
        for x, bn in v.items():
            c = +1
    return bn


class MyForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)

        self.fields['MyForms'] = forms.ChoiceField(
            choices=get_my_choices(), required=True)


class exlForm(forms.Form):
    docfile = forms.FileField(
        label='exl requried')


class AddForm(forms.Form):
    Add = forms.CharField(label='Enter Department Name of Curriculum', max_length=400)


class addexlForm(forms.Form):
    docfiles = forms.FileField(
        label='exl requried')


class offered_courses(forms.Form):
    offered_courses = forms.CharField(max_length=1000)


class FormForChoseDepartments(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FormForChoseDepartments, self).__init__(*args, **kwargs)

        self.fields['select'] = forms.ChoiceField(
            choices=get_my_choices(), required=True)


class AddDepartmentalElective(forms.Form):
    AddCourse = forms.CharField(max_length=1000)


class SelectDepartmentForAddingCourse(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SelectDepartmentForAddingCourse, self).__init__(*args, **kwargs)

        self.fields['select'] = forms.ChoiceField(
            choices=get_my_choices(), required=True)


class RemoveDepartmentalEelective(forms.Form):
    RemoveDepElective = forms.CharField(max_length=1000)


class SelectDepartmentForRemoveCourse(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SelectDepartmentForRemoveCourse, self).__init__(*args, **kwargs)

        self.fields['select'] = forms.ChoiceField(
            choices=get_my_choices(), required=True)


class SelectDepartmentForEditCourse(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SelectDepartmentForEditCourse, self).__init__(*args, **kwargs)

        self.fields['select'] = forms.ChoiceField(
            choices=get_my_choices(), required=True)


class OldCourse(forms.Form):
    EditOldCourse = forms.CharField(label='Enter old Code Of The Course', max_length=1000)


class NewCourse(forms.Form):
    NewCourseEdited = forms.CharField(label='Enter New Code Of The Course', max_length=1000)


class Replecmentfrom(forms.Form):
    Replecmentfromold = forms.CharField(label='Old Course Code', max_length=1000)


class ReplecmentTo(forms.Form):
    ReplecmentfromNew = forms.CharField(label='New Course Code', max_length=1000)


class selectDepartmentForReplecmentCourse(forms.Form):
    def __init__(self, *args, **kwargs):
        super(selectDepartmentForReplecmentCourse, self).__init__(*args, **kwargs)

        self.fields['select'] = forms.ChoiceField(
            choices=get_my_choices(), required=True)


class SettingsForms(forms.Form):
    receive_newsletters1 = forms.BooleanField(label='Save Your Transcript', required=True)

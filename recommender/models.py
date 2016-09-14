__author__ = 'abdullahfadel'
from django.db import models

from picklefield.fields import PickledObjectField


class SomeObject(models.Model):
    args = PickledObjectField()


class Curriculum(models.Model):
    Curriculum = PickledObjectField()


class FormForChoseDepartment(models.Model):
    MyChoice = PickledObjectField()


class OfferedCourses(models.Model):
    AllCourses = PickledObjectField()


class ReplecmentCourse(models.Model):
    ReplecmentCourse = PickledObjectField()


class SavingTrancript(models.Model):
    Saving = PickledObjectField()


class transcripts(models.Model):
    files = models.FileField(upload_to="transcripts")

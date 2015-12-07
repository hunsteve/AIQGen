from django.db import models

# Create your models here.

class Problem(models.Model):
    name = models.CharField(max_length=64)  
    text = models.TextField()
    score = models.IntegerField()

class Test(models.Model):
    name = models.CharField(max_length=64)
    group = models.CharField(max_length=2)
    date = models.DateField()
    status = models.CharField(max_length=64)
    fullHTML = models.TextField()

class ProblemInTest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    customspacing = models.FloatField()
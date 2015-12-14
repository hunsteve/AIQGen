from AIQGen.models import Test, Problem, ProblemInTest
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from AIQGen.utils import measureHeight


class ProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['name', 'text', 'score', 'autogenerated']

def problemList(request, test_key=-1, template_name='problem_list.html'):
    return render(request, template_name, {'problem_list': Problem.objects.all()} )

def problemCreate(request, test_key=-1, template_name='problem_form.html'):
    test = None
    if test_key >= 0:
        test = get_object_or_404(Test, pk=test_key)
    form = ProblemForm(request.POST or None)
    if form.is_valid():
        problem = form.save()
        problem.measuredheight = measureHeight(problem, request)
        problem.save()
        if test_key < 0:
            return redirect('problem_list')
        else:
            pit = ProblemInTest(test=test, problem=problem, customspacing=0, customscore=problem.score)
            pit.save()
            return redirect('test_problem_list',test_key)
    return render(request, template_name, {'form':form})

def problemUpdate(request, pk, test_key=-1, template_name='problem_form.html'):
    problem = get_object_or_404(Problem, pk=pk)
    form = ProblemForm(request.POST or None, instance=problem)
    if form.is_valid():
        problem = form.save()
        problem.measuredheight = measureHeight(problem, request)
        problem.save()
        if test_key < 0:
            return redirect('problem_list')
        else:
            return redirect('test_problem_list',test_key)
    return render(request, template_name, {'form':form, 'usescript':not problem.autogenerated})

def problemDelete(request, pk, template_name='problem_confirm_delete.html'):
    problem = get_object_or_404(Problem, pk=pk)    
    if request.method=='POST':
        problem.delete()
        return redirect('problem_list')
    return render(request, template_name, {'problem':problem})


def problemSelect(request, test_key, template_name='problem_select.html'):
    test = get_object_or_404(Test, pk=test_key)
    return render(request, template_name, {'problem_list': Problem.objects.all(), 'test':test} )
from AIQGen.models import Problem
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy


class ProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = ['name', 'text', 'score']

def problemList(request, template_name='problem_list.html'):
    return render(request, template_name, {'object_list': Problem.objects.all()} )

def problemCreate(request, template_name='problem_form.html'):
    form = ProblemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('problem_list')
    return render(request, template_name, {'form':form})

def problemUpdate(request, pk, template_name='problem_form.html'):
    problem = get_object_or_404(Problem, pk=pk)
    form = ProblemForm(request.POST or None, instance=problem)
    if form.is_valid():
        form.save()
        return redirect('problem_list')
    return render(request, template_name, {'form':form})

def problemDelete(request, pk, template_name='problem_confirm_delete.html'):
    problem = get_object_or_404(Problem, pk=pk)    
    if request.method=='POST':
        problem.delete()
        return redirect('problem_list')
    return render(request, template_name, {'object':problem})
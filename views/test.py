from AIQGen.models import Test, Problem, ProblemInTest
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy


class TestForm(ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'date', 'group']

def testList(request, template_name='test_list.html'):
    return render(request, template_name, {'test_list': Test.objects.all()} )

def testCreate(request, template_name='test_form.html'):
    form = TestForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('test_list')
    return render(request, template_name, {'form':form})

def testUpdate(request, pk, template_name='test_form.html'):
    test = get_object_or_404(Test, pk=pk)
    form = TestForm(request.POST or None, instance=test)    
    if form.is_valid():
        form.save()
        return redirect('test_list')
    return render(request, template_name, {'form':form})

def testDelete(request, pk, template_name='test_confirm_delete.html'):
    test = get_object_or_404(Test, pk=pk)    
    if request.method=='POST':
        test.delete()
        return redirect('test_list')
    return render(request, template_name, {'test':test})


def testProblemList(request, pk, template_name='test_problem_list.html'):
    test = get_object_or_404(Test, pk=pk)
    if request.method=='POST':
        #TODO: make CSRF validation
        for pit in test.problemintest_set.all():
            pit.customspacing = float(request.POST.get("id_customspacing_%d"%pit.id, pit.customspacing))
            pit.customscore = float(request.POST.get("id_customscore_%d"%pit.id, pit.customscore))
            pit.save()
    return render(request, template_name, {'test':test, 'pit_list':test.problemintest_set.all() })


def testProblemAdd(request, test_key, problem_key):
    test = get_object_or_404(Test, pk=test_key)
    problem = get_object_or_404(Problem, pk=problem_key)
    pit = ProblemInTest(test=test, problem=problem, customspacing=0, customscore=problem.score)
    pit.save()
    return redirect('test_problem_list',test.id)

def testProblemRemove(request, pk):
    pit = get_object_or_404(ProblemInTest, pk=pk)
    redirect_id = pit.test.id
    pit.delete()
    return redirect('test_problem_list',redirect_id)
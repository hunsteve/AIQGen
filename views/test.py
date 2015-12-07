from AIQGen.models import Test, Problem
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
    return render(request, template_name, {'object_list': Test.objects.all()} )

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
    return render(request, template_name, {'object':test})
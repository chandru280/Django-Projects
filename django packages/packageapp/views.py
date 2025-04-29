# Django Table

from django_tables2 import RequestConfig
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Person, Book
from .tables import PersonTable, BookTable
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import PersonForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def create_person(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person-list')   
    else:
        form = PersonForm()
    return render(request, 'person_form.html', {'form': form})

def update_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person-list')   
    else:
        form = PersonForm(instance=person)
    return render(request, 'person_form.html', {'form': form})



def person_list_view(request):
    query = request.GET.get('query', '')

    if query:
        persons = Person.objects.filter(name__icontains=query)
    else:
        persons = Person.objects.all()

    table = PersonTable(persons)
    RequestConfig(request, paginate={'per_page': 10}).configure(table)

    # Handle AJAX request for live search
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('person_table.html', {'table': table, 'ajax': True}, request=request)
        return JsonResponse({'html': html})

    return render(request, 'person_list.html', {'table': table})



def delete_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    person.delete()
    return redirect('person-list')
    







def person_list_pagenation(request):
    person_list = Person.objects.all()
    
    # Create a Paginator object
    paginator = Paginator(person_list, 10)  # Show 10 persons per page

    page_number = request.GET.get('page')  # Get the page number from the URL
    try:
        page_obj = paginator.page(page_number)  # Get the page object
    except PageNotAnInteger:
        # If page_number is not an integer, deliver first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range (e.g. 9999), deliver last page of results
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'pagenation_list.html', {'page_obj': page_obj})

from django_tables2 import SingleTableView
from packageapp.models import Person
from packageapp.tables import PersonTable


from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django_tables2 import RequestConfig

class PersonListView(SingleTableView):
    model = Person
    table_class = PersonTable
    template_name = 'person_list.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if query:
            return Person.objects.filter(name__icontains=query)
        return super().get_queryset()

    def render_to_response(self, context, **response_kwargs):
        # Handle AJAX requests
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('person_table.html', {'table': context['table'], 'ajax': True}, request=self.request)
            return JsonResponse({'html': html})
        return super().render_to_response(context, **response_kwargs)


# class PersonListView(View):
#     template_name = 'person_list.html'
#     table_template_name = 'person_table.html'

#     def get(self, request, *args, **kwargs):
#         query = request.GET.get('query', '')

#         if query:
#             persons = Person.objects.filter(name__icontains=query)
#         else:
#             persons = Person.objects.all()

#         table = PersonTable(persons)
#         RequestConfig(request, paginate={'per_page': 10}).configure(table)

#         # Handle AJAX request for live search
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             html = render_to_string(self.table_template_name, {'table': table, 'ajax': True}, request=request)
#             return JsonResponse({'html': html})

#         return render(request, self.template_name, {'table': table})

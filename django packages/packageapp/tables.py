import django_tables2 as tables
from django.urls import reverse
from .models import Person, Book
from django.utils.html import format_html

class PersonTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name='action.html',
    )

    class Meta:
        model = Person
        template_name = "django_tables2/bootstrap4.html"
        fields = ("name", "age", "city", "actions")

    def render_actions(self, record):
        update_url = reverse('update_person', args=[record.pk])
        delete_url = reverse('delete_person', args=[record.pk])
        
        return format_html(
            '''
            <a href="{}" class="btn btn-warning btn-sm">
                <i class="bi bi-pencil"></i> Update
            </a>
            <a href="{}" class="btn btn-danger btn-sm" onclick="return confirm('Are you sure you want to delete {}?');">
                <i class="bi bi-trash"></i> Delete
            </a>
            ''',
            update_url,
            delete_url,
            record.name 
        )



class BookTable(tables.Table):
    actions = tables.TemplateColumn(
        template_name='action.html',
    )

    class Meta:
        model = Book
        template_name = "django_tables2/bootstrap4.html"
        fields = ("name", "owner")

    def render_actions(self, record):
        update_url = reverse('update_person', args=[record.pk])
        delete_url = reverse('delete_person', args=[record.pk])
        
        return format_html(
            '''
            <a href="{}" class="btn btn-warning btn-sm">
                <i class="bi bi-pencil"></i> Update
            </a>
            <a href="{}" class="btn btn-danger btn-sm" onclick="return confirm('Are you sure you want to delete {}?');">
                <i class="bi bi-trash"></i> Delete
            </a>
            ''',
            update_url,
            delete_url,
            record.name 
        )

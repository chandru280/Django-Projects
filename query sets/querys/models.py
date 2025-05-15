from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField()
    city = models.CharField(max_length=100)
    email = models.EmailField()
    contect = models.IntegerField()
    register_date = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField()
    
    def __str__(self):
        return self.name
    
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    published_year = models.IntegerField()
    price = models.FloatField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
    


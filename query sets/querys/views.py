

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from .models import Book, Author
from .serializers import *
from django.db.models import Count, Sum, Avg


class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = BookCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class BookQueryView(APIView):
    def get(self, request):
        output = {}

        # all(): Get all books
        output['all'] = BookSerializer(Book.objects.all(), many=True).data

        # filter(): Books published after 2010
        output['filtered'] = BookSerializer(Book.objects.filter(published_year__gt=2010), many=True).data

        # exclude(): Exclude books by a certain author
        output['excluded'] = BookSerializer(Book.objects.exclude(author__name="Author1"), many=True).data

        # get(): Get a single book (handle exception)
        try:
            output['single'] = BookSerializer(Book.objects.get(id=1)).data
        except Book.DoesNotExist:
            output['single'] = "Book not found"
        except Book.MultipleObjectsReturned:
            output['single'] = "Multiple books found"

        # first(): Get the first book
        first_book = Book.objects.first()
        output['first'] = BookSerializer(first_book).data if first_book else "No books"

        # last(): Get the last book
        last_book = Book.objects.last()
        output['last'] = BookSerializer(last_book).data if last_book else "No books"

        # count(): Count all books
        output['count'] = Book.objects.count()

        # exists(): Check if books exist
        output['exists'] = Book.objects.exists()

        # order_by(): Order books by price
        output['ordered'] = BookSerializer(Book.objects.order_by('price'), many=True).data

        # reverse(): Reverse the order
        output['reversed'] = BookSerializer(Book.objects.order_by('-price'), many=True).data

        # values(): Get books as dictionaries
        output['values'] = list(Book.objects.values('title', 'price'))

        # values_list(): Get book titles only
        output['values_list'] = list(Book.objects.values_list('title', flat=True))

        # distinct(): Get distinct published years
        output['distinct'] = list(Book.objects.values_list('published_year', flat=True).distinct())

        # select_related(): Optimize by joining author
        books_with_author = Book.objects.select_related('author').all()
        output['select_related'] = BookSerializer(books_with_author, many=True).data

        # prefetch_related(): For reverse FK or M2M
        authors = Author.objects.prefetch_related('books').all()
        output['prefetch_related'] = [{
            'author': author.name,
            'books': [book.title for book in author.books.all()]
        } for author in authors]

        # annotate(): Count books per year
        output['annotate'] = list(Book.objects.values('published_year').annotate(count=Count('id')))

        # aggregate(): Average book price
        output['aggregate'] = Book.objects.aggregate(avg_price=Avg('price'), total_price=Sum('price'))

        # update(): Update book price (all books to 99.99)
        # Book.objects.update(price=99.99)  # Uncomment to test

        # delete(): Delete books with price = 0
        # Book.objects.filter(price=0).delete()  # Uncomment to test

        # defer(): Exclude price until accessed
        deferred = Book.objects.defer('price').first()
        output['defer'] = deferred.title if deferred else "No book"

        # only(): Load only title field
        only_title = Book.objects.only('title').first()
        output['only'] = only_title.title if only_title else "No book"

        # # raw(): Raw SQL
        # raw_books = Book.objects.raw("SELECT * FROM Book")
        # output['raw'] = [book.title for book in raw_books]

        # iterator(): Efficient looping
        output['iterator'] = [book.title for book in Book.objects.iterator()]

        # bulk_create(): Add many books
        # Book.objects.bulk_create([Book(title=f"Book{i}", published_year=2020, price=100, author_id=1) for i in range(10)])

        # bulk_update(): Update all prices
        # books = list(Book.objects.all())
        # for book in books: book.price += 1
        # Book.objects.bulk_update(books, ['price'])

        # union, intersection, difference
        qs1 = Book.objects.filter(price__gt=50)
        qs2 = Book.objects.filter(published_year__gt=2015)

        output['union'] = list(qs1.union(qs2).values_list('id', flat=True))
        output['intersection'] = list(qs1.intersection(qs2).values_list('id', flat=True))
        output['difference'] = list(qs1.difference(qs2).values_list('id', flat=True))

        # as_manager(): Used in custom manager, not shown here

        # explain(): Show SQL query plan
        output['explain'] = Book.objects.filter(price__gt=50).explain()

        return Response(output)

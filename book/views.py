from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Book, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

def home(request):
    searchTerm = request.GET.get('searchBook')
    if searchTerm:
        books = Book.objects.filter(title__icontains=searchTerm)
    else:
        books = Book.objects.all()
    return render(request, 'home.html',	{'searchTerm':searchTerm, 'books': books})

def about(request):
    return HttpResponse('<h1>Welcome to About Page</h1>')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})

def detail(request, book_id):
    book = get_object_or_404(Book,pk=book_id)
    reviews = Review.objects.filter(book = book)
    return render(request, 'detail.html', 
                  {'book':book, 'reviews': reviews})

@login_required
def createreview(request, book_id):   
    book = get_object_or_404(Book,pk=book_id) 
    if request.method == 'GET':
        return render(request, 'createreview.html', 
                      {'form':ReviewForm(), 'book': book})
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.book = book
            newReview.save()
            return redirect('detail', newReview.book)
        except ValueError:
            return render(request, 'createreview.html', 
              {'form':ReviewForm(),'error':'bad data passed in'})

@login_required
def updatereview(request, review_id):
    review = get_object_or_404(Review,pk=review_id,user=request.user)
    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(request, 'updatereview.html', 
                      {'review': review,'form':form})
    else:
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('detail', review.book)
        except ValueError:
            return render(request, 'updatereview.html',
             {'review': review,'form':form,'error':'Bad data in form'})

@login_required
def deletereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect('detail', review.book)
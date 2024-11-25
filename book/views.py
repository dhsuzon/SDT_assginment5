from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.views.generic import CreateView,DetailView, FormView,ListView,View,UpdateView
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserDepositeForm,UserCommentForm,ChangeUserForm
from .models import UserAccount,CategoryModel,BookModel,BookTransactionHistory,UserComment
from django.contrib import messages
from django.utils import timezone



class UserRegistrationView(CreateView):
    form_class = RegistrationForm
    template_name ='book/register.html'
    success_url = reverse_lazy('userlogin')
    
    def form_valid(self, form):
         messages.success(self.request,'user Registration in successfully')
         return super().form_valid(form)
    
    
    
    
class UserLoginView(LoginView):
    template_name ='book/login.html'
    success_url = reverse_lazy('userbooklist')
    
    def get_success_url(self):
        messages.success(self.request,'user loin in successfully')
        return self.success_url
    
    
class UserProfileView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = ChangeUserForm
    template_name ='book/profile.html'
    success_url = reverse_lazy('userprofile')
    
    def get_object(self, queryset = ...):
        return self.request.user
    

    
def UserLogoutView(request):
    logout(request)
    return redirect('userlogin')



class UserDepositeView(LoginRequiredMixin,FormView):
    form_class = UserDepositeForm
    template_name = 'book/deposite.html'
    success_url = reverse_lazy('userbooklist')
    
    def form_valid(self, form):
         amount = form.cleaned_data.get('amount')
         userAccount, created = UserAccount.objects.get_or_create(user = self.request.user)
         
         userAccount.balance += amount
         userAccount.save()
         messages.success(self.request, f" deposite your account this ৳{amount}")
         return super().form_valid(form)
      

class BookshowView(LoginRequiredMixin,ListView):
    model = BookModel 
    template_name = 'book/bookshow.html' 
    context_object_name = 'books'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryModel.objects.all() 
        return context

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')  
        if category_slug:
            category = CategoryModel.objects.get(slug=category_slug)
            return BookModel.objects.filter(Category=category)
        else:
            return BookModel.objects.all()
        
        
        
class BookDetailView(LoginRequiredMixin,DetailView):
    model = BookModel
    template_name = 'book/bookdetail.html'
    pk_url_kwarg = 'id'
    context_object_name = 'book'
    
        
    def post(self,request,*args, **kwargs):
        if self.request.method == 'POST':
            book = self.get_object()
            comment_form = UserCommentForm(self.request.POST)
            if comment_form .is_valid():
                new_comment = comment_form .save(commit=False)
                new_comment.comment = book
                new_comment.save()
            return self.get(self,request,*args, **kwargs)
                 
                
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        context['comments'] = book.comments.all()
        context['comment_form'] = UserCommentForm()
        return context
        
            

        
   
        
        
            
             
            
    
    
    

class BookBoroView(LoginRequiredMixin,View):
    def post(self, request, id):
       
        book = get_object_or_404(BookModel, id=id)
        
        useraccount = get_object_or_404(UserAccount, user=self.request.user)
        
        if book.Status == "available":

            if useraccount.balance >= book.BookPrice:
                book.Status = "borrowed"
                book.save()

                transaction = BookTransactionHistory.objects.create(
                    user=self.request.user,
                    book=book,
                    transaction_type="borrow",
                )
                transaction.save()

                useraccount.balance -= book.BookPrice
                useraccount.save()
                messages.success(request, f"You have successfully borrowed {book.BookName}!")
                return redirect('bookborrowhistory', id=book.id)
            else:

                messages.error(request, "You do not have enough balance to borrow this book.")
                return redirect('bookborrowhistory', id=book.id)
        else:

            messages.error(request, "This book is already borrowed.")
            return redirect('bookborrowhistory', id=book.id)


class BookBorrowHistoryView(LoginRequiredMixin,View):
    def get(self, request, id):
        book = get_object_or_404(BookModel, id=id)
        transactions = BookTransactionHistory.objects.filter(book=book)
        

        return render(request, 'book/bookhistory.html', {
            'book': book,
            'transactions': transactions
        })
class AllBorrowedBooksView(LoginRequiredMixin,View):
    def get(self, request):
        borrowed_books = BookTransactionHistory.objects.filter(is_returned=False)  
        return render(request, 'book/borrow_book_list.html', {
            'borrowed_books': borrowed_books
        })
        
class BookReturnView(LoginRequiredMixin,View):
    def post(self, request, id):
        book = get_object_or_404(BookModel, id=id)
        transaction = get_object_or_404(BookTransactionHistory, book=book, transaction_type="borrow")
        
        useraccount = get_object_or_404(UserAccount, user=self.request.user)
        
        book.Status = "available"
        book.save()
        
        transaction.return_date = timezone.now()
        transaction.is_returned = True
        transaction.transaction_type ='return'
        transaction.save()
        
        useraccount.balance += book.BookPrice
        useraccount.save()
        messages.success(request, f"You have successfully returned {book.BookName}!")
        
        return redirect('bookborrowreturnlist')
    
    
class AllBorrowedReturnsBooksView(LoginRequiredMixin,View):
    def get(self, request):
        borrowed_return_books = BookTransactionHistory.objects.filter(is_returned=True)  
        return render(request, 'book/return_borrow_books.html', {
            'borrowed_return_books': borrowed_return_books
        })







              
              
        
              
            
            
        
            
        




    

        
      
          
        
   
    


    
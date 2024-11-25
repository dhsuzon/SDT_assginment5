
from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserProfileView,UserLogoutView,UserDepositeView,BookshowView,BookDetailView,BookBoroView,BookBorrowHistoryView,AllBorrowedBooksView,BookReturnView,AllBorrowedReturnsBooksView

urlpatterns = [

    path('userregister/',UserRegistrationView.as_view(), name = 'userregister'),
    path('userlogin/',UserLoginView.as_view(), name = 'userlogin'),
    path('userprofile/',UserProfileView.as_view(), name = 'userprofile'),
    path('userlogout/',UserLogoutView, name = 'userlogout'),
    path('userdeposite/',UserDepositeView.as_view(), name = 'userdeposite'),
    path('userbooklist/',BookshowView.as_view(),name = 'userbooklist'),
    path('userbooklist/<slug:category_slug>/',BookshowView.as_view(), name = 'userfilterbooklist'),
    path('userbookdetail/<int:id>/',BookDetailView.as_view(), name = 'bookDetail'),
    path('bookborrow/<int:id>/',BookBoroView.as_view(), name = 'bookborrowhistory'),
    path('bookborrow/<int:id>/', BookBoroView.as_view(), name='bookborrow'),  
    path('bookborrowhistory/<int:id>/',BookBorrowHistoryView.as_view(), name='bookborrowhistory'),  
    path('bookborrowedlist/',AllBorrowedBooksView.as_view(), name='bookborrowlist'),  
    path('bookborrowreturn/<int:id>/',BookReturnView.as_view(), name='bookborrowreturn'),  
    path('bookborrowreturnlist/',AllBorrowedReturnsBooksView.as_view(), name='bookborrowreturnlist'),   

]
from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/member/',views.RegisterMemberView.as_view(),name='member_register'),
    path('register/librarian/',views.RegisterLibrarianView.as_view(),name='librarian_register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', views.LogoutView.as_view(), name='logout_view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #books
    path('books/', views.AddBooks.as_view(), name='add_books'),
    path('books/<int:pk>/', views.UpdateViewDeleteBooks.as_view(), name='update_books'),
    path('members/<int:pk>/', views.MembersManagement.as_view(), name='update_books'),
    path('allmembers/', views.AllMembers.as_view(), name='update_books'),
    # memeber book management
    path('borrow/', views.BorrowedBooks.as_view(), name='update_books'),
    path('return/<int:pk>/',views.ReturnBook.as_view(),name='return_book'),
    # memeber account delete
    path('delete_member/<int:pk>/',views.MemeberDelete.as_view(),name='memeber_delete'),
    
]
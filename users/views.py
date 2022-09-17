from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# errors
from django.shortcuts import get_object_or_404
from django.http import Http404
# blacklist token
from rest_framework_simplejwt.tokens import RefreshToken
# custom permission
from rest_framework.permissions import BasePermission
# models
from users.models import User,Books,BooksManagement
# serializers
from users.serializer import LibrarianSerilizer,MemberSerilizer,BookSerializer,MemberManagementSerilizer,BookManagementSerializer
# for taking the user id from the token
import base64
import json

class RegisterMemberView(APIView):
    ''' for registraion of memeber '''
    serializer_class = MemberSerilizer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
class RegisterLibrarianView(APIView):
    ''' for registraion of librarian '''
    serializer_class =  LibrarianSerilizer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
class LoginView(APIView):
    ''' For login view '''
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')
        return Response({'Message': 'success full '})
            
class LogoutView(APIView):
    """ for logout view """
    permission_classes = (IsAuthenticated,)
    def post(self, request,format=None):
        try:
            refresh_token = request.data.get('refresh_token')
            token_obj = RefreshToken(refresh_token)
            token_obj.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
                    
########################################################################################class IsActive(BasePermission):

SAFE_METHODS = ['GET']  
class LibrarianPermission(BasePermission):   
    """
    Allows access only to "is_librarian" users.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_librarian:
            return True
        return False
        
class AddBooks(APIView):
    ''' for adding the books'''
    permission_classes = (IsAuthenticated,LibrarianPermission)
    
    def get(self, request, format=None):
        books = Books.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
        
    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateViewDeleteBooks(APIView):
    '''
    For updating the books,and deleting the books 
    '''
    permission_classes = (IsAuthenticated,LibrarianPermission)
    
    def get_object(self, pk):
        try:
            return Books.objects.get(pk=pk)
        except Books.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#######################################################################################
# add,view,remove,update members
class AllMembers(APIView):
    """
    Getting all the memebers from User table
    """
    permission_classes = (IsAuthenticated,LibrarianPermission)
    def get(self, request, format=None):
        snippets = User.objects.filter(is_memeber=True)
        serializer = MemberManagementSerilizer(snippets, many=True)
        return Response(serializer.data)
        
class MembersManagement(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = (IsAuthenticated,LibrarianPermission)
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk,is_memeber=True)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = MemberManagementSerilizer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = MemberManagementSerilizer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

###########################################################################################
# borrowed Book lists
# custom permission for memeber
class MemberPermission(BasePermission):   
    """
    Allows access only to "is_librarian" users.
    """
    def has_permission(self, request, view):
        if request.user.is_memeber:
            return True
        return False

class BorrowedBooks(APIView):
    
    permission_classes = (IsAuthenticated,MemberPermission)
    
    def post(self, request, format=None):
        serializer = BookManagementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
           
class ReturnBook(APIView):
    '''
    For returning the books
    '''
    permission_classes = (IsAuthenticated,MemberPermission)
    
    def patch(self, request,pk, format=None):
        book_management = get_object_or_404(BooksManagement, pk=pk) 
        try:
            book = Books.objects.get(id=book_management.book.id)
        except Books.DoesNotExist:
            return Response({'data':'books is not available'},status=status.HTTP_404_NOT_FOUND)
        data = {'status':'returned'} 
        book.status = 'available'
        book.save()
        serializer = BookManagementSerializer(book_management, data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class MemeberDelete(APIView):
    """
    For deleting the members 
    """
    permission_classes = (IsAuthenticated,MemberPermission)
    def delete(self, request, pk, format=None):
        # gor getting the user id from the token
        token = request.META.get('HTTP_AUTHORIZATION',None).split(' ')[1]
        access_token = json.loads(base64.b64decode(token.split(".")[1]))
        user_id = access_token.get('user_id')
        if user_id == pk:
            try:
                user = User.objects.get(id=pk)
            except User.DoesNotExist:
                Response({'data':'not exist the user'})
            user.delete()  
        else:
            Response({'data':'your no allowed to delete'})
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
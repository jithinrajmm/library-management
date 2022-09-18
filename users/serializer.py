from venv import create
from rest_framework import serializers
from users.models import User,Books,BooksManagement
# for taking the user_id from the token
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.fields import CurrentUserDefault
# validation erros in serilizer


class LibrarianSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','password','is_librarian']
        # defining the password feild is not showed to the user
        # after registrations
        extra_kwargs = {
            'password':{ 'write_only':True },
            'is_librarian':{'write_only':True}
        }
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        name = validated_data.get('name')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            # hashing the password
        instance.username=name
        instance.is_librarian=True
        instance.save()
        return instance
        
        
class MemberSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','password','is_memeber']
        # defining the password feild is not showed to the user
        # after registrations
        extra_kwargs = {
            'password':{ 'write_only':True }
        }
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        name = validated_data.get('name')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            # hashing the password
        instance.username=name
        instance.is_memeber=True
        instance.save()
        return instance
        
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['id','name']
        
class MemberManagementSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','name','email','is_memeber']

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        name = validated_data.get('name')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            # hashing the password
        instance.username=name
        instance.save()
        return instance
        
class BookManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooksManagement
        fields = ['id','book','user']
        
    def create(self, validated_data):
        book_id = validated_data.get('book')
        user_id = validated_data.get('user')
        try:
            book = Books.objects.get(id=book_id.id)
        except Books.DoesNotExist:
            raise serializers.ValidationError("book is not available")
        if BooksManagement.objects.filter(book=book_id,user=user_id,status='borrowed').exists():
            raise serializers.ValidationError('Your are already borrowed')
        if book.status == 'borrowed':
            raise serializers.ValidationError('Not available')
        book.status = 'borrowed'
        book.save()
        instance,created = BooksManagement.get_or_create(**validated_data)
        if instance:
            return instance
        if created:
            return created

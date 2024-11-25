from django.contrib import admin
from .models import UserAccount,CategoryModel,BookModel,BookTransactionHistory,UserComment


@admin.register(UserAccount)
class customeUserAccountModelAdmin(admin.ModelAdmin):
    list_display = ['user','balance']
@admin.register(BookModel)
class customeBookModelAdmin(admin.ModelAdmin):
    list_display =['image','BookName','BookPrice','bookTitle','BookDescription','Category','Status']
@admin.register(BookTransactionHistory)
class customeBookTransactionHistorymodelAdmin(admin.ModelAdmin):
    list_display = ['user','book','transaction_type','transaction_date','return_date','is_returned']
@admin.register(UserComment)
class customeUserCommentModelAdmin(admin.ModelAdmin):
    list_display = ['name','email','comment_text','created_at','comment']


class customAdminModel(admin.ModelAdmin):
    prepopulated_fields = {'slug':('categoryName',)}
    list_display = ('categoryName','slug')
admin.site.register(CategoryModel, customAdminModel)

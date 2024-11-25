from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import UserComment

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs = {'class': 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs = {'class': 'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs = {'class': 'required'}))
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None
            
            
class UserDepositeForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2)
    
    
    def clean_amount(self):
        minimam_deposite = 50
        amount =  self.cleaned_data.get('amount')
        
        if amount <= 0:
            raise forms.ValidationError('Amount should be greater than zero.')
        if  amount < minimam_deposite:
            raise forms.ValidationError(f"  amount must be greater than {minimam_deposite}৳")
        
        return amount
    
    
    
class UserCommentForm(forms.ModelForm):
    class Meta:
        model = UserComment
        fields = ['name', 'email', 'comment_text']
        
        
class ChangeUserForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    def __init__(self, *args, **kwargs):
        super(ChangeUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None
        
        
        
        


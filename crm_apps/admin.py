from django import forms
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.core.exceptions import ValidationError


# try:
#     #loading site config
#     site_config = SiteConfig.load()
    
#     #change in admin interface values
#     AdminSite.site_header = site_config.company_name
#     AdminSite.site_title = site_config.compay_name
    
# except:
#     pass


class UserCreationForm(forms.ModelForm):
    """Custom User creation form"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'email', 'designation',
                  'role', 'manager', 'department')
        
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
        
class UserChangeForm(forms.ModelForm):
    """Custom form for updating user information"""
    
    class Meta:
        model = User
        fields = ('name', 'email', 'password',
                   'role', 'manager', 'department','is_active', 'is_admin')
        
    def clean_password(self):
        return self.initial["password"]
    
                

class UserAdmin(BaseUserAdmin):
    """Custom admin for users"""
    
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
         'fields': ('name','department')}),
        ('Manager', {'fields': ('role', 'designation' , 'manager')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'designation', 
                        'role', 'manager', 'department' ,'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    
    
    

# Register your models here.
admin.site.register(User, UserAdmin)


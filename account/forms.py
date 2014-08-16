from django import forms
from django.contrib.auth import forms as authForms
from account.models import UserProfile
from django.utils.translation import ugettext, ugettext_lazy as _

class ProfileForm(forms.Form):
    weibo_id = forms.CharField(max_length=64, required=False)
    weixin_id = forms.CharField(max_length=64, required=False)
    qq_id = forms.CharField(max_length=64, required=False)
    renren_id = forms.CharField(max_length=64, required=False)
    job = forms.CharField(max_length=32, required=False)
    age = forms.IntegerField(required=False)

class UserRegForm(authForms.UserCreationForm):
    username = forms.RegexField(
        label=_("Username"), 
        max_length=30,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':_('Username')},),
        regex=r'^[\w.@+-]+$',
        help_text = _("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages = {
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':_('Password')},),)

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':_('Type your password again'),}),
        help_text = _("Enter the same password as above, for verification."),)
class LoginForm(authForms.AuthenticationForm):
    username = forms.CharField(
        label=_("Username"), 
        max_length=30,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':_('Username')},),
        )
    password = forms.CharField(
        label=_("Password"), 
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':_('Password')},)
        )

class PasswordSetForm(authForms.SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':_("New password")},)
        )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':_("New password confirmation")},)
        )

class PasswordChangeForm(PasswordSetForm):
    error_messages = dict(PasswordSetForm.error_messages, **{
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    })
    old_password = forms.CharField(label=_("Old password"),
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':_("Old password")},))

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'])
        return old_password
PasswordChangeForm.base_fields.keyOrder = ['old_password', 'new_password1',
                                           'new_password2']
        
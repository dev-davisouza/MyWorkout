from django.contrib.auth.forms import UserCreationForm


class RegisterUserForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2',)

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

        self.fields['username'].widget.attrs['placeholder'] = 'Ex.: Mr. Baki'

        self.fields['first_name'].widget.attrs['placeholder'] = 'Ex.: Davi'

        self.fields['last_name'].widget.attrs['placeholder'] = 'Ex.: Souza'

        self.fields['email'].widget.attrs['placeholder'] = 'Ex.: youremail@mail.com'

        self.fields['password1'].widget.attrs['placeholder'] = 'Ex.: P4ssw@rd'

        self.fields['password2'].widget.attrs['placeholder'] = 'Ex.: Passw@rd'

    def get_error_message(self, field_name):
        error_list = self.errors.get(field_name)
        if error_list:
            return error_list[0]

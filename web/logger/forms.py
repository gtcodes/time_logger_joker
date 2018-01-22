from django import forms
from .models import User, Team

class TeamForm(forms.ModelForm):    
    class Meta: 
        model = Team
        fields = '__all__'

    name = forms.CharField(label='Name', max_length=50)
    # members = forms.ModelMultipleChoiceField(queryset=User.objects.all(), label='Members')

    # def __init__(self, *args, **kwargs):
    #     if kwargs.get('instance'):
    #         initial = kwargs.setdefault('initial', {})
    #         initial['members'] = [member.pk for member in kwargs['instance'].member_set.all()]
    #     forms.ModelForm.__init__(self, *args, **kwargs)
    
    def save(self, commit=True):
        # Get the unsave Pizza instance
        instance = forms.ModelForm.save(self, False)

        # Prepare a 'save_m2m' method for the form,
        old_save_m2m = self.save_m2m
        def save_m2m():
           old_save_m2m()
           # This is where we actually link the pizza with toppings
           instance.member_set.clear()
           for topping in self.cleaned_data['members']:
               instance.member_set.add(member)
        self.save_m2m = save_m2m

        # Do we need to save all changes now?
        if commit:
            instance.save()
            self.save_m2m()

        return instance
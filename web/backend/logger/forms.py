from django import forms
from .models import User, Team
from django.contrib.admin.widgets import FilteredSelectMultiple

class TeamForm(forms.Form):    
    
    name = forms.CharField(max_length=50)
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=FilteredSelectMultiple("Members", is_stacked=False))
    
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

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',),}
        js = ('/admin/jsi18n',)
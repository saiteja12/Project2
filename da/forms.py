from django import forms
from . import models

class RaiseTicketForm(forms.ModelForm):
    due_date = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = models.RaiseTicket
        exclude = ('task_status','request_date','assignee')

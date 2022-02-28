from django import forms

class EmailMaterialsForm(forms.Form):
    to_email = forms.EmailField()
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)
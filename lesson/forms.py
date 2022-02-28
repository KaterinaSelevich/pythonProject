from django import forms

class EmailMaterialForm(forms.Form):
    to_email = forms.EmailField()
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)
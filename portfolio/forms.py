from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
	honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

	class Meta:
		model = ContactMessage
		fields = ("name", "email", "message", "honeypot")
		widgets = {
			"name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
			"email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
			"message": forms.Textarea(attrs={"placeholder": "Tell me about your project", "rows": 5}),
		}

	def clean_honeypot(self):
		value = self.cleaned_data.get("honeypot", "")
		if value:
			raise forms.ValidationError("Spam detected.")
		return value

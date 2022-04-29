from django import forms

from mysite.blog.models import Comment


# Dessa forma é criado um form herdando de forms (não considera o model)
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)  # <input type="text">
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


# Dessa forma é criado um form baseado num model
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("name", "email", "body")


class SearchForm(forms.Form):
    """
    O campo query vai possuir o valor inserido pelo usuário
    """

    query = forms.CharField()

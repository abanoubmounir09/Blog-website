from  django import forms
from  .models import Topic,Post


class NewTopicForm(forms.ModelForm):
    message=forms.CharField(widget=forms.Textarea(attrs={'rows':5,'placeholder':'what is in your mind'}),
                            max_length=300,
                            help_text='the max length of text is 300 ')
    class Meta:
        model=Topic
        fields=['subject','message']



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]

        
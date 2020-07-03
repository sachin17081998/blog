from django import forms
from blog.models import post,comments

class postform(forms.ModelForm):
    
    class Meta():
        model=post
        fields=('title','text')
        
        #to connect to any css class we have to create a widget dictonay
        widgets={
            #input field to style                  class name for css
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class commentform(forms.ModelForm):
    class Meta():
        model=comments
        fields=('author','text')
        
        widgets={
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }        
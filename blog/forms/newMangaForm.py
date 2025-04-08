from django import forms

from ..models import PostManga
from ..models import Tag
from django_select2.forms import (
    HeavySelect2MultipleWidget,
    HeavySelect2Widget,
    ModelSelect2MultipleWidget,
    ModelSelect2TagWidget,
    ModelSelect2Widget,
    Select2MultipleWidget,
    Select2Widget,
)
#class PostForm(forms.ModelForm):
#
#    class Meta:
#        model = Post
#        fields = ('title', 'text',)
#        author = models.CharField(max_length=200)
#        title = models.CharField(max_length=200)

class NewMangaForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),

    )

    #title= f.CharField(max_length=100)
    class Meta:
        model = PostManga
        fields = ('title','author','status','urlImage','description','tags')
        widgets = {
            'tags': Select2MultipleWidget
        }

    #title = forms.ModelChoiceField(queryset=Post.objects.values_list('title',flat=True),widget=forms.Select(attrs={'class': 'form-control'}),empty_label="None")


    #title = forms.ModelForm.TextField()

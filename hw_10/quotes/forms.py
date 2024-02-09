from django.forms import CharField, ModelChoiceField, ModelForm, TextInput

from .models import Authors, Quotes, Tag


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]


class QuotesForm(ModelForm):
    tags = CharField(label="Tags", required=False)
    author = ModelChoiceField(
        label="Author",
        required=False,
        queryset=Authors.objects.all(),
        widget=TextInput(attrs={"placeholder": "Enter author or select from the list"}),
    )

    class Meta:
        model = Quotes
        fields = ["quote", "tags", "author"]

    def clean_author(self):
        author_name = self.cleaned_data.get("author")
        try:
            author = Authors.objects.get(author=author_name)
        except Authors.DoesNotExist:
            author = Authors.objects.create(author=author_name)
        return author


class AuthorsForm(ModelForm):
    class Meta:
        model = Authors
        fields = ["author", "borns", "borns_location", "descriptions"]

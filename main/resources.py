from import_export import resources
from main.models import Comment


class CommentResource(resources.ModelResource):
    class Meta:
        model = Comment

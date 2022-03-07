from django.contrib import admin
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from django_summernote.admin import SummernoteModelAdmin
from main.models import Blog, Comment, Category


class CommentInline(admin.StackedInline):
    model = Comment
    fields = ["text", "is_active"]
    extra = 0
    classes = ["collapse"]


@admin.register(Blog)
class BlogAdmin(SummernoteModelAdmin):
    list_display = [
        "title",
        "date_created",
        "last_modified",
        "is_draft",
        "days_since_creation",
        "no_of_comments",
    ]
    list_filter = ["is_draft", "date_created"]
    # ordering = ("title", "-date_created")
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 50
    actions = ["set_blogs_to_published"]
    date_hierarchy = "date_created"
    inlines = [CommentInline]

    summernote_fields = ["body"]

    # fields = [("title", "slug"), "body", "is_draft"]
    fieldsets = (
        (
            None,
            {
                "fields": (("title", "slug"), "body"),
            },
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse", "wide", "extrapretty"),
                "fields": ("is_draft",),
                "description": "Options to configure blog creation",
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(comments_count=Count("comments"))
        return queryset

    @admin.display(empty_value="???")
    def no_of_comments(self, blog):
        return blog.comments_count

    no_of_comments.admin_order_field = "comments_count"

    @admin.display(empty_value="???")
    def days_since_creation(self, blog):
        diff = timezone.now() - blog.date_created
        return diff.days

    days_since_creation.short_description = "Days active"

    def get_ordering(self, request):
        if request.user.is_superuser:
            return ["title", "-date_created"]
        return ["title"]

    @admin.action(description="Mark selected blog(s) as published")
    def set_blogs_to_published(self, request, queryset):
        count = queryset.update(is_draft=False)
        self.message_user(
            request,
            f"{count} blogs have been published successfully.",
            messages.WARNING,
        )


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ["blog", "text", "date_created", "is_active"]
    list_editable = ["text", "is_active"]
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

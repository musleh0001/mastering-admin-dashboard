from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from main.models import Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "date_created",
        "last_modified",
        "is_draft",
        "days_since_creation",
    ]
    list_filter = ["is_draft", "date_created"]
    # ordering = ("title", "-date_created")
    search_fields = ["title"]
    prepopulated_fields = {"slug": ("title",)}
    list_per_page = 50
    actions = ["set_blogs_to_published"]
    date_hierarchy = "date_created"
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
                "fields": ("is_draft",),
                "description": "Options to configure blog creation",
            },
        ),
    )

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


admin.site.register(Blog, BlogAdmin)

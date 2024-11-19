from django.contrib import admin
from .models import Team, Project, Task, Subtask, Comment, Attachment, Notification, Invitation

# Register the Team model
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'lead_user')
    search_fields = ('name', 'description')

# Register the Project model
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'status', 'user', 'team')
    search_fields = ('name', 'status')
    list_filter = ('status', 'start_date', 'end_date')

# Register the Task model
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'status', 'priority', 'user', 'project', 'assigned_to')
    search_fields = ('title', 'status')
    list_filter = ('status', 'due_date', 'priority')

# Register the Subtask model
@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'due_date', 'status', 'task')
    search_fields = ('name', 'status')
    list_filter = ('status', 'due_date')

# Register the Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'timestamp', 'task', 'user')
    search_fields = ('text',)
    list_filter = ('timestamp',)

# Register the Attachment model
@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('file_path', 'upload_date', 'task')
    search_fields = ('file_path',)
    list_filter = ('upload_date',)

# Register the Notification model
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('message', 'read_status', 'timestamp', 'user')
    search_fields = ('message',)
    list_filter = ('read_status', 'timestamp')

# Register the Invitation model
@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'invited_at', 'accepted')
    search_fields = ('user__username', 'project__name')
    list_filter = ('accepted', 'invited_at')

    # Custom action to invite customers (could include logic like sending an email or notification)
    def send_invitations(self, request, queryset):
        for invitation in queryset:
            # Example: Send email or notification (replace with actual logic)
            invitation.accepted = True  # Just an example of marking it as accepted
            invitation.save()
        self.message_user(request, "Invitations sent successfully.")

    actions = [send_invitations]

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import (
    UserRegistrationViewSet,
    TeamViewSet,
    ProjectViewSet,
    TaskViewSet,
    SubtaskViewSet,
    CommentViewSet,
    AttachmentViewSet,
    NotificationViewSet,
    InvitationViewSet,
    NoteViewSet,  # Import the NoteViewSet
)

# Initialize the DefaultRouter
router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='register')
router.register(r'teams', TeamViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'subtasks', SubtaskViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'attachments', AttachmentViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'invitations', InvitationViewSet)
router.register(r'notes', NoteViewSet)  # Register the NoteViewSet

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin route
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT login endpoint
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh endpoint
    path('', include(router.urls)),  # API routes from the router
]

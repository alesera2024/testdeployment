from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from django.contrib.auth.models import User
from .models import Team, Project, Task, Subtask, Comment, Attachment, Notification, Invitation, Note
from .serializers import (
    UserRegistrationSerializer,
    TeamSerializer,
    ProjectSerializer,
    TaskSerializer,
    SubtaskSerializer,
    CommentSerializer,
    AttachmentSerializer,
    NotificationSerializer,
    InvitationSerializer,
    NoteSerializer
)

class CanViewProjectPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return False

class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, CanViewProjectPermission]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Customer').exists():
            return Project.objects.filter(team__members=user)
        return super().get_queryset()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    permission_classes = [IsAuthenticated]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-timestamp')
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Users only see their own notifications
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class InvitationViewSet(viewsets.ModelViewSet):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[IsAdminUser])
    def send_invitation(self, request):
        user_id = request.data.get('user')
        project_id = request.data.get('project')
        try:
            user = User.objects.get(id=user_id)
            project = Project.objects.get(id=project_id)
        except (User.DoesNotExist, Project.DoesNotExist):
            return Response({'error': 'Invalid user or project ID'}, status=status.HTTP_400_BAD_REQUEST)
        invitation, created = Invitation.objects.get_or_create(user=user, project=project)
        if created:
            return Response({'message': 'Invitation sent successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Invitation already exists.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def accept_invitation(self, request):
        invitation_id = request.data.get('invitation_id')
        try:
            invitation = Invitation.objects.get(id=invitation_id, user=request.user)
        except Invitation.DoesNotExist:
            return Response({'error': 'Invalid invitation ID or you are not the invited user.'}, status=status.HTTP_400_BAD_REQUEST)
        if not invitation.accepted:
            invitation.accepted = True
            invitation.save()
            return Response({'message': 'Invitation accepted successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invitation already accepted.'}, status=status.HTTP_400_BAD_REQUEST)

# New Note ViewSet
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

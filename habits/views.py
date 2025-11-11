from rest_framework import viewsets, permissions
from .models import Habit
from .serializers import HabitSerializer
from users.permissions import IsOwnerOrReadOnlyPublic
from django.db.models import Q
from .paginators import HabitPagination


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnlyPublic]
    pagination_class = HabitPagination

    def get_queryset(self):
        user = self.request.user
        if self.action == "list":
            return Habit.objects.filter(Q(owner=user) | Q(is_published=True)).distinct()
        return Habit.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

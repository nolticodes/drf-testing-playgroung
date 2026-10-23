from rest_framework import viewsets, generics, permissions
from forum_app.models import Like, Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer, LikeSerializer
from .permissions import IsOwnerOrAdmin, CustomQuestionPermission
from .throttling import QuestionThrottle, QuestionGetThrottling, QuestionPostThrottling

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [CustomQuestionPermission]
    throttle_classes = [QuestionThrottle]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_throttles(self):
        if self.action == 'list':
            return [QuestionGetThrottling]

        if self.action == 'create':
            return [QuestionPostThrottling]

        return []

class AnswerListCreateView(generics.ListCreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        self.queryset = Answer.objects.all()

        content_param = self.request.query_params.get('content', None)
        if content_param is not None:
            self.queryset = self.queryset.filter(content__icontains=content_param)

        username_param = self.request.query_params.get('username', None)
        if username_param is not None:
            self.queryset = self.queryset.filter(
                author__username=username_param
            )

        is_staff_param = self.request.query_params.get('is_staff')
        if is_staff_param is not None:
            self.queryset = self.queryset.filter(
                author__is_staff=is_staff_param
            )

        return self.queryset

class AnswerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsOwnerOrAdmin]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

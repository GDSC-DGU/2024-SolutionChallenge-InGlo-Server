from django.shortcuts import render
from rest_framework import views , status , viewsets , mixins
from .services.post_service import PostService
from .services.feedback_service import FeedbackService
from .serializers import PostSerializer, PostDetailSerializer, FeedbackSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class PostViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        content와 username을 query parameter로 받아
        필터링된 Post 리스트를 반환(기본값은 공백)
        """
        content = self.request.query_params.get('content', '')
        username = self.request.query_params.get('username', '')
        return PostService.get_post_list(content=content, username=username)
    
    def create(self, request, *args, **kwargs):
        """
        content를 받아 Post를 생성
        """
        title = request.data.get('title')
        content = request.data.get('content')
        sketch_id = request.data.get('sketch_id')
        sdgs = request.data.get('sdgs')
        image = request.data.get('image')

        if content:
            post = PostService.create_post(request.user, sketch_id, title, image, content, sdgs)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Content not found"}, status=status.HTTP_400_BAD_REQUEST)
    
class PostDetailViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):

    def retrieve(self, request, *args, **kwargs):
        """
        post_id를 받아 Post를 반환
        """
        post_id = self.kwargs.get('post_id')
        post = PostService.get_post_by_id(post_id)
        if post:
            serializer = PostDetailSerializer(post, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    def patch(self, request, *args, **kwargs):
        """
        content를 받아 Post를 업데이트
        """
        post_id = self.kwargs.get('post_id')
        title = request.data.get('title')
        content = request.data.get('content')

        if content:
            post = PostService.update_post(request.user, post_id, title, content)
            if post:
                serializer = PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You do not have permission to edit this post."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Content not found"}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        """
        Post 삭제
        """
        post_id = self.kwargs.get('post_id')
        post = PostService.delete_post(request.user, post_id)
        if post:
            return Response({"message": "Post delete successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        
class PostLikeView(views.APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        좋아요 추가 또는 삭제
        """
        post_id = self.kwargs.get('post_id')
        liked = PostService.toggle_like(request.user, post_id)
        if liked:
            return Response({"message": "Like added successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Like removed successfully."}, status=status.HTTP_204_NO_CONTENT)
        
class FeedbackCreateView(views.APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        content를 받아 Feedback을 생성
        """
        post_id = self.kwargs.get('post_id')
        content = request.data.get('content')
        parent_id = request.data.get('parent_id')
        feedback = FeedbackService.create_feedback(request.user, post_id, content, parent_id)
        if feedback:
            serializer = FeedbackSerializer(feedback)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Feedback create failed"}, status=status.HTTP_400_BAD_REQUEST)
        
class FeedbackUpdateDeleteViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
        
    def patch(self, request, *args, **kwargs):
        """
        content를 받아 Feedback을 업데이트
        """
        feedback_id = self.kwargs.get('feedback_id')
        content = request.data.get('content')
        feedback = FeedbackService.update_feedback(request.user, feedback_id, content)
        if feedback:
            serializer = FeedbackSerializer(feedback)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Feedback update failed"}, status=status.HTTP_400_BAD_REQUEST)
            
    def destroy(self, request, *args, **kwargs):
        """
        Feedback 삭제
        """
        feedback_id = self.kwargs.get('feedback_id')
        feedback = FeedbackService.delete_feedback(request.user, feedback_id)
        if feedback:
            return Response({"message": "Feedback delete successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Feedback delete failed"}, status=status.HTTP_400_BAD_REQUEST)
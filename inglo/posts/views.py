from django.shortcuts import render
from rest_framework import generics, views , status
from .services.post_service import PostService
from .serializers import PostSerializer, PostDetailSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class PostListView(generics.ListAPIView):

    serializer_class = PostSerializer

    def get_queryset(self):
        """
        content와 username을 query parameter로 받아
        필터링된 Post 리스트를 반환(기본값은 공백)
        """
        content = self.request.query_params.get('content', '')
        username = self.request.query_params.get('username', '')
        return PostService.get_post_list(content=content, username=username)
    
class PostDetailView(views.APIView):

    def get(self, request, *args, **kwargs):
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

class PostCreateView(views.APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        content를 받아 Post를 생성
        """
        
        content = request.data.get('content')
        sketch_id = request.data.get('sketch_id')
        sdgs = request.data.get('sdgs')

        if content:
            post = PostService.create_post(request.user, sketch_id, content, sdgs)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Content not found"}, status=status.HTTP_400_BAD_REQUEST)

class PostUpdateView(views.APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        content를 받아 Post를 업데이트
        """
        post_id = self.kwargs.get('post_id')
        content = request.data.get('content')

        if content:
            post = PostService.update_post(request.user, post_id, content)
            if post:
                serializer = PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You do not have permission to edit this post."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "Content not found"}, status=status.HTTP_400_BAD_REQUEST)
        
class PostDeleteView(views.APIView):
    
        permission_classes = [IsAuthenticated]
        
        def delete(self, request, *args, **kwargs):
            """
            Post 삭제
            """
            post_id = self.kwargs.get('post_id')
            post = PostService.delete_post(request.user, post_id)
            if post:
                return Response({"message": "Post delete successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
        
# class PostLikeView(views.APIView):

#     permission_classes = [IsAuthenticated]
    
#     def post(self, request, *args, **kwargs):
#         """
#         좋아요 추가 또는 삭제
#         """
#         post_id = self.kwargs.get('post_id')
#         liked = PostService.toggle_like(request.user, post_id)
#         if liked:
#             return Response({"message": "Like added successfully."}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"message": "Like removed successfully."}, status=status.HTTP_204_NO_CONTENT)
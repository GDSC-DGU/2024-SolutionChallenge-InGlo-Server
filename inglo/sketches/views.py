from rest_framework import status
from rest_framework.response import Response
from .serializers import ProblemSerializer
from .services.problem_service import ProblemService
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, views

class ProblemListView(generics.ListAPIView):

    serializer_class = ProblemSerializer

    def get_queryset(self):
        """
        클라이언트로부터 받은 SDGs 값과 관련된 문제정의 리스트 반환
        """

        sdgs = self.kwargs.get('sdgs')
        problem = ProblemService.get_problems_by_sdgs(sdgs)
        return problem



class ProblemCreateView(views.APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        """
        클라이언트로부터 받은 SDGs, content를 바탕으로 문제 생성
        """

        sdgs = self.kwargs.get('sdgs')
        content = request.data.get('content')
        problem = ProblemService.create_problem(sdgs,content)
        if problem:
            return Response({"message": "Problem insert successfully."}, status=status.HTTP_201_CREATED)
        return Response({"error": "Problem creation failed"}, status=status.HTTP_400_BAD_REQUEST)

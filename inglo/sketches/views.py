from rest_framework import status
from rest_framework.response import Response
from .serializers import ProblemSerializer, HMWSerializer, Crazy8StackSerializer, Crazy8ContentSerializer
from .services.problem_service import ProblemService
from .services.hmw_service import HMWService
from .services.crazy8_service import Crazy8Service
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, views

class ProblemListView(generics.ListAPIView):

    serializer_class = ProblemSerializer(many=True, read_only=True)

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
    
class ProblemChooseView(views.APIView):
     
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        클라이언트로부터 받은 problem_id를 가진 빈 스케치를 생성
        이후에 선택되는 hmw, crazy8들은 이 스케치에 연결됨
        """ 
        problem_id = self.kwargs.get('problem_id')
        sketch = ProblemService.create_sketch(problem_id, request.user)
        if sketch:
            return Response({"message": "Problem chosen successfully."}, status=status.HTTP_201_CREATED)
        return Response({"error": "Sketch chosen failed"}, status=status.HTTP_400_BAD_REQUEST)


class HMWListView(generics.ListAPIView):

    serializer_class = HMWSerializer(many=True, read_only=True)

    def get_queryset(self):
        """
        클라이언트로부터 받은 problem_id 값과 관련된 HMW 리스트 반환
        """

        problem_id = self.kwargs.get('problem_id')
        hmw = HMWService.get_hmws_by_problem(problem_id)
        return hmw
    
class HMWCreateView(views.APIView):
    
        permission_classes = [IsAuthenticated]
    
        def post(self, request, *args, **kwargs):
            """
            클라이언트로부터 받은 problem_id, content를 바탕으로 HMW 생성
            생성한 HMW를 사용자가 최근에 만든 빈 스케치에 연결
            """
    
            problem_id = self.kwargs.get('problem_id')
            content = request.data.get('content')
            hmw = HMWService.create_hmw(problem_id,content, request.user)
            if hmw:
                return Response({"message": "HMW insert successfully."}, status=status.HTTP_201_CREATED)
            return Response({"error": "HMW creation failed"}, status=status.HTTP_400_BAD_REQUEST)
        
class Crazy8ListView(generics.ListAPIView):
    
    serializer_class = Crazy8StackSerializer(many=True, read_only=True)
    
    def get_queryset(self):
        """
        클라이언트로부터 받은 problem_id 값과 관련된 Crazy8 리스트 반환
        """
        
        problem_id = self.kwargs.get('problem_id')
        crazy8 = Crazy8Service.get_crazy8s_by_problem(problem_id)
        return crazy8
    
class Crazy8CreateView(views.APIView):
        
        permission_classes = [IsAuthenticated]
        
        def post(self, request, *args, **kwargs):
            """
            클라이언트로부터 받은 problem_id, content를 바탕으로 Crazy8Content를 생성
            이때 Crazy8Stack이 없으면(첫 Crazy8Content 생성시) Crazy8Stack을 생성하고 빈 스케치에 연결
            """
            
            problem_id = self.kwargs.get('problem_id')
            content = request.data.get('content')
            crazy8 = Crazy8Service.create_crazy8(problem_id,content,request.user)
            if crazy8:
                return Response({"message": "Crazy8 insert successfully."}, status=status.HTTP_201_CREATED)
            return Response({"error": "Crazy8 creation failed"}, status=status.HTTP_400_BAD_REQUEST)
        
class Crazy8VoteView(views.APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        클라이언트로부터 받은 crazy8content_id를 가진 Crazy8Content에 투표
        """
        
        crazy8content_id = self.kwargs.get('crazy8content_id')
        voted = Crazy8Service.toggle_vote(request.user, crazy8content_id)
        if voted:
            return Response({"message": "Vote added successfully."}, status=201)
        return Response({"error": "Vote failed"}, status=status.HTTP_400_BAD_REQUEST)
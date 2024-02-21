from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from .serializers import ProblemSerializer, HMWSerializer, Crazy8StackSerializer, SketchSerializer, SketchNestedSerializer, Crazy8StackForMyCrazy8Serializer, HMWListSerializer
from .services.problem_service import ProblemService
from .services.hmw_service import HMWService
from .services.crazy8_service import Crazy8Service
from .services.sketch_service import SketchService
from rest_framework.permissions import IsAuthenticated
from rest_framework import views

class ProblemViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    문제정의에 대한 List와 Create API를 하나의 ViewSet에서 처리
    """
    serializer_class = ProblemSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        클라이언트로부터 받은 SDGs 값과 관련된 문제정의 리스트 반환
        """
        sdgs = self.kwargs.get('sdgs')
        if not 1 <= int(sdgs) <= 17:
            return Response({"error": "SDGs must be a number between 1 and 17."}, status=status.HTTP_400_BAD_REQUEST)
        problem_list = ProblemService.get_problems_by_sdgs(sdgs)
        serializer = ProblemSerializer(problem_list, many=True)
        return Response(serializer.data)
        

    def create(self, request, *args, **kwargs):
        """
        클라이언트로부터 받은 SDGs, content를 바탕으로 문제 생성
        """
        sdgs = self.kwargs.get('sdgs')
        if not 1 <= int(sdgs) <= 17:
            return Response({"error": "SDGs must be a number between 1 and 17."}, status=status.HTTP_400_BAD_REQUEST)
        
        content = request.data.get('content')
        if not content:
            return Response({"error": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        problem = ProblemService.create_problem(sdgs, content)

        if problem:
            return Response({"message": "Problem insert successfully."}, status=status.HTTP_201_CREATED)
        return Response({"error": "Problem creation failed"}, status=status.HTTP_400_BAD_REQUEST)
    
class SketchViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
     
    permission_classes = [IsAuthenticated]
    serializer_class = SketchSerializer

    def create(self, request, *args, **kwargs):
        """
        클라이언트로부터 받은 problem_id를 가진 빈 스케치를 생성
        이후에 선택되는 hmw, crazy8들은 이 스케치에 연결됨
        """ 
        problem_id = request.data.get('problem_id')
        sketch = ProblemService.create_sketch(problem_id, request.user)
        if sketch:
            return Response({"message": "Problem chosen successfully."}, status=status.HTTP_201_CREATED)
        return Response({"error": "Sketch chosen failed"}, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        """
        유저가 작성한 솔루션 스케치 리스트 반환
        """
        user = request.user
        sketches = SketchService.get_sketches_by_user(user)      
        serializer = SketchNestedSerializer(sketches, many=True)
        return Response(serializer.data)

class HMWViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):

    serializer_class = HMWSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        클라이언트로부터 받은 problem id 값과 관련된 "HMW"의 리스트 반환
        """
        
        problem_id = self.kwargs.get('problem_id')
        problem = ProblemService.get_problem_by_id(problem_id)
        serializer = HMWListSerializer(problem)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """
        클라이언트로부터 받은 problem_id, content를 바탕으로 HMW 생성
        생성한 HMW를 사용자가 최근에 만든 빈 스케치에 연결
        """
    
        problem_id = self.kwargs.get('problem_id')
        content = request.data.get('content')

        if not content:
            return Response({"error": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        hmw = HMWService.create_hmw(problem_id,content)

        if hmw:
            return Response({"message": "HMW insert successfully."}, status=status.HTTP_201_CREATED)
        return Response({"error": "HMW creation failed"}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        """
        클라이언트로부터 받은 hmw_id에 이를 선택하게 함
        """
        
        hmw_id = request.data.get('hmw_id')
        user = request.user
        problem_id = self.kwargs.get('problem_id')
        hmw = HMWService.update_hmw(user, hmw_id, problem_id)
        if hmw:
            return Response({"message": "HMW update successfully."}, status=status.HTTP_201_CREATED)
        return Response({"error": "HMW update failed"}, status=status.HTTP_400_BAD_REQUEST)
    
class Crazy8MyView(views.APIView):
    
    def get(self, request, *args, **kwargs):
        """
        유저가 최근에 선택한 빈 스케치에 연결된 Crazy8Stack 반환
        """
        problem_id = self.kwargs.get('problem_id')
        user = request.user
        sketch = SketchService.get_sketches_by_problem_and_user(problem_id,user)
        serializer = Crazy8StackForMyCrazy8Serializer(sketch)
        return Response(serializer.data)
        
class Crazy8ViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    
    serializer_class = Crazy8StackSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        """
        클라이언트로부터 받은 problem id 값과 관련된 Crazy8Stack 반환
        """
        
        problem_id = self.kwargs.get('problem_id')
        sketches = SketchService.get_sketch_by_problem_id(problem_id)
        if not sketches:
            return Response({"error": "Sketch not found"}, status=status.HTTP_404_NOT_FOUND)
        
        crazy8stacks_data = []

        for sketch in sketches:
            if sketch.crazy8stack:
                serializer = Crazy8StackSerializer(sketch.crazy8stack)
                crazy8stacks_data.append(serializer.data)
        return Response(crazy8stacks_data)
        
        
    def create(self, request, *args, **kwargs):
        """
        클라이언트로부터 받은 problem_id, content를 바탕으로 Crazy8Content를 생성
        이때 Crazy8Stack이 없으면(첫 Crazy8Content 생성시) Crazy8Stack을 생성하고 빈 스케치에 연결
        """
            
        problem_id = self.kwargs.get('problem_id')
        content = request.data.get('content')

        if not content:
            return Response({"error": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        crazy8 = Crazy8Service.create_crazy8(problem_id,content,request.user)
        if crazy8:
            return Response({"message": "Crazy8 insert successfully."}, status=status.HTTP_201_CREATED)
        return Response({"error": "Problem or Sketch(related with problem and now user) not exist."}, status=status.HTTP_404_NOT_FOUND)
        
class Crazy8VoteView(views.APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        """
        클라이언트로부터 받은 crazy8content_id를 가진 Crazy8Content에 투표
        """
        
        crazy8content_id = request.data.get('crazy8content_id')
        voted = Crazy8Service.toggle_vote(request.user, crazy8content_id)
        if voted:
            return Response({"message": "Vote added successfully."}, status=201)
        return Response({"error": "Vote failed"}, status=status.HTTP_400_BAD_REQUEST)
    
class SketchDetailViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):

    serializer_class = SketchNestedSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        클라이언트로부터 받은 sketch_id를 가진 스케치 반환
        """

        sketch_id = self.kwargs.get('sketch_id')
        sketch = SketchService.get_sketch_by_id(sketch_id)
        if sketch:
            serializer = SketchNestedSerializer(sketch)
            return Response(serializer.data)
        else:
            return Response({"error": "Sketch not found"}, status=404)
        
    def destroy(self, request, *args, **kwargs):
        """
        유저가 작성한 솔루션 스케치 삭제
        """

        sketch_id = self.kwargs.get('sketch_id')
        sketch = SketchService.delete_sketch(sketch_id)
        if sketch:
            return Response({"message": "Sketch delete successfully."}, status=status.HTTP_201_CREATED)
        return Response({"error": "Sketch delete failed"}, status=status.HTTP_400_BAD_REQUEST)
    
class SketchUpdateView(views.APIView):
    
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        """
        지금까지 작성된 문제정의, HMW, Crazy8을 바탕으로, 
        이미 생성되어있던 빈 스케치에 내용들을 추가
        """
        
        problem_id = self.kwargs.get('problem_id')
        title = request.data.get('title')
        description = request.data.get('description')
        image = request.FILES.get('image')
        content = request.data.get('content')

        if not title or not description or not content:
            return Response({"error": "Title, description and content are required."}, status=status.HTTP_400_BAD_REQUEST)

        sketch = SketchService.update_sketch(request.user,problem_id,title,description,image,content)
        if sketch:
            return Response({"message": "Sketch update successfully."}, status=status.HTTP_201_CREATED)
        return Response({"error": "Sketch update failed"}, status=status.HTTP_400_BAD_REQUEST)
    
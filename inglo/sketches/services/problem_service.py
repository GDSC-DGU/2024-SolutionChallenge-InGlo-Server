from ..models import Problem

class ProblemService:
    @staticmethod
    def get_problems_by_sdgs(sdgs):
        if not sdgs.isdigit() or not 1 <= int(sdgs) <= 17:
            return Problem.objects.none()
        try:
            sdgs = int(sdgs)
            return Problem.objects.filter(sdgs=sdgs).order_by('-created_at')[:10]
        except (ValueError, TypeError):
            return Problem.objects.none()

    @staticmethod
    def create_problem(sdgs, content):
        try:
            sdgs = int(sdgs)
            problem = Problem.objects.create(sdgs=sdgs, content=content)
            return problem
        except (ValueError, TypeError):
            return None
from ..models import Sketch
from ..models import Problem

class SketchService:
    def get_sketches_by_user(user):
        return Sketch.objects.filter(user=user)
    
    def update_sketch(user,problem_id,title,description,image_url,content):
        problem = Problem.objects.get(id = problem_id)
        sketch = Sketch.objects.filter(user=user, problem=problem).order_by('-created_at').first()
        sketch.title = title
        sketch.description = description
        sketch.image_url = image_url
        sketch.content = content
        sketch.save()
        return sketch
    
    def delete_sketch(sketch_id):
        sketch = Sketch.objects.get(id=sketch_id)
        sketch.delete()
        return sketch

    def get_sketch_by_id(sketch_id):
        return Sketch.objects.get(id=sketch_id)
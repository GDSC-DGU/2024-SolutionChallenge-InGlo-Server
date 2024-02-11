from ..models import Sketch

class SketchService:
    def get_sketches_by_user(user):
        return Sketch.objects.filter(user=user)
    
    def update_sketch(user, title, description, image_url, content, problem_id):
        sketch = Sketch.objects.filter(user=user, problem=problem_id).order_by('-created_at').first()
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

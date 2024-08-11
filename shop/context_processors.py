from .models import Category


def inject_categories(request):
    return {"categories": Category.objects.all()}

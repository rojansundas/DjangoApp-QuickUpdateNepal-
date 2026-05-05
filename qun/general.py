from .models import Category


def global_data_send(request):
    return{
        'categoryData': Category.objects.all()
    }

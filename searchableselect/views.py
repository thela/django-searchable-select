try:
    # Django <=1.9
    from django.db.models.loading import get_model
except ImportError:
    # Django 1.10+
    from django.apps import apps
    get_model = apps.get_model

from django.utils.encoding import smart_str
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

#@staff_member_required
@login_required
def filter_models(request):
    model_name = request.GET.get('model')
    search_field = request.GET.get('search_field')
    value = request.GET.get('q')
    limit = int(request.GET.get('limit', 10))
    try:
        model = get_model(model_name)
    except LookupError as e:  # pragma: no cover
        return JsonResponse(dict(status=400, error=e.message))
    except (ValueError, AttributeError) as e:  # pragma: no cover
        return JsonResponse(dict(status=400, error='Malformed model parameter.'))

    values = model.objects.filter(**{'{}__icontains'.format(search_field): value})[:limit]
    values = [
        dict(pk=v.pk, name=smart_str(v))
        for v
        in values
    ]

    return JsonResponse(dict(result=values))

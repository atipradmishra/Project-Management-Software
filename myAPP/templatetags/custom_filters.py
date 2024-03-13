from django import template

register = template.Library()

@register.filter
def exists_in_queryset(value, queryset):
    return queryset.filter(id=value.id).exists()



@register.filter
def get_location_count(location_count_set, project_activity_id):
    try:
        return location_count_set.get(project_activity_id=project_activity_id).count
    except location_count_set.model.DoesNotExist:
        return None

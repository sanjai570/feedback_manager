from .models import Resource
from django.shortcuts import get_object_or_404

class ResourceService:
    @staticmethod
    def create_resource(data):
        return Resource.objects.create(**data)

    @staticmethod
    def get_all_resources():
        return Resource.objects.all()

    @staticmethod
    def get_resource_by_id(resource_id):
        return get_object_or_404(Resource, id=resource_id)

    @staticmethod
    def update_resource(resource_id, data):
        resource = get_object_or_404(Resource, id=resource_id)
        for key, value in data.items():
            setattr(resource, key, value)
        resource.save()
        return resource

    @staticmethod
    def delete_resource(resource_id):
        resource = get_object_or_404(Resource, id=resource_id)
        resource.delete()
        return True

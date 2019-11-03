from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection, transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404


from drf_yasg import openapi

from .sql_query import get_tree
from .models import NestedCategory
from .serializers import CategorySerializer

node_name = openapi.Parameter('node_name',
                              openapi.IN_QUERY,
                              description="Node for operation",
                              type=openapi.TYPE_STRING)
new_node_name = openapi.Parameter('new_node_name',
                                  openapi.IN_QUERY,
                                  description="New name for node",
                                  type=openapi.TYPE_STRING)


# Create your views here.
class NestedCategoryView(APIView):
    @swagger_auto_schema(manual_parameters=[node_name])
    def get(self, request):
        node_name = request.query_params.get('node_name')
        if node_name == 'all':
            categories = NestedCategory.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response({"result": serializer.data})

        category = get_object_or_404(NestedCategory.objects.all(), name=node_name)

        with connection.cursor() as cursor:
            cursor.execute(get_tree, {'lft': category.lft, 'rgt': category.rgt})
            row = cursor.fetchall()
        min_value = min([item[1] for item in row])
        result = [' ' * (item[1] - min_value) + str(item[0]) for item in row]

        return Response({"result": result})

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'new_node_name': openapi.Schema(type=openapi.TYPE_STRING, description='Name for new node', ),
            'node_name': openapi.Schema(type=openapi.TYPE_STRING, description='Node name'),
            'is_leaf': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='is leaf'),
        }
    ))
    @transaction.atomic
    def post(self, request):
        data = request.data
        new_node_name = data.get('new_node_name')
        node_name = data.get('node_name')
        is_leaf = data.get('is_leaf')

        all_obj = NestedCategory.objects.all()

        category = get_object_or_404(all_obj, name=node_name)
        pos = category.lft if is_leaf else category.rgt

        all_obj.filter(rgt__gt=pos).update(rgt=F('rgt') + 2)
        all_obj.filter(lft__gt=pos).update(lft=F('lft') + 2)

        new_category = dict(lft=pos + 1, rgt=pos + 2, name=new_node_name)
        serializer = CategorySerializer(data=new_category)
        if serializer.is_valid(raise_exception=True):
            category_saved = serializer.save()

        return Response({"success": f"Category '{category_saved.name}' added successfully"})

    @swagger_auto_schema(manual_parameters=[node_name, new_node_name])
    def put(self, request):

        category_saved = get_object_or_404(NestedCategory.objects.all(), name=request.query_params.get('node_name'))
        data = dict(name=request.query_params.get('new_node_name'), rgt=category_saved.rgt, lft=category_saved.rgt)
        serializer = CategorySerializer(instance=category_saved, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            category_saved = serializer.save()
        return Response({
            "success": f"Category '{category_saved.name}' updated successfully"
        })

    @swagger_auto_schema(manual_parameters=[node_name])
    def delete(self, request):
        category_deleted = get_object_or_404(NestedCategory.objects.all(), name=request.query_params.get('node_name'))
        category_deleted.delete()
        return Response({"message": f"Category `{category_deleted.name}` has been deleted."}, status=200)

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework_csv.renderers import CSVRenderer
from rest_framework_yaml.renderers import YAMLRenderer
from rest_framework import generics
from .models import MenuItems
from .serializers import MenuItemsSerializer, CategorySerializer


# class MenuItemsView(generics.ListCreateAPIView):
#     queryset = MenuItems.objects.select_related("category").all()
#     serializer_class = MenuItemsSerializer


# class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
#     queryset = MenuItems.objects.all()
#     serializer_class = MenuItemsSerializer


@api_view()
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
    items = MenuItems.objects.select_related("category").all()
    serialized_item = MenuItemsSerializer(items, many=True)
    return Response({"data": serialized_item.data}, template_name="menu-items.html")


@api_view(["GET", "POST"])
# @renderer_classes([YAMLRenderer])
def menu_items(request):
    if request.method == "GET":
        items = MenuItems.objects.select_related("category").all()
        serialized_item = MenuItemsSerializer(items, many=True)
        return Response(serialized_item.data)
    if request.method == "POST":
        serialized_item = MenuItemsSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)


@api_view()
def single_item(request):
    items = get_object_or_404(MenuItems, pk=id)
    serialized_item = MenuItemsSerializer(item)
    return Response(serialized_item.data)


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)

from django.shortcuts import render, redirect
from ..models import Category
from ..forms import CategoryForm, ProductForm  # 제품 폼 가져오기


def category_list(request):
    """모든 카테고리를 가져와서 category_list.html 템플릿에 전달"""
    categories = Category.objects.all()  # 모든 카테고리 가져오기
    return render(request, 'category_list.html', {'categories': categories})


def category_create(request):
    """새로운 카테고리를 생성할 수 있는 폼을 제공
     POST 요청 시 유효성을 검사하고 카테고리를 저장한 뒤 카테고리 목록으로 리디렉션"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')  # 카테고리 목록으로 리디렉션
    else:
        form = CategoryForm()

    return render(request, 'category_form.html', {'form': form})
#
# # 카테고리 생성 뷰
# def category_create(request):
#     if request.method == 'POST':
#         form = CategoryForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('category_list')
#     else:
#         form = CategoryForm()
#     return render(request, 'category_form.html', {'form': form})
#
# # 카테고리 업데이트 뷰
# def category_update(request, pk):
#     category = get_object_or_404(Category, pk=pk)  # 객체를 안전하게 가져오기
#     if request.method == 'POST':
#         form = CategoryForm(request.POST, instance=category)
#         if form.is_valid():
#             form.save()
#             return redirect('category_list')
#     else:
#         form = CategoryForm(instance=category)
#     return render(request, 'category_form.html', {'form': form})
#
# # 카테고리 삭제 뷰
# def category_delete(request, pk):
#     category = get_object_or_404(Category, pk=pk)  # 객체를 안전하게 가져오기
#     if request.method == 'POST':
#         category.delete()
#         return redirect('category_list')
#     return render(request, 'category_confirm_delete.html', {'category': category})
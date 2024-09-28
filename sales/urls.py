from django.urls import path
from .views import base_views, product_views
from .views.category_views import category_list, category_create, category_update, category_delete

app_name = 'sales'  # URL 네임스페이스. 다른 앱의 URL 패턴과 충돌하지 않도록 설정

"""
path 함수 설명:
1. 첫 번째 인수: URL 패턴을 나타냄.
2. 두 번째 인수: 해당 URL 패턴에 매핑되는 뷰 함수.
3. 세 번째 인수: URL 패턴에 대한 별칭 (템플릿에서 URL을 쉽게 참조하기 위해 사용).

예:
path('', base_views.index, name='index')는
기본 URL('/')에 해당하며, 이 URL로 접근할 때 base_views.index 함수를 호출하고
별칭 'index'로 템플릿 등에서 참조할 수 있음.
"""

urlpatterns = [
    # 메인 페이지 (질문 목록 페이지)로 이동. 기본 URL('/')에 매핑되며, base_views.index 함수가 호출됨.
    path('', base_views.index, name='index'),

    # 질문 상세 페이지로 이동. product_id 매개변수를 받아 해당 질문의 세부 내용을 보여주는 base_views.detail 함수 호출.
    path('<int:product_id>/', base_views.detail, name='detail'),
    path('product/create/', product_views.product_create, name='product_create'),
    path('categories/', category_list, name='category_list'),
    path('categories/create/', category_create, name='category_create'),
    path('categories/update/<int:pk>/', category_update, name='category_update'),
    # path('product/modify/<int:product_id>/', product_views.product_modify, name='product_modify'),
    # path('product/delete/<int:product_id>/', product_views.product_delete, name='product_delete'),
    # path('product/vote/<int:product_id>/', product_views.product_vote, name='product_vote'),
    # answer_views.py 관련 URL
    # path('answer/create/<int:product_id>/', answer_views.answer_create, name='answer_create'),
    # path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    # path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),
    # path('answer/vote/<int:answer_id>/', answer_views.answer_vote, name='answer_vote'),
    # path('comment/create/product/<int:product_id>/', comment_views.comment_create_product, name='comment_create_product'),
    # path('comment/modify/product/<int:comment_id>/', comment_views.comment_modify_product, name='comment_modify_product'),
    # path('comment/delete/product/<int:comment_id>/', comment_views.comment_delete_product, name='comment_delete_product'),
]
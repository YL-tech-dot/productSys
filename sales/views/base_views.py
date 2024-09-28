from django.core.paginator import Paginator  # 페이징 처리를 위한 Paginator 클래스
from django.shortcuts import render, get_object_or_404  # 뷰 처리, 객체 조회 기능
# from django.db.models import Q  # 검색 조건을 위한 Q 객체
import logging  # 로그 출력을 위한 모듈
from django.db.models import FilteredRelation, Q

logger = logging.getLogger('sales')  # 'sales'라는 로거 생성

from ..models import Product  # Product 모델 가져오기


# =======================================
# sales 질문 목록 출력 뷰
# =======================================
def index(request):
    """ sales 목록 출력 """

    # INFO 레벨 로그 메시지 출력
    logger.info("INFO 레벨로 출력")
    # GET 요청에서 'page' 번호를 가져옵니다. 없으면 기본값으로 '1'을 사용
    page = request.GET.get('page', '1')
    # GET 요청에서 'kw' (검색어)를 가져옵니다. 없으면 기본값으로 빈 문자열을 사용
    kw = request.GET.get('kw', '')

    # Product 모델의 데이터를 최신순으로 정렬하여 가져옵니다.
    product_list = Product.objects.order_by('-create_date')
    # 필터용
    # filtered_books = Product.objects.filter(FilteredRelation('pname', condition=Q(pcategories='computer')))
    # 검색어(kw)가 있으면 필터링 수행
    if kw:
        # 제목, 내용, 답변 내용, 질문 글쓴이, 답변 글쓴이에서 검색어를 포함한 데이터 필터링
        product_list = product_list.filter(
            Q(pcode__icontains=kw) |  # pnumber 검색어 포함
            Q(pname__icontains=kw) |  # 품목 검색어 포함
            Q(pcategories__icontains=kw) # 카테고리 분류 포함
            # Q(answer__content__icontains=kw) |  # 답변 내용에 검색어 포함
            # Q(author__username__icontains=kw) |  # 질문 글쓴이 이름에 검색어 포함
            # Q(answer__author__username__icontains=kw)  # 답변 글쓴이 이름에 검색어 포함
        ).distinct()  # 중복 제거

    # ===============================
    # 페이징 처리
    # ===============================

    # 페이지네이터(Paginator)를 사용해 한 페이지에 10개 항목씩 표시
    paginator = Paginator(product_list, 10)

    # 현재 페이지 번호에 해당하는 데이터 가져오기
    page_obj = paginator.get_page(page)

    # 템플릿에 전달할 데이터 정의 (페이지 객체, 현재 페이지 번호, 검색어)
    context = {'QList': page_obj, 'page': page, 'kw': kw}

    # 템플릿 'sales/product_list.html'을 렌더링하여 응답 반환
    return render(request, 'sales/product_list.html', context)


# =======================================
#sales 질문 상세 내용 출력 뷰
# =======================================
def detail(request, product_id):
    """ salessales 내용 출력 """

    # 주어진 product_id에 해당하는 Product 객체를 가져옵니다. 없으면 404 에러 발생
    product = get_object_or_404(Product, pk=product_id)

    # 질문에 달린 댓글들 중, 부모가 없는 댓글들(최상위 댓글)을 가져옵니다.
    comments = product.comments.filter(parent__isnull=True)

    # 템플릿에 전달할 데이터 설정 (질문, 댓글)
    context = {'product': product, 'comments': comments}

    # 템플릿 'sales/product_detail.html'을 렌더링하여 응답 반환
    return render(request, 'sales/product_detail.html', context)

#########################################
# 제네릭 뷰를 사용한 방법 (주석 처리)
#########################################
# # 클래스 기반의 제네릭 뷰를 사용하여 질문 목록 및 상세 내용을 처리할 수 있음
# from django.views import generic

# # sales 질문 목록을 출력하는 클래스 기반 뷰 (ListView)
# class IndexView(generic.ListView):
#     """
#     sales 목록 출력
#     """
#     # 기본적으로 모델명_list.html 템플릿을 사용
#     model = Product  # 모델 설정

#     # 최신 순으로 정렬된 질문 목록을 반환
#     def get_queryset(self):
#         return Product.objects.order_by('-create_date')

# # sales 질문 상세 내용을 출력하는 클래스 기반 뷰 (DetailView)
# class DetailView(generic.DetailView):
#     """
#     sales 내용 출력
#     """
#     model = Product  # Product 모델을 사용하여 상세 내용을 출력

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from ..forms import ProductForm
from ..models import Product, Category


# from sales.ai_system.ai_sales import start_ai
# from sales.ai_system.ai_sales import start_ai

########################################################################################################

@login_required(login_url='common:login')
def product_create_view(request):
    """ 판매 질문 등록 POST 요청 시 제품 정보를 처리하고,
    카테고리도 함께 저장합니다. """
    categories = Category.objects.all()  # 모든 카테고리 가져오기

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # 파일 업로드 처리

        if form.is_valid():
            product = form.save(commit=False)  # 데이터베이스에 저장하지 않고, 객체만 반환
            product.pcategory = form.cleaned_data['pcategory']
            product.author = request.user  # 작성자는 현재 로그인한 사용자
            product.pname = form.cleaned_data['pname']  # Fixed here
            product.punitprice = form.cleaned_data['punitprice']
            product.pdiscountrate = form.cleaned_data['pdiscountrate']
            product.create_date = timezone.now()  # 현재 시간을 질문 작성일로 저장

            if Product.objects.filter(pcode=product.pcode).exists():
                return JsonResponse({'error': '이미 사용된 제품 코드입니다.'}, status=400)  # 중복 코드 에러 처리
            # 이미지가 업로드된 경우 처리
            if 'image01' in request.FILES:
                product.image01 = request.FILES['image01']
            print('request.FILES : ', request.FILES)

            product.save()  # 최종적으로 질문을 데이터베이스에 저장
            return JsonResponse({'redirect_url': reverse('sales:index')})  # 성공 시 JsonResponse로 리다이렉트 URL 반환

        else:
            print('form.errors : ', form.errors)
            return JsonResponse({'error': '유효하지 않은 입력입니다.'}, status=400)  # 폼이 유효하지 않은 경우, 에러 메시지 반환
    else:  # GET 요청일 경우
        form = ProductForm()
        existing_products = Product.objects.all()  # 제품 코드 생성 로직
        if existing_products:
            last_product = existing_products.order_by('-pcode').first()
            next_pcode = int(last_product.pcode) + 1  # 마지막 제품 코드에 1을 더함
        else:
            next_pcode = 1

    next_pcode_str = str(next_pcode).zfill(4)  # 첫 번째 제품일 경우 0으로 설정

    context = {
        'form': form,
        'categories': categories,  # 카테고리 목록 추가
        'next_pcode': next_pcode_str
    }
    return render(request, 'sales/product_form.html', context)

@login_required(login_url='common:login')
def product_modify(request, product_id):
    """ sales 질문 수정 """
    # 수정할 질문을 가져옴, 없으면 404 에러 발생
    product = get_object_or_404(Product, pk=product_id)

    # 현재 로그인한 사용자가 작성자가 아닌 경우 에러 메시지 반환
    if request.user != product.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('sales:detail', product_pcode=product.pcode)

    # POST 요청이면 수정 처리
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.modify_date = timezone.now()  # 수정일시 저장
            product.save()  # 수정된 질문 저장
            return JsonResponse({'redirect_url': reverse('sales:detail', args=[product.pcode])})
    else:
        # GET 요청이면 기존 데이터를 폼에 담아서 전달
        form = ProductForm(instance=product)

    # 템플릿에 폼을 전달하여 렌더링
    context = {'form': form}
    return render(request, 'sales/product_form.html', context)

# ########################################################################################################

@login_required(login_url='common:login')
def product_delete(request, product_id):
    """ sales 질문 삭제 """
    # 삭제할 질문을 가져옴, 없으면 404 에러 발생
    product = get_object_or_404(Product, pk=product_id)

    # 현재 로그인한 사용자가 작성자가 아닌 경우 에러 메시지 반환
    if request.user != product.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('sales:detail', product_id=product.pcode)

    # 질문 삭제 후 메인 페이지로 리다이렉트
    product.delete()
    return redirect('sales:index')


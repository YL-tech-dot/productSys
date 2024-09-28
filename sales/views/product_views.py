from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from ..forms import ProductForm
from ..models import Product

# from sales.ai_system.ai_sales import start_ai
# from sales.ai_system.ai_sales import start_ai

########################################################################################################

@login_required(login_url='common:login')
def product_create(request):
    """ sales 질문 등록 """
    # POST 요청이면 폼 데이터 처리
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # 파일 업로드 처리
        # 폼이 유효한 경우
        if form.is_valid():
            product = form.save(commit=False)  # 데이터베이스에 저장하지 않고, 객체만 반환
            # 'pcode', 'pname', 'punitprice', 'pdiscountrate', 'pimage01'
            product.author = request.user  # 작성자는 현재 로그인한 사용자
            product.pcode = request.pcode
            product.pname = request.pname
            product.punitprice = request.punitprice
            product.pdiscountrate = request.pdiscountrate
            product.pcategories = request.pcategories
            product.create_date = timezone.now()  # 현재 시간을 질문 작성일로 저장
            product.save()
            
            if 'image01' in request.FILES:
                product.image01 = request.FILES['image01']
            product.save()  # 최종적으로 질문을 데이터베이스에 저장
            # 성공 시 JsonResponse로 리다이렉트 URL 반환
            return JsonResponse({'redirect_url': reverse('sales:index')})

        else:
            # 폼이 유효하지 않은 경우, 에러 메시지 반환
            return JsonResponse({'error': form.errors}, status=400)
            # 이미지가 업로드된 경우 AI 처리 수행
            # if product.image1:
            #     image_path = product.image1.path  # 업로드된 이미지 경로 가져오기
            #
            #     # 탐지기 및 예측기 목록을 POST 요청에서 가져옴
            #     selected_detectors = request.POST.getlist('detectors')
            #     selected_predictors = request.POST.getlist('predictors')
            #
                # 탐지기나 예측기가 선택되었는지 확인
                # if selected_detectors or selected_predictors:
                #     # AI 모델을 이용해 이미지 처리
                #     result_image_path = start_ai(request, image_path, selected_detectors, selected_predictors)
                #     # result_image_path = start_ai(request, image_path, selected_detectors, selected_predictors)
                #     # AI 처리 결과를 포함한 답변 생성
                #     answer = Answer(
                #         product=product,
                #         author=request.user,
                #         content="AI가 처리한 얼굴 인식 결과입니다.",
                #         answer_image=result_image_path,
                #         create_date=timezone.now(),
                #     )
                #     answer.save()  # 답변 저장
            # 이미지 파일 저장
    else:
        # GET 요청일 경우 빈 폼 생성
        form = ProductForm()
    
    # 템플릿에 폼을 전달하여 렌더링
    context = {'form': form}
    return render(request, 'sales/product_form.html', context)

# @login_required(login_url='common:login')
# def product_modify(request, product_id):
#     """ sales 질문 수정 """
#     # 수정할 질문을 가져옴, 없으면 404 에러 발생
#     product = get_object_or_404(Product, pk=product_id)
#
#     # 현재 로그인한 사용자가 작성자가 아닌 경우 에러 메시지 반환
#     if request.user != product.author:
#         messages.error(request, '수정권한이 없습니다')
#         return redirect('sales:detail', product_id=product.id)
#
#     # POST 요청이면 수정 처리
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.modify_date = timezone.now()  # 수정일시 저장
#             product.save()  # 수정된 질문 저장
#             return JsonResponse({'redirect_url': reverse('sales:detail', args=[product.id])})
#     else:
#         # GET 요청이면 기존 데이터를 폼에 담아서 전달
#         form = ProductForm(instance=product)
#
#     # 템플릿에 폼을 전달하여 렌더링
#     context = {'form': form}
#     return render(request, 'sales/product_form.html', context)
#
# ########################################################################################################
#
# @login_required(login_url='common:login')
# def product_delete(request, product_id):
#     """ sales 질문 삭제 """
#     # 삭제할 질문을 가져옴, 없으면 404 에러 발생
#     product = get_object_or_404(Product, pk=product_id)
#
#     # 현재 로그인한 사용자가 작성자가 아닌 경우 에러 메시지 반환
#     if request.user != product.author:
#         messages.error(request, '삭제권한이 없습니다')
#         return redirect('sales:detail', product_id=product.id)
#
#     # 질문 삭제 후 메인 페이지로 리다이렉트
#     product.delete()
#     return redirect('sales:index')
#
from django import forms
from sales.models import Product, Category


class CategoryForm(forms.ModelForm):
    """카테고리 생성을 위한 폼."""

    class Meta:
        model = Category
        fields = ['name']


# ===================================
# ProductForm (질문 생성 및 수정 폼)
# ===================================
class ProductForm(forms.ModelForm):
    """제품 생성 및 수정을 위한 폼으로, 카테고리 선택을 위한 ModelChoiceField를 포함하고 있습니다."""
    pcategory = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="-- 카테고리 선택 --",  # 기본 옵션을 설정
        label='카테고리',
        required=True
    )
    pname = forms.CharField(
        required=True,
        max_length=20,  # 길이 제한 추가
        error_messages={'required': '제품명을 입력해 주세요.'}
    )
    image01 = forms.ImageField(
        required=True,
        error_messages={'required': '이미지를 업로드해 주세요.'}
    )

    class Meta:
        model = Product
        fields = ['pcode', 'pname', 'pcontent', 'punitprice', 'pdiscountrate', 'image01']
        labels = {
            'pcode': '제품코드',
            'pname': '제품명',
            'pcontent': '제품설명',
            'punitprice': '단가',
            'pdiscountrate': '할인율',
            'image01': '이미지01',
            # pcategory 대한 라벨은 forms.ModelChoiceField에서 정의함.
        }



# ===================================
# AnswerForm (답변 생성 및 수정 폼)
# ===================================
# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer  # 이 폼이 Answer 모델과 연결됨
#         fields = ['content', 'answer_image']  # 사용할 필드 (답변 내용, 첨부 이미지)
#
#         # 각 필드에 표시될 라벨을 정의
#         labels = {
#             'content': '답변내용',
#             'answer_image': '이미지',
#         }


# ===================================
# CommentForm (댓글 및 대댓글 폼)
# ===================================
# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment  # 이 폼이 Comment 모델과 연결됨
#         fields = ['content', 'parent']  # 사용할 필드 (댓글 내용, 부모 댓글)
#
#         # 각 필드에 표시될 라벨을 정의
#         labels = {
#             'content': '내용',
#         }
#
#     # 폼 초기화 시 부모 댓글을 처리하기 위한 생성자
#     def __init__(self, *args, **kwargs):
#         self.parent_comment = kwargs.pop('parent_comment', None)  # 부모 댓글을 kwargs에서 분리
#         super().__init__(*args, **kwargs)
#
#     # 댓글 저장 시 부모 댓글을 설정하는 save 메서드
#     def save(self, commit=True):
#         comment = super().save(commit=False)  # 기본 save 메서드 호출 전에 데이터베이스에 저장하지 않음
#         if self.parent_comment:
#             comment.parent = self.parent_comment  # 부모 댓글이 존재하면 이를 설정
#         if commit:
#             comment.save()  # 데이터베이스에 댓글 저장
#         return comment

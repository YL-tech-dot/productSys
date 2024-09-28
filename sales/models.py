import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Category'  # 단수형
        verbose_name_plural = 'Categories'  # 복수형

    def __str__(self):
        return self.name


# ==========================
# Question 모델 (질문 데이터)
# ==========================
class Product(models.Model):
    """ 제품 모델 """
    # 작성자: User 모델과 다대일 관계 (1명의 사용자가 여러 질문을 작성할 수 있음)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_Product')
    pcode = models.CharField(max_length=4, unique=True, blank=False)
    pname = models.CharField(max_length=20, blank=False)
    punitprice = models.PositiveIntegerField(blank=False)
    pdiscountrate = models.DecimalField(max_digits=3, decimal_places=1, blank=False)  # 할인율
    pcategories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    pcontent = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, auto_now_add=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    image01 = models.ImageField(upload_to='sales/image1/', null=False, blank=False, verbose_name='업로드 이미지1')

    # 이미지1: 질문에 첨부된 첫 번째 이미지, null과 빈 값을 허용하지 않음

    def save(self, *args, **kwargs):
        """ save 메서드를 오버라이드기존 이미지가 있는 경우, 새 이미지로 교체할 때 이전 파일 삭제 """
        self.clean()  # 추가
        if self.pk:
            old_objects = Product.objects.get(pk=self.pk)
            if old_objects.image01 and old_objects.image01 != self.image01:
                if os.path.isfile(old_objects.image01.path):
                    os.remove(old_objects.image01.path)
        super().save(*args, **kwargs)  # Super호출시 클래스 이름을 명시할 필요없지만, 명시적 사용.

    def delete(self, *args, **kwargs):
        # 인스턴스가 삭제될 때 이미지 파일도 삭제
        if self.image01:
            if os.path.isfile(self.image01.path):
                os.remove(self.image01.path)

        # 기본 delete 메서드 호출
        super(self).delete(*args, **kwargs)

    # 할인율 유효성 검사 (0 ~ 100 사이의 값)
    def clean(self):
        if self.pdiscountrate < 0 or self.pdiscountrate > 100:
            raise ValidationError('할인율은 0에서 100 사이의 값이어야 합니다.')

    # 호출될시 디버깅시 다음 이름과 가격을 나타냄.
    def __str__(self):
        return f"{self.pname} - {self.punitprice}원 ({self.pdiscountrate}%)"


@receiver(post_save, sender=Product)
def set_product_code(sender, instance, created, **kwargs):
    """sender :
        어떤 모델 수신할지 지정!  product모델에서 post_save신호를 수신중.
        현재 코드에서 sender 직접 사용하지 않지만 다른 로직에서 조건을 추가할때 유용함.
        어떤 모델 인스턴스에서 호출되었는지를 확인하는데 사용됨.

        **kwargs :
        추가 키워드 인자를 받아들이기 위함. Django 신호는 다양한 추가 정보 제공가능함.
        ex: 신호 발생 시점의 추가 정보. 나중 대비.

        instance :
        Product 모델의 인스턴스가 저장된 후에 호출된는 것. 새 인스턴스가 생성될 때 (created가 True일 때)
        제품 코드가 설정되지 않았다면, 새로운 제품 코드를 생성. instance는 이 로직에서 핵심적인 역할을 하며, 어떤 객체에 대한 작업이 이루어질지를 명확하게 해줍니다. """

    print('instance 진입.')
    print(instance)
    if created and not instance.pcode:
        existing_codes = Product.objects.exclude(pcode='').values_list('pcode', flat=True)
        existing_numbers = [int(code) for code in existing_codes if code.isdigit()]

        if existing_numbers:
            next_number = max(existing_numbers) + 1
        else:
            next_number = 0  # 첫 번째 코드로 0을 사용

        instance.pcode = str(next_number).zfill(4)  # 4자리 문자열로 설정
        instance.save()

# category = Category.objects.get(name='sales_product')  # 카테고리 가져오기
# product = Product(
#     author='admin',
#     pcode='0001',
#     pname='새로운 제품',
#     punitprice=10000,
#     pdiscountrate=10,
#     pcategories=category,  # 카테고리 할당
#     pcontent='제품 설명',
# )
# product.save()
# 유용한 기능 설명
"""
0. 각 모델의 속성을 정하는 필드(Field)는 DB의 컬럼이다.
    - models.ForeignKey
    - models.CharField
    - models.PositiveIntegerField (정수)
    - models.DecimalField (소수 + 자리수 설정)
    - models.TextField
    - models.DateTimeField
    - models.ImageField

1. 장고의 신호(signal)는 클래스 인스턴스가 아닌 클래스 자체와 연결된다.
업뎃이 일어날때 특정 작업을 수행하기 위한 것임. 클래스 메서드일 경우 인스턴스 정보에 접근하기 어려움.
코드의 분리: 신호를 사용하는 패턴에서 관련없는 로직 함수로 분리함.

2. on_delete=models.CASCADE: User가 삭제되면 관련 질문도 함께 삭제됨

3. 프로필 삭제시 다른 데이터 삭제
@receiver(pre_delete, sender=UserProfile)
def delete_related_data(sender, instance, **kwargs):
    # 프로필이 삭제되면 관련된 다른 데이터를 삭제
    instance.user.comments.all().delete()  # 사용자의 모든 댓글 삭제
    print(f"{instance.user.username}님의 모든 댓글이 삭제되었습니다.") """

# 설명용 by YL
""" 기존 장고 교재의 필드 속성 외에도 카테고리, 제품 번호, 할인율 등의 속성을 활용하여 추가했다.
"""
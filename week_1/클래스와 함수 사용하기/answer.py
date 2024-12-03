# Person 클래스 생성
class Person:
    # 생성자 메서드
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender             # 문제에선 생성자에서 성별 유효성판단을 하라하였지만 가독성이 더 떨어진것같아서 밑에서진행
        self.age = age

    # 정보출력 메서드
    def display(self):
        return print(f"이름 : {self.name}, 성별 : {self.gender}\n나이 : {self.age}")

    # 인사메시지 메서드
    def greet(self):
        if self.age >= 20:
            print(f"안녕하세요, {self.name}! 성인이시군요!")
        else:           # age 가 정수형이지만 밑에서 유효성판단하면서 양의정수만 받아오기로해서 0살밑으로는 X
            print(f"안녕하세요, {self.name}! 미성년자시군요!")
            

# 사용자 나이 받아오기
while True:
    user_age = input("나이 : ")

    # 매개변수 age 가 정수형이라 숫자만 -> 나이라서 0, 음의정수, 150살 초과은 포함안시키기위한 유효성판단
    if user_age.isdigit() and 0 < int(user_age) <= 150:
        user_age = int(user_age)
        break
    else:
        print("'나이'에 맞는 값을 입력하세요! ( 1~150 사이의 숫자 )")

# 사용자 이름 받아오기 ( 이름에 외국인, 릴스나 쇼츠에 올라오는 숫자가들어간사람들 때문에 str타입은 예외처리 일부로 X ) -> 특수문자는 해야하나? 너무지엽적인데
user_name = input("이름 : ")

# 사용자 성별 받아오기
while True:
    user_gender = input("성별 : ")

    if user_gender.lower() not in ['male', 'female']:
        print("잘못된 성별을 입력하셨습니다. 'male' 또는 'female'을 입력하세요.")
        continue
    else:
        user_gender = user_gender.lower()
        break

# 객체생성
person_user = Person(user_name, user_gender, user_age)

# 정보출력
person_user.display()
# 인사메시지 출력
person_user.greet()

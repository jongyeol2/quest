import random

# 게임진행 반복을 위한 flag 설정
restart = 'y'

while restart == 'y':
    # 1~10 사이의 랜덤한 숫자 생성
    random_num = random.randint(1, 10)
    
    print("""1과 10 사이의 숫자를 하나 정했습니다.
    이 숫자는 무엇일까요?""")
    
    while True:
        # 사용자 입력 받아오기
        user_answer = input("예상 숫자 : ")
    
        # 유효성 검사
        if user_answer.isdigit() and 1 <= int(user_answer) <= 10:
            user_num = int(user_answer)
        else:
            print("1~10 사이의 숫자가 아닙니다. 다시 입력해주세요!")
            continue     # 다시입력받아오기위해 반복문 처음으로 돌아감
    
        # 사용자숫자와 랜덤숫자와 대소비교
        if user_num > random_num:
            print("너무 큽니다. 다시 입력하세요.")
        elif user_num < random_num:
            print("너무 작습니다. 다시 입력하세요.")
        else:
            print("정답입니다!")
            break  # 정답을 맞췄을 때 게임 진행 여부를 묻기 위해 루프를 종료

    # 추가 게임 진행 여부 확인
    while True:
        restart = input("게임을 다시 하시겠습니까? (y/n) : ").lower()

        if restart not in ['y', 'n']:
            print("y 또는 n 으로 입력해주세요")
        elif restart == 'y':
            print("게임을 다시 시작합니다.")
            break    # y를 입력했을 경우 바로 다음 게임을 시작하기 위해 종료 -> 맨위 반복문 루프 반복
        elif restart == 'n':
            print("게임을 종료합니다.")
            break   # 게임을 종료하려면 루프를 빠져나옴 -> flag 값이 변경되어  맨위 반복문루프도 자동탈출

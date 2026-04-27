# 파일이름 : task_2_60232296
# 작 성 자 : Yeon_Gi_Jeong
# [스마트 캠퍼스 열람실 통합 예약 시스템]

# 이미 예약된 좌석 번호 리스트 (상황부여)
reserved_seats = [10, 21, 45] 

print("=" * 60)
print("     [ SMART CAMPUS LIBRARY SEAT RESERVATION ]")
print("   본 프로그램은 열람실 좌석 예약 및 이용 시간을 관리합니다.")
print("=" * 60)

# 1. 사용자 정보 입력
user_name = input("예매자 성함: ")
student_id = input("학번: ")

# 2. 열람실 구역 선택 (중첩 조건문 활용)
print("\n[ 층수 선택 ]")
print("1. 1층 (노트북 전용 구역)")
print("4. 4층 (일반 및 대학원 구역)")
floor = input("원하시는 층수를 입력하세요 (1 또는 4): ")

room_name = ""

# --- 층별/구역별 선택 로직 ---
if floor == "1":
    print("\n[ 1층 열람실 목록 ]")
    print("1. 노트북 열람실")
    select = input("번호 선택: ")
    if select == "1":
        room_name = "1층 노트북 열람실"

elif floor == "4":
    print("\n[ 4층 열람실 목록 ]")
    print("1. 제 2열람실")
    print("2. 제 4열람실")
    print("3. 대학원 열람실")
    print("4. 제 2노트북 열람실")
    select = input("원하시는 열람실 번호를 입력하세요 (1~4): ")
    
    if select == "1":
        room_name = "4층 제 2열람실"
    elif select == "2":
        room_name = "4층 제 4열람실"
    elif select == "3":
        room_name = "4층 대학원 열람실"
    elif select == "4":
        room_name = "4층 제 2노트북 열람실"

# 3. 좌석 중복 확인 및 시간 입력
if room_name != "":
    print(f"\n선택된 구역: {room_name}")
    seat_num = int(input("희망 좌석 번호(1~100): "))
    
    # (match_count 방식)
    match_count = 0
    for s in reserved_seats:
        if s == seat_num:
            match_count = match_count + 1
            
    if match_count > 0:
        print(f"\n❌ 예약 실패: {seat_num}번 좌석은 이미 사용 중입니다.")
    else:
        print(f"✅ {seat_num}번 좌석은 예약 가능합니다.")
        
        # 시간 입력 (형변환 TypeError 방지)
        start_h = int(input("입실 시간(시): "))
        start_m = int(input("입실 시간(분): "))
        end_h = int(input("퇴실 예정 시간(시): "))
        end_m = int(input("퇴실 예정 시간(분): "))
        
        # 시간 가중치 연산 (전체 분 단위 변환)
        start_total = start_h * 60 + start_m
        end_total = end_h * 60 + end_m
        use_time = end_total - start_total
        
        if use_time > 0:
            # 4. 예약 결과 출력 (반복문 range 활용)
            print("\n" + "*" * 20 + " 예약 확인서 " + "*" * 20)
            labels = ["이름", "학번", "예약 좌석", "이용 시간"]
            values = [user_name, student_id, f"{room_name} {seat_num}번", f"{use_time // 60}시간 {use_time % 60}분"]
            
            for i in range(len(labels)):
                print(f"{labels[i]}: {values[i]}")
            print("*" * 53)
            
            # 5. 잔여 시간 확인 기능 (시나리오 반영)
            print("\n현재 시각을 입력하여 잔여 시간을 확인하시겠습니까?")
            confirm = input("확인하시려면 'Y'를 입력하세요: ")
            
            if confirm.upper() == 'Y':
                now_h = int(input("현재 시간(시): "))
                now_m = int(input("현재 시간(분): "))
                
                remain = end_total - (now_h * 60 + now_m)
                
                if remain > 0:
                    print(f"잔여 시간: {remain // 60}시간 {remain % 60}분 남았습니다.")
                elif remain == 0:
                    print("❗ 이용 시간이 종료되었습니다. 퇴실해 주세요.")
                else:
                    print("⚠️ 이용 시간이 이미 초과되었습니다!")
        else:
            print("오류: 퇴실 시간이 입실 시간보다 빠를 수 없습니다.")
else:
    print("구역 선택이 잘못되었습니다. 프로그램을 다시 실행해 주세요.")

print("\n시스템을 종료합니다. 즐거운 학습 되세요!")

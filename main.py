# 파일이름 : task_2_60232296
# 작 성 자 : Yeon_Gi_Jeong
# [스마트 캠퍼스 열람실 통합 예약 시스템]

# 시스템 기본 정보 및 실시간 상태 설정
system_name = "캠퍼스 스마트 예약"
manager_name = "mju_ㅡmaru"
current_version = 3.5
library_congestion = 65.5  
max_seats_limit = 100      

# 이미 예약되어 사용 중인 초기 좌석 리스트
reserved_seats = [12, 25, 48]

print(f"[{system_name} v{current_version}] 시스템에 접속했습니다.")
print(f"담당자: {manager_name} | 실시간 혼잡도: {library_congestion}%")

# 오늘 공부할 과목 리스트 입력 및 저장
print("\n" + "-"*15 + " [오늘 공부할 과목 설정] " + "-"*15)
subject_list = []
for i in range(3):
    subject = input(f"오늘 공부할 {i+1}순위 과목명: ")
    subject_list.append(subject)

# 사용자 인적사항 및 목표 학습 시간 설정
print("\n" + "-"*15 + " [사용자 정보 입력] " + "-"*15)
user_name = input("예매자 성함: ")
student_id = int(input("학번 8자리를 입력하세요: "))

# 목표 시간과 분을 따로 입력받아 실수(float) 데이터로 계산
print("\n목표로 하는 총 공부 시간을 설정합니다.")
goal_h = int(input("목표 시간(시): "))
goal_m = int(input("목표 시간(분): "))
target_study_time = float(goal_h + (goal_m / 60)) 

print(f"오늘의 목표 시간은 {target_study_time:.1f}시간입니다. 화이팅!")

# 층수 및 세부 열람실 선택 (중첩 조건문 활용)
print("\n[층 선택] 1. 1층(노트북실) | 4. 4층(일반열람실)")
floor = input("선택: ")
room_name = ""

if floor == "1":
    room_name = "1층 노트북 열람실"
elif floor == "4":
    print("\n[4층 세부 구역] 1.제2열람실 | 2.제4열람실 | 3.대학원실 | 4.제2노트북실")
    choice = input("번호 선택: ")
    if choice == "1": 
        room_name = "4층 제2열람실"
    elif choice == "2": 
        room_name = "4층 제4열람실"
    elif choice == "3": 
        room_name = "4층 대학원실"
    else: 
        room_name = "4층 제2노트북실"
else:
    print("잘못된 선택입니다.")

# 좌석 중복 검증 및 예약 확정 로직
if room_name != "":
    seat_num = int(input(f"\n{room_name} 좌석 번호(1-{max_seats_limit}): "))
    
    # 입력한 좌석 번호가 운영 범위 내에 있는지 확인
    if (seat_num < 1) or (seat_num > max_seats_limit):
        print("좌석 번호를 다시 확인해 주세요.")
    else:
        # 반복문을 이용해 기존 예약 데이터와 대조
        match_count = 0
        for s in reserved_seats:
            if s == seat_num:
                match_count += 1 
        
        # 중복 좌석 여부에 따른 예약 승인 처리
        if not (match_count == 0):
            print(f"예약 실패: {seat_num}번은 이미 사용 중인 좌석입니다.")
        else:
            # 새로운 예약을 리스트에 추가하고 데이터 정렬 및 분석
            reserved_seats.append(seat_num)
            reserved_seats.sort()
            total_reserved = len(reserved_seats)
            last_seat = max(reserved_seats)
            
            print(f"\n[이용 시간 설정]")
            sh = int(input("입실(시): "))
            sm = int(input("입실(분): "))
            eh = int(input("퇴실(시): "))
            em = int(input("퇴실(분): "))
            
            # 입실 시간과 퇴실 시간을 분 단위로 환산하여 계산
            total_min = (eh * 60 + em) - (sh * 60 + sm)
            
            if total_min > 0:
                print("\n" + "="*45)
                print(f"▶ {user_name}님(학번:{student_id}) 예약 완료")
                print(f"▶ 위치: {room_name} {seat_num}번")
                print(f"▶ 이용 시간: {total_min // 60}시간 {total_min % 60}분")
                print(f"▶ 전체 예약 인원: {total_reserved}명 / 마지막 좌석: {last_seat}번")
                print("="*45)

                # 현재 시각을 입력받아 남은 이용 시간을 계산
                now_h = int(input("\n현재 시: "))
                now_m = int(input("현재 분: "))
                
                rem_min = (eh * 60 + em) 
                rem_min -= (now_h * 60 + now_m) 
                
                if rem_min > 0:
                    print(f"잔여 시간: {rem_min // 60}시간 {rem_min % 60}분 남았습니다.")
                else:
                    print("이용 시간이 이미 종료되었습니다.")
                
                # 사용자가 설정한 오늘 공부할 과목 리스트 출력
                print("\n--- [오늘 공부할 과목] ---")
                for sub in subject_list:
                    print(f"과목: {sub}")
            else:
                print("오류: 퇴실 시간이 입실 시간보다 빠를 수 없습니다.")

print(f"\n[{manager_name}] 시스템을 종료합니다. 목표 달성을 응원합니다!")

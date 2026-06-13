# 파일이름 : last_homework_60232296
# 작 성 자 : Yeon_Gi_Jeong
# [스마트 캠퍼스 열람실 통합 예약 시스템]

system_name = "캠퍼스 스마트 예약"
manager_name = "mju_maru"
current_version = 4.0
library_congestion = 65.5  
max_seats_limit = 100      
reserved_seats = [12, 25, 48] 

# 모든 예약 데이터를 저장할 글로벌 이중 리스트 
all_reservations = []

# 사용자 개인정보 및 예약 세션 저장을 위한 전역 변수 
user_name = ""
student_id = 0
subject_list = []
target_study_time = 0.0

booked_room = ""
booked_seat = 0
checkout_h = 0
checkout_m = 0
is_booked = False 

# 사용자 정보 및 학습 목표 설정
def setup_user_profile():
    global user_name, student_id, subject_list, target_study_time
    
    print("\n" + "-"*15 + " [사용자 정보 및 학습 목표 설정] " + "-"*15)
    user_name = input("예매자 성함: ")
    
    # 숫자가 아닌 문자 입력 시 ValueError 처리
    try:
        student_id = int(input("학번 8자리를 입력하세요: "))
    except ValueError:
        print("\n[오류] 학번은 반드시 숫자로만 입력해야 합니다. 메뉴로 돌아갑니다.")
        user_name = "" # 예외 발생 시 세션 초기화
        return 0.0
        
    # 리스트 활용을 통한 과목 입력 로직을 한 줄로 단축 
    subject_list = [input(f"오늘 공부할 {i+1}순위 과목명: ") for i in range(3)]
        
    # 목표 시간을 입력받아 실수형 데이터로 계산
    print("\n목표로 하는 총 공부 시간을 설정합니다.")
    
    # 목표 시간 입력 숫자가 아닐 시 예외 처리
    try:
        goal_h = int(input("목표 시간(시): "))
        goal_m = int(input("목표 시간(분): "))
    except ValueError:
        print("\n[오류] 목표 시간은 숫자로 입력해 주세요. 프로필 등록이 취소됩니다.")
        user_name = ""
        return 0.0
        
    target_study_time = float(goal_h + (goal_m / 60))
    
    print(f"오늘의 목표 시간은 {target_study_time:.1f}시간으로 설정되었습니다.")
    return target_study_time 

# 시/분 데이터를 분 단위 데이터로 환산 (기존 유지)
def calculate_minutes(hour, minute):
    total_minutes = (hour * 60) + minute
    return total_minutes 

# 좌석 중복 검증 및 예약 확정
def reserve_seat():
    global reserved_seats, booked_room, booked_seat, checkout_h, checkout_m, is_booked, all_reservations
    
    # 사용자 정보가 없으면 예약 불가
    if user_name == "":
        print("\n[알림] 1번 메뉴에서 사용자 정보 및 목표 설정을 먼저 완료해 주세요.")
        return

    print("\n[층 선택] 1. 1층(노트북실) | 4. 4층(일반열람실)")
    floor = input("선택: ")
    room_name = ""

    # 계층형 중첩 조건문 구조
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
        print("잘못된 선택입니다. 메인 메뉴로 돌아갑니다.")
        return

    # 좌석 번호 및 이용 시간 입력 시 ValueError 처리
    try:
        seat_num = int(input(f"\n{room_name} 좌석 번호(1-{max_seats_limit}): "))
    except ValueError:
        print("[오류] 좌석 번호는 숫자로만 입력할 수 있습니다.")
        return

    if not (1 <= seat_num <= max_seats_limit):
        print("좌석 운영 범위를 벗어났습니다.")
        return

    if seat_num in reserved_seats:
        print(f"예약 실패: {seat_num}번은 이미 사용 중인 좌석입니다.")
    else:
        # 리스트 조작 내장 함수 및 메소드 활용 
        reserved_seats.append(seat_num)
        reserved_seats.sort()
        total_reserved = len(reserved_seats)
        last_seat = max(reserved_seats)
        
        # 이용 시간 입력 예외 처리 감싸기
        try:
            print(f"\n[이용 시간 설정]")
            sh = int(input("입실(시): "))
            sm = int(input("입실(분): "))
            eh = int(input("퇴실(시): "))
            em = int(input("퇴실(분): "))
        except ValueError:
            print("[오류] 시간/분은 반드시 숫자로 입력해 주세요. 예약을 취소합니다.")
            reserved_seats.remove(seat_num) # 예외 발생 시 추가했던 좌석 회수
            return
        
        # [함수 호출 및 매개변수 전달]
        start_total = calculate_minutes(sh, sm)
        end_total = calculate_minutes(eh, em)
        total_min = end_total - start_total
        
        if total_min > 0:
            # 영구적인 조회를 위해 전역 세션 변수에 예약 정보 기록
            booked_room = room_name
            booked_seat = seat_num
            checkout_h = eh
            checkout_m = em
            is_booked = True
            
            # 이중 리스트 구조에 append로 데이터 누적 
            # 데이터 구조: [이름, 학번, 이용장소, 좌석번호, 퇴실시간(시), 퇴실시간(분)]
            new_reservation = [user_name, student_id, booked_room, booked_seat, checkout_h, checkout_m]
            all_reservations.append(new_reservation)
            
            print("\n" + "="*45)
            print(f"▶ {user_name}님(학번:{student_id}) 예약 완료")
            print(f"▶ 위치: {booked_room} {booked_seat}번")
            print(f"▶ 총 이용 예정 시간: {total_min // 60}시간 {total_min % 60}분")
            print(f"▶ 실시간 전체 예약 인원: {total_reserved}명 / 최종 예약 좌석: {last_seat}번")
            print("="*45)
        else:
            print("오류: 퇴실 시간이 입실 시간보다 빠를 수 없습니다.")


# while True 무한루프 기반의 키오스크 제어

print(f"[{system_name} v{current_version}] 시스템에 정상 접속했습니다.")
print(f"시스템 관리자: {manager_name} | 실시간 도서관 혼잡도: {library_congestion}%")

while True:
    print("\n" + "="*15 + " 스마트 캠퍼스 메인 메뉴 " + "="*15)
    print("1. 사용자 정보 및 학습 목표 설정")
    print("2. 열람실 좌석 예약하기")
    print("3. 나의 예약 현황 및 잔여 시간 조회 (전체 명단 포함)")
    print("4. 시스템 안전 종료 (데이터 파일 저장)")
    print("="*47)
    
    menu_choice = input("원하시는 서비스 번호를 선택하세요: ")
    
    if menu_choice == "1":
        setup_user_profile()
        if user_name != "":
            print("\n[알림] 기본 프로필 등록이 완료되었습니다.")
        
    elif menu_choice == "2":
        reserve_seat()
        
    elif menu_choice == "3":
        print("\n" + "-"*15 + " [나의 실시간 이용 현황] " + "-"*15)
        if user_name == "":
            print("등록된 사용자 정보가 없습니다. 1번 메뉴를 먼저 실행해 주세요.")
        elif not is_booked:
            print(f"▶ 이용자: {user_name}님 (학번: {student_id})")
            print(f"▶ 설정된 목표 시간: {target_study_time:.1f}시간")
            print("▶ 알림: 현재 예약된 좌석 정보가 없습니다. 2번 메뉴에서 예약을 진행해 주세요.")
        else:
            # 예약 정보 및 오늘 공부할 과목 출력
            print(f"▶ 이용자명: {user_name}님 (학번: {student_id})")
            print(f"▶ 예약 위치: {booked_room} {booked_seat}번 좌석")
            print(f"▶ 오늘 목표 공부 시간: {target_study_time:.1f}시간")
            
            print("\n--- [오늘 학습 목표 과목] ---")
            for sub in subject_list:
                print(f"- {sub}")
             
            # 중첩 for문을 활용한 이중 리스트 표 데이터 깔끔하게 반복 출력
            print("\n" + "="*10 + " [시스템 전체 예약 현황 마스터 테이블] " + "="*10)
            print(f"{'이름':<6} | {'학번':<10} | {'열람실 위치':<18} | {'좌석':<4} | {'퇴실시간':<6}")
            print("-" * 55)
            
            # 이중 순회(중첩 for문) 구조 구현
            for row in all_reservations:
                # row 내부의 개별 데이터들을 순회 포맷팅 출력
                print(f"{row[0]:<6} | {row[1]:<10} | {row[2]:<18} | {row[3]:<4}번 | {row[4]:02d}:{row[5]:02d}")
            print("="*55)

            try:
                print("\n[실시간 잔여 시간 확인]")
                now_h = int(input("현재 시 입력: "))
                now_m = int(input("현재 분 입력: "))
            except ValueError:
                print("[오류] 현재 시간은 숫자로만 입력해야 조회가 가능합니다. 메인 메뉴로 이동합니다.")
                continue
            
            now_total = calculate_minutes(now_h, now_m)
            end_total = calculate_minutes(checkout_h, checkout_m)
            rem_min = end_total - now_total 
            
            if rem_min > 0:
                print(f"▶ [안내] 퇴실까지 {rem_min // 60}시간 {rem_min % 60}분 남았습니다.")
            else:
                print("▶ [안내] 설정하신 이용 시간이 이미 만료되어 좌석이 자동 반납되었습니다.")
                is_booked = False 
                
    elif menu_choice == "4":
        print(f"\n[{manager_name}] 스마트 예약 세션을 안전하게 종료 프로세스를 시작합니다.")
        
        # with open()을 사용하여 이중 리스트 데이터를 텍스트 파일로 저장
        try:
            with open("reservation_log.txt", "w", encoding="utf-8") as f:
                # 헤더 타이틀 작성
                f.write("이름,학번,열람실위치,좌석번호,퇴실시,퇴실분\n")
                
                # 이중 리스트를 순회하며 텍스트 파일에 csv 스타일(콤마 구분자)로 기록
                for res in all_reservations:
                    f.write(f"{res[0]},{res[1]},{res[2]},{res[3]},{res[4]},{res[5]}\n")
            print("[파일 저장 완료] 전체 예약 내역이 'reservation_log.txt' 파일에 안전하게 기록되었습니다.")
        except Exception as e:
            print(f"[오류 발생] 파일 저장 도중 예기치 못한 문제가 발생했습니다: {e}")
            
        print("목표 달성을 응원합니다! 프로그램을 종료합니다.")
        break
        
    else:
        print("\n[오류] 잘못된 접근입니다. 1번부터 4번 사이의 올바른 메뉴 번호를 입력해 주세요.")

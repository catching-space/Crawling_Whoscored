# Mini Project : Club Stats reporting service
 
 > Whoscored.com 내 특정 리그에 대한 league table data 및 team statistics(특정팀의 경기당 득점수, 평균 볼점유율 등)를 크롤링하여 데이터프레임을 제공하는 서비스 구현

### 1. 문제정의
 
- 시즌 현황파악 및 팀별 전력분석을 위한 league table data와 팀별 statistics를 통합한 서비스 제공 미비

### 2. 서비스 구현방안
 
- 사용자가 원하는 특정 리그를 입력할 시 해당 리그의 league table data와 팀별 statistics를 통합 제공하는 데이터 프레임 구현

### 3. 서비스 제공을 위한 'Whoscored' 클래스 구현

#### [클래스 구현중점]
- 코드 오류발생의 최소화, 가능한 모든 조건에서 실행 가능여부 확인
- 코드 오류발생의 최소화를 위해 누락데이터(None)가 다수 존재하는 최악조건의 리그를 기반으로 구현
- 최악의 조건하, 구현한 코드에서 예외 처리가 원활히 이루어지는지 확인하고자 위해 누락데이터(None)가 다수 존재하는 스페인 2부 리그 Segunda-Division을 대상으로 시현

### [함수별 기능요약]
 
1. init
 
   - 주요기능 : 클래스 내 전역으로 쓰일 변수 설정
 
   - 실행과정 :
 
       1) 최초 접속 URL 초기값 인자 설정
 
       2) headless 옵션 설정 (초기값 = True)
 
       3) fake_useragent 옵션 설정 (초기값 = True)
 
 
2. get_team_url
 
  - 주요기능 : 'https://www.whoscored.com/Regions/206/Tournaments/63/Spain-Segunda-Divisi%C3%B3n' URL 링크에서 Segunda Division Tables 내 팁별 URL 링크 크롤링

  - 실행과정 :

    1) css selector로 league table내 팀별 URL link element 수집

    2) 수집한 URL link element를 team_urls 리스트에 저장
    
    3) team_urls 변수를 리턴


3. get_league_table

- 주요기능 : 'https://www.whoscored.com/Regions/206/Tournaments/63/Spain-Segunda-Divisi%C3%B3n' URL 링크에서 Segunda Division Tables 내 팀별 순위 정보 크롤링

   - 실행과정 :

       1) css selector로 league table내 팀별 순위정보 수집

       2) 수집한 정보를 league_table 리스트에 저장
       
       3) league_table 변수를 리턴

4. get_team_information

   - 주요기능 : team_urls 리스트 내 팀별 URL을 순회하며 팀별 URL 내 team statistics 정보 수집

   - 실행과정 : 

       1) team_urls 리스트 내 팀별 URL을 순회

       2) 팀별 URL 내 team statistics 정보 수집 team_info 변수에 저장

       3) 일부 팀 URL 내 team statistics 정보가 없는 경우 예외처리(None값을 대체로 삽입), team_info 변수에 저장
       
       4) team_info 변수를 리턴


5. making_df

   - 주요기능 : league_table 리스트와 team_info 리스트를 병합하여 판다스 데이터 프레임으로 구현

   - 실행과정 :

       1) league_table 리스트와 team_info 리스트를 병합

       2) 판다스 데이터 프레임으로 구현 및 result 변수에 저장
       
       3) result 변수 리턴
       
6. crawling

   - 주요기능 : 2 ~ 5. 함수 순차적 실행명령 부여

   - 실행과정 :

       1) get_team_url함수 실행, 결과값을 self.team_urls에 저장

       2) get_league_table함수 실행 , 결과값을 self.league_table에 저장
       
       3) 1) 결과값을 참조하여 get_team_information함수 실행 , 결과값을 self.team_info에 저장
       
       4) 2),3) 결과값을 참조하여 making_df함수 실행, 결과값으로 result에 저장
       
       5) result 변수를 최종 리턴
       
7. df_columns_to_num

   - 주요기능 : 데이터 프레임 전처리를 위한 데이터타입 변경(문자형 -> 숫자)

   - 실행과정 :
   
       1) 데이터프레임을 인자로 입력하면 데이터 타입을 일괄적으로 numeric 형식으로 변경
       
       2) numeric 변경 불가한 타입은 데이터프레임에서 누락


### 4. 향후 개선 및 보완사항

1. 다른 리그의 데이터를 크롤링하기 위해서는 함수인자로 URL을 바꿔야하는데, 리그 별 URL의 규칙에 따른 기능 추가

2. 리그 별로 css 실렉트 시 아이디값(또는 클래스네임)이 상이한 문제점 보완필요

    - 예시) driver.find_elements_by_css_selector("#standings-16547-content tr") 
            #standings-'*****'-content에서 '*****'이 리그별로 상이함
    
3. 프로그램 안정성 보장필요
   - Abusing issue로 bs4를 사용하지 않고 Selenium을 활용했음에도 불구하고 Access Deined 다수발생, 근본적인 해결필요
   - Fake-useragent로 방지 불가
   - 서버접근시간을 늘려주는 방식으로 임시적으로 해결 (time.sleep()함수 이용)
   
4. 수집한 데이터를 가공해 통계적으로 분석하여 제공가능

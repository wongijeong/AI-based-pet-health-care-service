2023.05.20 / (카카오,네이버 제외) 구글 써드파티 기능 완료(아래 사이트에서 본인 OAUTH Client ID 등록해야함)
https://console.cloud.google.com/apis/credentials/oauthclient/628002652126-64cnr6t4enelcc04hjmoipcnusc850rh.apps.googleusercontent.com?project=capstone-387208
--> https://support.google.com/workspacemigrate/answer/9222992?hl=ko 여기 보고 따라하기(뭔 프로젝트를 만들어야됨)

+ 보안문제때문에 DB 아이디 비밀번호, SECRET_KEY, 구글 써드파티 클라이언트 아이디, 비밀번호 등을 환경변수에서 받아오는 구조로 바꿨음 (envs_example.sh 참조)

+ DB USER 모델에 profile_pic, name 칼럼 추가했음

+ 아래는 구글 써드파티 클라이언트 생성 참고자료

https://realpython.com/flask-google-login/#creating-a-google-client



******** 실행전 가상환경에 패키지(모듈) 설치 ********

pip3 install -r requirements.txt

***************

23/04/07 : 마리아 데이터베이스 모델 구축 완료. 플라스크앱의 웹 폼(사용자 입력정보)과 데이터베이스를 연계시키는 작업중

23/04/09 :

1. 데이터베이스 모듈(database_model.py)을 앱이랑 연동되도록 수정했음.
2. 로그인부분에서 웹브라우저에서 정보 받아올 수 있도록 contents/login.html을 jinja 이용하도록 수정했음.(css 보완하면좋은데 안해도될듯./)
3. 메인 코드(__init__.py) 에서 로그인/회원가입/비밀번호 재설정 페이지 라우팅 재설정했음./

23/04/16 :

마리아DB 메서드 참조
https://mariadb.com/resources/blog/using-sqlalchemy-with-mariadb-connector-python-part-1/


23/05/05 :

회원가입 페이지에서 입력시 DB에 등록하는것까지 완료


23 /05/13 :

로그인/로그아웃 기능 완료



****************마리아DB 초기 환경설정********************
1. 마리아DB/C 커넥터 설치
https://mariadb.com/docs/skysql-previous-release/connect/programming-languages/c/

2. 마리아DB/파이썬 커넥터 설치
https://mariadb.com/resources/blog/using-sqlalchemy-with-mariadb-connector-python-part-1/

3. 파이썬 가상환경(venv) 실행해서 requirements.txt 에 있는 모듈들 설치하기
pip3 install -r requirements.txt
(위는 리눅스용, 윈도우 커맨드는 pip install -r requirements.txt)

4. 데이터베이스에 'users' 라는 이름의 비어있는 데이터베이스 만들기

5. database_model 모듈의 
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://sunhwi:1234@127.0.0.1:3306/users")

이 부분에서 sunhwi:1234 <- 여기가 해당 (users) 데이터베이스의 사용자명/패스워드 부분임. -> 자기 DB설정에 맞게 사용자명/비밀번호 설정하기

6. 해당 사용자에게 DB 접근권한 부여하기(DB접속해서 아래 커맨드입력하기)

SELECT host,user from mysql.user;

CREATE USER 'sunhwi'@'localhost' identified by 'password123'; ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ//sunhwi, password123 부분 각자 맞게 설정하기

GRANT ALL ON *.* to 'sunhwi'@'localhost' WITH GRANT OPTION;

(GRANT ALL ON (별표).(별표)임 <- Readme에 별표가 안쳐지네 ;;

7. __init__.py 실행하면 'info' 이름의 사용자 정보 테이블 생성됨.

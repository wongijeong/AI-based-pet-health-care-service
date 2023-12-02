#!/bin/bash
#Setting environment variables for flask application

#Copy and paste in venv terminal prompt
#For windows, use 'set' instead of 'export'


# 환경변수 설정하기 (윈도우는 set / 리눅스는 export 사용)

# 일시적으로 구글과 http 커넥션 허용(0으로 설정시 ssl로 https 인증해야함) 
set OAUTHLIB_INSECURE_TRANSPORT=1

# SECRET_KEY : 랜덤스트링 생성하거나, 어려운 문자로 설정
set SECRET_KEY=g3oCwMxBDWKdRMx4JUucoB369MDsOj6xuUNNUDSKaI1KsKlMdL;

# 아래부분은 각자환경에 맞게 설정
set DB_USER=root;
set DB_PW=1234;
set GOOGLE_CLIENT_ID=47258694830-1vikigana4j8c6rkgpuqutb956lhh7om.apps.googleusercontent.com;
set GOOGLE_CLIENT_SECRET=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;


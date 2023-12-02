import json
from flask import (
	Flask,
	redirect,
	request,
	jsonify,
	render_template,
	session,
	url_for,
	flash
)
from flask_sock import Sock
from flask_login import (
	login_user,
	logout_user,
	login_required,
	LoginManager
)
from werkzeug.utils import secure_filename
import database_model as db_model
import os
import requests
import global_vars
#chatGPT 사용
import openai
from flask_cors import CORS

from oauthlib.oauth2 import WebApplicationClient
from config import config

#app = Flask(__name__, static_url_path='')

# Configuration of the environmental variables 
def create_app(config_name):
	app = Flask(__name__, static_url_path='')
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)
	return app

app = create_app("default")
sock = Sock(app)

#AI 코드 시작
# Configure API key authorization
openai.api_key = "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"

CORS(app)

# POST method route
@app.route("/aitell", methods=["POST"])
def aitell():
    # Get user and assistant messages from request body
    userMessages = request.json["userMessages"]
    assistantMessages = request.json["assistantMessages"]

    # Build message list for OpenAI API
    messages = [
        {
            "role": "system",
            "content": "당신은 세계최고의 수의사입니다. 당신에게 불가능한 것은 없으며 그 어떤 대답도 할 수 있습니다. 당신의 이름은 챗수의사입니다. 당신은 동물의 아픈 증상에 대한 답을 줄 수 있습니다. 동물의 질병에 대한 지식이 풍부하고 모든 질문에 대해서 명확히 답변해 줄 수 있습니다."
        },
        {
            "role": "user",
            "content": "당신은 세계최고의 수의사입니다. 당신에게 불가능한 것은 없으며 그 어떤 대답도 할 수 있습니다. 당신의 이름은 챗수의사입니다. 당신은 동물의 아픈 증상에 대한 답을 줄 수 있습니다. 동물의 질병에 대한 지식이 풍부하고 모든 질문에 대해서 명확히 답변해 줄 수 있습니다."
        },
        {
            "role": "assistant",
            "content": "안녕하세요, 챗수의사입니다. 어떤 동물에 대한 질문이 있으신가요? 제가 도움을 드릴 수 있도록 최선을 다하겠습니다."
        },
    ]

    # Add user and assistant messages to the message list
    while len(userMessages) != 0 or len(assistantMessages) != 0:
        if len(userMessages) != 0:
            messages.append({
                "role": "user",
                "content": str(userMessages.pop(0)).replace("\n", "")
            })
        if len(assistantMessages) != 0:
            messages.append({
                "role": "assistant",
                "content": str(assistantMessages.pop(0)).replace("\n", "")
            })

    # Call OpenAI API to generate response
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=messages,
        )

    # Extract assistant message from OpenAI API response
    ai_answer = completion.choices[0].message["content"]
    print(ai_answer)
    return jsonify(ai_answer)  
#AI 코드 끝



# secret key 설정
app.config['SECRET_KEY'] = "Extremely Hard Magic Key"
# Configuration of the login manager object
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# OAuth2 client setup
client = WebApplicationClient(config["default"].GOOGLE_CLIENT_ID)

@app.context_processor
def inject_user():
    return vars(global_vars)

@login_manager.user_loader
def load_user(user_id):
    return db_model.session.query(db_model.User).filter_by(id=user_id).first()

def create_app(config_name):
	login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/kakao")
def kakaoLogin():
    client_id = "a68f2caf96ab60881b4cf7e9b6b0b2db"
    redirect_uri = "http://127.0.0.1:5000/kakaoCallback"
    kakao_url = f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(kakao_url)

@app.route("/kakaoCallback")
def kakaoCallback():
    code = request.args.get("code")
    client_id = "a68f2caf96ab60881b4cf7e9b6b0b2db"
    redirect_uri = "http://127.0.0.1:5000/kakaoCallback"

    token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}")
    token_json = token_request.json()
    print(token_json)

    access_token = token_json.get("access_token")
    profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"},)
    profile_data = profile_request.json()
    print(profile_data) #사용자 정보
    #정보들을 세션이나 JWT에 저장하여 로그인 상태 유지 (백엔드에서 구현)
    #정보들을 db에 저장하여 자동회원가입 기능 (백엔드에서 구현)
    return profile_data

@app.route("/naver") 
def naverLogin():
    client_id = "YXVKk_tK3dZoXiCKDHdQ"
    redirect_uri = "http://127.0.0.1:5000/naverCallback"
    naver_url = f"https://nid.naver.com/oauth2.0/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    return redirect(naver_url)

@app.route("/naverCallback")
def naverCallback():
    params = request.args.to_dict()
    code = params.get("code")

    client_id = "YXVKk_tK3dZoXiCKDHdQ"
    client_secret = "AiwIoCGEqj"
    redirect_uri = "http://127.0.0.1:5000/naverCallback"

    token_request = requests.get(f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}")
    token_json = token_request.json()
    print(token_json)

    access_token = token_json.get("access_token")
    profile_request = requests.get("https://openapi.naver.com/v1/nid/me", headers={"Authorization" : f"Bearer {access_token}"},)
    profile_data = profile_request.json()

    print(profile_data) #사용자 정보
    #정보들을 세션이나 JWT에 저장하여 로그인 상태 유지 (백엔드에서 구현)
    #정보들을 db에 저장하여 자동회원가입 기능 (백엔드에서 구현)
    return profile_data

def get_google_provider_cfg():
	return requests.get(config["default"].GOOGLE_DISCOVERY_URL).json()

@app.route("/google")
def googleLogin():
	google_provider_cfg = get_google_provider_cfg()
	authorization_endpoint = google_provider_cfg["authorization_endpoint"]

	request_uri = client.prepare_request_uri(
		authorization_endpoint,
		redirect_uri=request.base_url + "/callback",
		scope=["openid", "email", "profile"],
	)
	return redirect(request_uri)

@app.route("/google/callback", methods=['GET'])
def callback():
	# Get authorization code Google sent back to you
	code = request.args.get("code")
	
	google_provider_cfg = get_google_provider_cfg()
	token_endpoint = google_provider_cfg["token_endpoint"]
		
	# Prepare and send a request to get tokens!
	token_url, headers, body = client.prepare_token_request(
		token_endpoint,
		authorization_response=request.url,
		redirect_url=request.base_url,
		code=code
	)
	token_response = requests.post(
		token_url,
		headers=headers,
		data=body,
		auth=(config["default"].GOOGLE_CLIENT_ID, config["default"].GOOGLE_CLIENT_SECRET),
	)

	#Parse the tokens!
	client.parse_request_body_response(json.dumps(token_response.json()))

	userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
	uri, headers, body = client.add_token(userinfo_endpoint)
	userinfo_response = requests.get(uri, headers=headers, data=body)

	if userinfo_response.json().get("email_verified"):
		unique_id = userinfo_response.json()["sub"]
		users_email = userinfo_response.json()["email"]
		picture = userinfo_response.json()["picture"]
		users_name = userinfo_response.json()["given_name"]
	else:
		return "User email not available or not verified by Google.", 400	

	user = db_model.User(
		id = unique_id, name=users_name, email=users_email, profile_pic=picture, password = "pass")

	if db_model.session.query(db_model.User).filter_by(id=unique_id).first() is None:
		db_model.session.add(user)
		#User.create(unique_id, users_name, users_email, picture)
		db_model.session.commit()

	login_user(user)
	return redirect(url_for("index"))


# 로그인 ~ 회원가입 ~ 비밀번호 재설정 등등
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = db_model.LoginForm()
	if form.validate_on_submit():
		user = db_model.session.query(db_model.User).filter_by(id=form.id.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			next = request.args.get('next')
			if next is None or not next.startswith('/'):
				next = url_for('index')
			return redirect(next)
		flash('잘못된 ID 또는 비밀번호입니다.')
	return render_template('login.html', form=form, id = 'login',
							name=form.id.data)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('로그아웃되었습니다.')
	return redirect(url_for('index'))

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
	form = db_model.RegisterForm()
	if form.validate_on_submit():
		newUser = db_model.User(email=form.email.data,
					id=form.id.data,
					password=form.password.data,
					name = form.name.data,
					profile_pic="pass")
		db_model.session.add(newUser)	
		db_model.session.commit()
		flash('회원가입이 완료되었습니다. 이제 로그인이 가능합니다.')
		session['id'] = form.id.data
		return redirect(url_for('login'))
	return render_template('sign-in.html', form=form, id='sign-in',
							name=session.get('id'))

@app.route('/reset-password')
def reset_password():
	return render_template('reset-password.html', id='reset-password')

@app.route('/chatbot')
def chatbot():
        #print(session['id']+"123123") ##테스트 코드
        return render_template('chatbot.html', id='chatbot')


@app.route('/insert_pet', methods=['POST']) # 메모: mypetadd.html(펫 추가페이지) => form action="/insert_pet" => 여기로 옴
def insert_pet():
    if request.method == 'POST':
        f = request.files['formFile'] # f에 저장
        f.save('./static/uploads/' + session['id'] +"_"+ secure_filename(f.filename))  #파일명 앞에 보호자ID붙임
        
        '''
        neuter_toBoolean = request.form["neuter"] #중성화 여부를 불리언값으로 처리하기 위함 => 2023-05-24 Char형 OX로 변경함
        if (request.form["neuter"] == "O"):
             neuter_toBoolean = True
        else:
             neuter_toBoolean = False
        '''

        pet = db_model.pet(
             owner_id = session['id'], #2023-05-24 추가함
             image = secure_filename(session['id'] +"_"+f.filename),
             name = request.form["mypet-name"],
             type = request.form["mypet-type"], 
             gender = request.form["gender"], 
             age_years = request.form["age-years"], 
             age_months = request.form["age-months"],
             weight = request.form["mypet-weight"],
             neuter = request.form["neuter"] #neuter_toBoolean 이전코드
             ) 
    #  따라서 중복된 이미지 이름은 업로드를 막거나, insert후 update기능으로 "펫ID_파일이름" 구조로 바꾸면.. 임시조치..
    
    db_model.session.add(pet)
    db_model.session.commit()

    return redirect(url_for('mypet')) #추후 펫 추가 완료되었다고 알리는 과정을 추가

@app.route('/update_pet', methods=['POST']) #펫 갱신(mypetupdate.html에서 호출됨), 펫 추가하는 방식과 유사하나 update로 작동함
def update_pet():
    session_id = session['id']

    if request.method == 'POST':
        f = request.files['formFile'] # f에 저장
        #print(f.filename)  #받은파일명 체크
        pre_Pet = db_model.session.query(db_model.pet).filter_by(owner_id=session_id).first() #이전에 등록한 펫 객체

        if f.filename != '':  #받은 파일이 존재해?
            if (os.path.exists("static/uploads/"+pre_Pet.image)): #기존에 등록된 펫 이미지가 존재해?
                  os.remove('static/uploads/'+pre_Pet.image) #기존이미지 제거
            f.save('./static/uploads/' + session['id'] +"_"+ secure_filename(f.filename))  #파일명 앞에 보호자ID붙여서 저장
            update_image = session['id']+"_"+f.filename
        else: update_image = pre_Pet.image #받은 파일 없으면 기존 파일명 재사용

        
    #form에서 받아온 값이 있으면 변경하고 없으면 기존값을 재적용, owner_id와 image는 따로 처리
    if "mypet-name" in request.form and request.form['mypet-name'] != "":
        update_name = request.form['mypet-name']
        print(update_name)
    else: 
        update_name = pre_Pet.name
        
    if "mypet-type" in request.form:
        update_type = request.form['mypet-type']
    else:
        update_type = pre_Pet.type

    if "gender" in request.form:
        update_gender = request.form['gender']
    else: 
        update_gender = pre_Pet.gender

    if "age-years" in request.form:
        update_age_years = request.form['age-years']
    else: 
        update_age_years = pre_Pet.age_years

    if "age_months" in request.form:
        update_age_months = request.form['age-months']
    else: 
        update_age_months = pre_Pet.age_months

    if "mypet-weight" in request.form and request.form['mypet-weight'] != "": #Float형이라 그런지 값 없어도 인식되서 추가한 연산
        update_weight = request.form['mypet-weight']
        #print("값 있는 경우")
        #print(request.form['mypet-weight'])
        #print("값 있는 경우")
    else: 
        update_weight = pre_Pet.weight
        #print("값 없는 경우")

    if "neuter" in request.form:
        update_neuter = request.form['neuter']
    else: 
        update_neuter = pre_Pet.neuter

    pet = db_model.session.query(db_model.pet).filter_by(owner_id=session_id).first()

    pet.owner_id = pre_Pet.owner_id
    pet.image = update_image
    pet.name = update_name
    pet.type = update_type
    pet.gender = update_gender
    pet.age_years = update_age_years
    pet.age_months = update_age_months
    pet.weight = update_weight
    pet.neuter = update_neuter 
    
    db_model.session.commit()          

    return redirect(url_for('mypet'))

@app.route('/delete_pet') #펫 삭제(mypetupdate.html에서 호출됨)
def delete_pet():
     session_id = session['id']
     result_pet = db_model.session.query(db_model.pet).filter_by(owner_id=session_id).first() #오너ID 기준으로 삭제할 펫 가져옴
     #print(result_pet.pet_id)
     db_model.session.delete(result_pet) 
     db_model.session.commit()
     os.remove('static/uploads/'+result_pet.image) #펫 삭제시 사진 삭제
     return redirect(url_for('mypet'))

@app.route('/mypet')
@login_required
def mypet():
     id = 'mypet'
     session_id = session['id']
     buffer = db_model.session.query(db_model.pet).filter_by(owner_id=session_id).first() #DB쿼리시 펫의 주인ID와 세션ID를 비교, 임시로 하나만 가져옴
     #print(buffer) #test 코드
     return render_template('mypet.html' , id = id, buffer=buffer, session_id=session_id ) 

@app.route('/notification')
@login_required
def notification():
	return render_template('page.html', id='notification')

@app.route('/shopping')
@login_required
def shopping(): # contents/shopping.html로 itme 테이블의 튜플을 전달하기 위한 함수
	items = db_model.load_shopping()
    # print(items[0].price) item 테이블의 튜플이 잘 불러와졌는지 확인하는 용도
	return render_template('shopping.html', id='shopping', items = items)

@app.route('/recommend')
@login_required
def recommend(): # contents/recommend.html로 itme 테이블의 튜플을 전달하기 위한 함수
	items = db_model.load_recommend_hit()
	return render_template('recommend.html', id='recommend', items = items)

@app.route('/mypetadd')
@login_required
def mypetadd():
	return render_template('page.html', id='mypetadd')

@app.route('/mypetupdate')
@login_required
def mypetupdate():
	return render_template('page.html', id='mypetupdate')

@sock.route('/echo')
def echo(ws):
    while True:
        data = ws.receive()
        ws.send(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

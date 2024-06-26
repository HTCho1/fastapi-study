from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel


# 데이터베이스 설정을 위한 문자열을 정의
# 이 문자열에는 사용자 이름, 비밀번호, 서버 주소, 데이터베이스 이름이 포함
name = "xx"
password = "xx"
DATABASE_URL = f"mysql+pymysql://{name}:{password}!!@localhost/db_name"
engine = create_engine(DATABASE_URL)

# SQLAlchemy의 모델 기본 클래스를 선언
# 이 클래스를 상속받아 데이터베이스 정보로 변경해야 함
Base = declarative_base()


class User(Base):
    # 'users' 테이블을 정의
    __tablename__ = "users"
    # 각 열(column)을 정의. id는 primary key로 설정됨
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # 사용자 이름, 중복 불가능하고 인덱싱 가능
    email = Column(String(120))  # 이메일 주소, 120자로 길이 제한
    
    
# Pydantic 모델 정의.
# 이 모델은 클라이언트로부터 받은 데이터의 유효성을 검사하는 데 사용됨
class UserCreate(BaseModel):
    username: str
    email: str
    
    
# 데이터베이스 세션을 생성하고 관리하는 의존성 함수를 정의
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()
        
    
# 데이터베이스 엔진을 사용하여 모델을 기반으로 테이블을 생성
Base.metadata.create_all(bind=engine)

# FastAPI app 초기화
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# 사용자를 생성하는 POST API 엔드포인트를 추가
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Pydantic 모델을 사용하여 전달받은 데이터의 유효성을 검증하고 새 User 인스턴스를 생성
    new_user = User(username=user.username, email=user.email)
    db.add(new_user)  # 생성된 User 인스턴스를 데이터베이스 세션에 추가
    db.commit()  # 데이터베이스에 대한 변경사항을 커밋
    db.refresh(new_user)  # 데이터베이스로부터 새 User 인스턴스의 최신 정보를 가져옴
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel


# DB 설정
name = "xx"
password = "xx"
DATABASE_URL = f"mysql+pymysql://{name}:{password}@localhost/db_name"  # 본인의 DB에 맞게 수정
engine = create_engine(DATABASE_URL)

# SQLAlchemy 모델
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # 길이를 50으로 설정
    email = Column(String(120))  # 길이를 120으로 설정
    
    
# Pydantic 모델
class UserCreate(BaseModel):
    username: str
    email: str


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    
    
# Session 초기화 의존성
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
        

# DB에 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# Create
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}


# Read
@app.get("/users/{user_id}")
def read_user(user_id:int, db: Session = Depends(get_db)):
    # SQLAlchemy의 query 메서드를 사용하여 데이터베이스에서 User를 가져오고(쿼리) user_id와 일치하는 User를 찾음(필터링)
    db_user = db.query(User).filter(User.id == user_id).first()
    # users = db.query(User).all()  # 모든 사용자를 가져오는 경우
    # userinfo = db.query(User.username, User.email).all()  # 모든 사용자의 이름과 이메일을 가져오는 경우 (특정 컬럼 선택)
    # user = db.query(User).filter(User.username == "haha").first()  # 특정 사용자를 가져오는 경우 (필터링)
    # user = db.query(User).filter(User.username == "haha").filter(User.email == "hihi@naver.com").first()  # 여러 조건을 사용하는 경우
    # user = db.query(User).filter(or_(User.username == "Son", User.email == "Son@gmail.com")).first()  # or 조건 사용하는 경우. "from sqlalchemy import or_" 필요
    # users = db.query(User).order_by(User.username).all()  # 오름차순 정렬하여 가져오는 경우
    # users = db.query(User).order_by(desc(User.username)).all()  # 내림차순 정렬하여 가져오는 경우. "from sqlalchemy import desc" 필요
    # users = db.query(User).limit(5).all()  # 가져올 데이터 개수 제한 -> 상위 5개
    # users = db.query(User).offset(2).all()  # 가져올 데이터의 시작점 설정 -> 2개 건너뛰고 가져옴: 3번째부터 가져옴
    # count = db.query(User).count()  # 데이터 개수 가져오기
    if db_user is None:
        return {"error": "User not found"}
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}
    
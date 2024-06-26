from fastapi import FastAPI
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel


app = FastAPI()

name = "xx"
password = "xx"
DATABASE_URL = f"mysql+pymysql://{name}:{password}@localhost/db_name"  # 본인에게 맞게 수정 필요
engine = create_engine(DATABASE_URL)  # SQLAlchemy 엔진 생성

# SessionLocal 인스턴스를 생성하기 위한 factory를 정의
# autocommit과 autoflush를 False로 설정하여 데이터베이스 세션 관리를 더욱 세밀하게 제어 가능
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLAlchemy의 Base 클래스를 상속받아 모델의 기본 클래스를 생성
Base = declarative_base()


# User 모델을 정의 -> 이 클래스는 데이터베이스의 'users' 테이블에 매핑됨
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(120))
    
    
class UserCreate(BaseModel):
    username: str
    email: str
    

# SQLAlchemy를 사용하여 데이터베이스에 테이블을 생성
# 만약 테이블이 이미 존재한다면 아무런 작업도 수행하지 않음
Base.metadata.create_all(bind=engine)


@app.post("/users/")
def create_user(user: UserCreate):
    # SessionLocal()을 호출하여 데이터베이스 세션을 생성
    db = SessionLocal()
    
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # 데이터베이스 세션을 닫음
    db.close()
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}

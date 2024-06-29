from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import or_


# DB 설정
name = "root"
password = "9027yw08"
DATABASE_URL = f"mysql+pymysql://{name}:{password}@localhost/db_name"
engine = create_engine(DATABASE_URL)

# SQLAlchemy 모델
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), index=True)
    email = Column(String(120))
    
    
# Session 초기화 의존성
def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()
        

# DB에 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 앱
app = FastAPI()


@app.get("/")
def reat_root():
    return {"message": "Hello World!"}


# Create
@app.post("/users/")
def creat_user(username: str, email: str, db: Session = Depends(get_db)):
    new_user = User(username=username, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email}


from sqlalchemy import func, desc


@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    # 쿼리 실행
    db_users_count = db.query(User.username, func.count(User.id)).group_by(User.username).all()
    db_users_sum = db.query(User.username, func.sum(User.id)).group_by(User.username).all()
    db_users_max = db.query(User.username, func.max(User.id)).group_by(User.username).all()
    db_users_min = db.query(User.username, func.min(User.id)).group_by(User.username).all()
    
    users_count = [{"username": username, "count": count} for username, count in db_users_count]
    users_sum = [{"username": username, "sum": sum} for username, sum in db_users_sum]
    users_max = [{"username": username, "max": max} for username, max in db_users_max]
    users_min = [{"username": username, "min": min} for username, min in db_users_min]
    
    return {"users_count":  users_count, "users_sum": users_sum, "users_max": users_max, "users_min": users_min}
    
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, db, auth, crud
from .db import engine, SessionLocal
import datetime
from .utils import get_password_hash

# create tables (for demo; use Alembic in production)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Admin Dashboard API")

def create_default_admin():
    db = SessionLocal()
    admin = db.query(models.User).filter_by(username="admin").first()
    if not admin:
        new_admin = models.User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            first_name="ادمین",
            last_name="سیستم",
            national_id="0000000000",
            phone="09100000000",
            role="مدیر سایت",
            is_active=True
        )
        db.add(new_admin)
        db.commit()
    db.close()

create_default_admin()

def get_db():
    db_sess = SessionLocal()
    try:
        yield db_sess
    finally:
        db_sess.close()

# login (token) - update last_login and save login history
@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    now = datetime.datetime.utcnow()
    # update last_login
    user.last_login = now
    db.add(user)
    db.commit()
    # create login history
    ip = request.client.host if request and request.client else None
    crud.create_login_history(db, user.id, user.username, now, ip)
    access_token = auth.create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# create user (admin role required)
@app.post("/users/", response_model=schemas.UserOut)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db), admin = Depends(auth.get_current_admin)):
    # validations done in crud
    u = crud.create_user(db, user_in)
    return u

# check username availability
@app.get("/users/check-username/{username}")
def check_username(username: str, db: Session = Depends(get_db)):
    return {"exists": crud.username_exists(db, username)}

# check national id availability
@app.get("/users/check-national/{national_id}")
def check_national(national_id: str, db: Session = Depends(get_db)):
    return {"exists": crud.national_exists(db, national_id)}

# list users (admin)
@app.get("/users/", response_model=list[schemas.UserOut])
def list_users(skip:int=0, limit:int=100, db: Session = Depends(get_db), admin = Depends(auth.get_current_admin)):
    return crud.get_users(db, skip=skip, limit=limit)

# get single user (admin)
@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user_endpoint(user_id:int, db: Session = Depends(get_db), admin = Depends(auth.get_current_admin)):
    u = crud.get_user(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u

# update user (admin)
@app.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id:int, payload: schemas.UserUpdate, db: Session = Depends(get_db), admin = Depends(auth.get_current_admin)):
    try:
        return crud.update_user(db, user_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# change password (owner or admin)
@app.post("/users/{user_id}/change-password")
def change_password(user_id:int, payload: schemas.ChangePassword, db: Session = Depends(get_db), current_user = Depends(auth.get_current_active_user)):
    try:
        crud.change_password(db, current_user, user_id, payload)
        return {"status":"ok"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# delete user (admin)
@app.delete("/users/{user_id}")
def delete_user(user_id:int, db: Session = Depends(get_db), admin = Depends(auth.get_current_admin)):
    crud.delete_user(db, user_id)
    return {"status":"deleted"}

# recent login history (admin)
@app.get("/login-history/recent", response_model=list[schemas.LoginHistoryOut])
def recent_logins(limit:int=10, db: Session = Depends(get_db), admin = Depends(auth.get_current_admin)):
    return crud.get_recent_logins(db, limit=limit)

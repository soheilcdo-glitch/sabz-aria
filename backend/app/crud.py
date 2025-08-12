from sqlalchemy.orm import Session
from . import models, schemas, auth
import datetime

def username_exists(db: Session, username: str) -> bool:
    return db.query(models.User).filter(models.User.username==username).first() is not None

def national_exists(db: Session, national_id: str) -> bool:
    if not national_id:
        return False
    return db.query(models.User).filter(models.User.national_id==national_id).first() is not None

def create_user(db: Session, user_in: schemas.UserCreate) -> models.User:
    if user_in.username and username_exists(db, user_in.username):
        raise ValueError("username already exists")
    if user_in.national_id and national_exists(db, user_in.national_id):
        raise ValueError("national_id already used")
    hashed = auth.get_password_hash(user_in.password)
    u = models.User(
        username=user_in.username,
        hashed_password=hashed,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        father_name=user_in.father_name,
        national_id=user_in.national_id,
        card_number=user_in.card_number,
        phone=user_in.phone,
        birth_date=user_in.birth_date,
        role=user_in.role
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

def get_users(db: Session, skip:int=0, limit:int=100):
    return db.query(models.User).order_by(models.User.created_at.desc()).offset(skip).limit(limit).all()

def get_user(db: Session, user_id:int):
    return db.query(models.User).get(user_id)

def get_user_by_username(db: Session, username:str):
    return db.query(models.User).filter(models.User.username==username).first()

def update_user(db: Session, user_id:int, payload: schemas.UserUpdate):
    u = get_user(db, user_id)
    if not u:
        raise ValueError("User not found")
    # national_id uniqueness check
    if payload.national_id and payload.national_id != u.national_id:
        if national_exists(db, payload.national_id):
            raise ValueError("national_id already used")
    for k, v in payload.dict(exclude_unset=True).items():
        setattr(u, k, v)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

def change_password(db: Session, current_user, target_user_id:int, payload: schemas.ChangePassword):
    target = get_user(db, target_user_id)
    if not target:
        raise ValueError("User not found")
    # only owner or admin can change
    admin_roles = ['مدیر سایت','مدیر ای تی','مدیر مالی','مدیر حسابداری','مدیر انبار']
    if current_user.id != target.id and current_user.role not in admin_roles:
        raise PermissionError("Not permitted")
    if payload.old_password and current_user.id == target.id:
        if not auth.verify_password(payload.old_password, target.hashed_password):
            raise ValueError("old password incorrect")
    target.hashed_password = auth.get_password_hash(payload.new_password)
    db.add(target)
    db.commit()

def delete_user(db: Session, user_id:int):
    u = get_user(db, user_id)
    if not u:
        raise ValueError("User not found")
    db.delete(u)
    db.commit()

# login history
def create_login_history(db: Session, user_id:int, username:str, timestamp:datetime.datetime, ip:str=None):
    rec = models.LoginHistory(user_id=user_id, username=username, timestamp=timestamp, ip=ip)
    db.add(rec)
    db.commit()

def get_recent_logins(db: Session, limit:int=10):
    return db.query(models.LoginHistory).order_by(models.LoginHistory.timestamp.desc()).limit(limit).all()

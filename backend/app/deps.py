from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
\
from . import database, models, schemas, auth
\
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
\
SECRET_KEY = auth.SECRET_KEY
ALGORITHM = auth.ALGORITHM
\
\
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
def get_current_admin(
    current_user: models.User = Depends(get_current_user),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    \
    is_admin_claim = False
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        is_admin_claim = bool(payload.get("is_admin", False))
    except JWTError:
        pass
    if not (current_user.is_admin or is_admin_claim):
        \
        try:
            first_user = db.query(models.User).order_by(models.User.id.asc()).first()
            if first_user and current_user.id == first_user.id:
                current_user.is_admin = True
                db.add(current_user)
                db.commit()
        except Exception:
            pass
    if not (current_user.is_admin or is_admin_claim):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user

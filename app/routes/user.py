from fastapi import APIRouter, Depends, HTTPException, status
from app.Database import database
from app.models import model
from app.schemas import schemas
from sqlalchemy.orm import Session
from sqlalchemy import update
from app.Database.database import SessionLocal
import logging

router = APIRouter()

get_db = database.get_db

logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    filemode="w",
    format="%(asctime)s-%(levelname)s-%(message)s",
)

# POST USER----


@router.post(
    "/Post_User",
    tags=["User"],
    summary="Process User Upload",
    response_description="File processed to User successfully.",
    response_model=schemas.User_schemas,
)
async def Create_User(request: schemas.User_schemas, db: Session = Depends(get_db)):
    """
      Endpoint for processing Create_User Upload data in database
    \f
    :request:Show the pydantic BaseModel
    :db: Database session.
    :return: JSONResponse with status code and message.
    """
    logging.info("Create User upload triggered.")
    new_user = model.User(
        User_id=request.User_id,
        User_name=request.User_name,
        User_age=request.User_age,
        User_email=request.User_email,
        User_address=request.User_address,
    )
    if db.query(model.User).filter(model.User.User_id == new_user.User_id).first():
        logging.warning("user id already in database")
        raise HTTPException(
            status_code=status.HTTP_208_ALREADY_REPORTED, detail="User id already exits"
        )
    logging.info("User Successfully Upload !")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# GET USER----


@router.get(
    "/Get_User",
    tags=["User"],
    summary=" Get Process User ",
    response_description="File Get processed to User successfully.",
    response_model=schemas.User_schemas,
)
async def Get_User(id: int, db: Session = Depends(get_db)):
    """
    Endpoint for processing  Get_User get the data into Database.
    - **id**:get the User in User inventory
    \f
    :db: Database session.
    :return: JSONResponse with status code and message.
    """
    logging.info("Get User triggered.")
    user = db.query(model.User).filter(model.User.User_id == id).first()
    if not user:
        logging.warning("User Not in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User id{id} Not in Database"
        )
    logging.warning("Get the User Successfully!")
    return user


# PUT USER----


@router.put(
    "/Update_User",
    tags=["User"],
    summary=" Update Process to User",
    response_description="File Update processed to User successfully.",
    response_model=schemas.User_schemas,
)
def Update_User(request: schemas.User_schemas, db: Session = Depends(get_db)):
    """
    Endpoint for processing Update_User Update the data into Database.
    \f
    :request:Show the pydantic BaseModel
    :db: Database session.
    :return: JSONResponse with status code and message.
    """
    logging.info("Update User triggered.")
    update_user = (
        db.query(model.User).filter(model.User.User_id == request.User_id).first()
    )
    if not update_user:
        logging.warning("User Not in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"user id not found"
        )
    logging.info("User successfully Updated")
    input = request.model_dump(exclude={"User_id"})
    print("input", input)
    update_stmt = (
        update(model.User).where(model.User.User_id == request.User_id).values(input)
    )

    db.execute(update_stmt)
    db.commit()
    db.close()
    updated_user = (
        db.query(model.User).filter(model.User.User_id == request.User_id).first()
    )
    return updated_user


# DELETE USER----


@router.delete(
    "/Delete_User",
    tags=["User"],
    summary=" Delete Process to User",
    response_description="File delete processed to User successfully.",
)
async def Delete_User(id: int):
    """
    Endpoint for processing Delete_User Delete the data into Database.
    - **id**:get the User in User inventory
    \f
    :db: Database session.
    :return: JSONResponse with status code and message.
    """
    logging.info("Delete User triggered.")
    db = SessionLocal()
    db_item = db.query(model.User).filter(model.User.User_id == id).first()
    if not db_item:
        logging.warning("User Not in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} Not in Database"
        )
    logging.info("User successfully Deleted")
    db.delete(db_item)
    db.commit()
    return {f"message:data deleted {id} successfully"}

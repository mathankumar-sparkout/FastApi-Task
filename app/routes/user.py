from fastapi import APIRouter, Depends, HTTPException, status
from app.Database import database
from app.models import model
from app.schemas import schemas
from sqlmodel import SQLModel, Session, select
import logging

router = APIRouter()

get_db = database.get_db


logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    filemode="w",
    format="%(asctime)s-%(levelname)s-%(message)s",
)

# GET ALL USER----


@router.get(
    "/Get_All_User",
    tags=["USER"],
    summary="Get All Process User",
    response_description="File Get All processed to User successfully.",
    status_code=status.HTTP_200_OK,
)
async def Get_All_User(db: Session = Depends(get_db)):
    """
    Endpoint for processing  Get_All_User get the All data into Database.
    \f
    :db: Database session.
    :return: JSONResponse with status code and message.
    """

    getall_user = db.exec(select(model.User)).all()
    return getall_user


# POST USER----


@router.post(
    "/Post_user",
    tags=["USER"],
    response_model=schemas.schema_User,
    summary="Process User Upload",
    response_description="File processed to User successfully.",
    status_code=status.HTTP_202_ACCEPTED,
)
async def Create_User(request: model.User, db: Session = Depends(get_db)):
    """
      Endpoint for processing Create_User Upload data in database
    \f
    :request:Show the request Body of sql model
    :db: Database session.
    :return: JSONResponse with status code and message.
    """
    logging.info("Create User upload triggered.")
    existing_user = db.exec(
        select(model.User).where(model.User.User_id == request.User_id)
    ).first()
    if existing_user:
        logging.warning("user id already in database")
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED)
    logging.info("User Successfully Upload !")
    db.add(request)
    db.commit()
    db.refresh(request)
    return request


# GET USER----


@router.get(
    "/Get_User/{id}",
    tags=["USER"],
    response_model=schemas.schema_User,
    summary="Get Process User",
    response_description="File Get processed to User successfully.",
    status_code=status.HTTP_200_OK,
)
async def Get_User(id: int, db: Session = Depends(get_db)):
    """
    Endpoint for processing  Get_User get the data into Database.
    - **id**:get the User in Database
    \f
    :db: Database session.
    :return: JSONResponse with status code and message.
    """
    logging.info("Get User triggered.")
    user = db.exec(select(model.User).where(model.User.User_id == id)).first()
    if user is None:
        logging.warning("User Not in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User id {id} Not in Database",
        )
    logging.info("Get the User Successfully!")
    return user


# PUT USER----


@router.put(
    "/Update_User",
    tags=["USER"],
    summary="Update Process User",
    response_model=schemas.schema_User,
    response_description="File Update processed to User successfully.",
    status_code=status.HTTP_201_CREATED,
)
async def Update_User(request: model.User, db: Session = Depends(get_db)):
    # user = db.get(model.User, id)
    """
    Endpoint for processing Update_User Update the data into Database.
    \f
    :request:Show the request body of sql model
    :db: Database session.
    :return: JSONResponse with status code and message.
    """
    user = db.exec(
        select(model.User).where(model.User.User_id == request.User_id)
    ).first()
    logging.info("Update User triggered.")
    if user is None:
        logging.warning("User Not in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User id {request.User_id} Not in Database",
        )
    logging.info("User successfully Updated")
    update_data = request.model_dump(exclude_unset=True)
    user.sqlmodel_update(update_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# DELETE USER----


@router.delete(
    "/Delete_User",
    tags=["USER"],
    summary="Delete Process User",
    response_description="File Delete processed to User successfully.",
    status_code=status.HTTP_200_OK,
)
async def Delete_User(id: int, db: Session = Depends(get_db)):
    """
    Endpoint for processing Delete_User Delete the data into Database.
    - **id**:get the User in User Database
    \f
    :db: Database session.
    :return: JSONResponse with status code and message.
    """
    user = db.exec(select(model.User).where(model.User.User_id == id)).first()
    logging.info("Delete User triggered.")
    if user is None:
        logging.warning("User Not in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User id {id} Not in Database",
        )
    logging.info("User successfully Deleted")

    db.delete(user)
    db.commit()
    return user

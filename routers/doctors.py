from fastapi import APIRouter, HTTPException
from models import DoctorResponseModel, DoctorResponseModelCreate, DoctorResponseModelUpdate
from database import DatabaseManager

router = APIRouter(
    prefix="/doctors",
    tags = ["doctors"],
    responses={404: {"description": "Not found"}}
    )

db = DatabaseManager()


@router.post("/")
async def create_doctor(doctor: DoctorResponseModelCreate) -> DoctorResponseModel:
    doctor = db.tables["doctor"](first_name=doctor.first_name, last_name=doctor.last_name)
    db.add(doctor)
    return doctor

@router.get("/")
async def read_doctors() -> list[DoctorResponseModel]:
    doctors = db.get_all(db.tables["doctor"])
    return doctors

@router.get("/{doctor_id}")
async def read_doctor(doctor_id: int) -> DoctorResponseModel:
    doctor = db.get(db.tables["doctor"], id=doctor_id)
    if doctor:
        return doctor
    else:
        raise HTTPException(status_code=404)

@router.put("/{doctor_id}")
async def update_doctor(doctor_id: int, updated_doctor: DoctorResponseModelUpdate) -> dict:
    doctor = db.get(db.tables["doctor"], id=doctor_id)
    if doctor:
        if db.update(db.tables["doctor"], doctor, **updated_doctor.model_dump(exclude_none=True)):
            return {"message": "record succesfully updated"}
    else:
        raise HTTPException(status_code=404)

@router.delete("/{doctor_id}")
async def delete_doctor(doctor_id: int) -> dict:
    doctor = db.get(db.tables["doctor"], id=doctor_id)
    if doctor:
        db.delete(doctor)
        return {"message": f"removed doctor with id '{doctor_id}' succesfully"}
    else:
        raise HTTPException(status_code=404)
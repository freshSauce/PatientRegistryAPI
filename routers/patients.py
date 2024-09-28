from fastapi import APIRouter, HTTPException
from models import PatientResponseModel, PatientResponseModelCreate, PatientResponseModelUpdate
from database import DatabaseManager

router = APIRouter(
    prefix="/patients",
    tags = ["patients"],
    responses={404: {"description": "Not found"}}
    )

db = DatabaseManager()


@router.post("/")
async def create_patient(patient: PatientResponseModelCreate) -> PatientResponseModel:
    patient = db.tables["patient"](first_name=patient.first_name, last_name=patient.last_name)
    db.add(patient)
    return patient

@router.get("/")
async def read_patients() -> list[PatientResponseModel]:
    patients = db.get_all(db.tables["patient"])
    return patients

@router.get("/{patient_id}")
async def read_patient(patient_id: int) -> PatientResponseModel:
    patient = db.get(db.tables["patient"], id=patient_id)
    if patient:
        return patient
    else:
        raise HTTPException(status_code=404)

@router.put("/{patient_id}")
async def update_patient(patient_id: int, updated_patient: PatientResponseModelUpdate) -> dict:
    patient = db.get(db.tables["patient"], id=patient_id)
    if patient:
        if db.update(db.tables["patient"], patient, **updated_patient.model_dump(exclude_none=True)):
            return {"message": "record succesfully updated"}
    else:
        raise HTTPException(status_code=404)
@router.delete("/{patient_id}")
async def delete_patient(patient_id: int) -> dict:
    patient = db.get(db.tables["patient"], id=patient_id)
    if patient:
        db.delete(patient)
        return {"message": f"removed patient with id '{patient_id}' succesfully"}
    else:
        raise HTTPException(status_code=404)
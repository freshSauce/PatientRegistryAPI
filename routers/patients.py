from datetime import datetime

from fastapi import APIRouter, HTTPException
from models import PatientResponseModel, PatientResponseModelCreate, PatientResponseModelUpdate
from models import MedicalHistoryModel, MedicalHistoryModelCreate, MedicalHistoryModelUpdate
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
    if not patient:
        raise HTTPException(status_code=404)

    return patient


@router.put("/{patient_id}")
async def update_patient(patient_id: int, updated_patient: PatientResponseModelUpdate) -> dict:
    patient = db.get(db.tables["patient"], id=patient_id)
    if not patient:
        raise HTTPException(status_code=404)

    if not db.update(db.tables["patient"], patient, **updated_patient.model_dump(exclude_none=True)):
        raise HTTPException(status_code=500,
                            detail={"message": f"Something went wrong while updating the patient with id: {patient_id}"})

    return {"message": "record succesfully updated"}

@router.delete("/{patient_id}")
async def delete_patient(patient_id: int) -> dict:
    patient = db.get(db.tables["patient"], id=patient_id)
    if not patient:
        raise HTTPException(status_code=404)

    db.delete(patient)
    return {"message": f"removed patient with id '{patient_id}' succesfully"}



@router.get("/{patient_id}/records")
async def get_patient_records(patient_id: int) -> list[MedicalHistoryModel]:
    patient = db.get(db.tables["patient"], id=patient_id)
    if not patient:
        raise HTTPException(status_code=404)

    medical_history = patient.medical_records
    return medical_history

@router.post("/{patient_id}/records")
async def create_record(record: MedicalHistoryModelCreate) -> MedicalHistoryModel:
    patient = db.get(db.tables["patient"], id=record.patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    date = int(datetime.now().timestamp())
    record = db.tables["record"](**record.model_dump(), date=date)
    db.add(record)
    return record

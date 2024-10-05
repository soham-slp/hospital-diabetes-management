from random import random
from management.models import PatientData
from db import db
from sqlalchemy.exc import SQLAlchemyError
from common.exceptions import DBException, ResourceNotFound


def get_prediction(
    pregnancies: int,
    glucose: int,
    blood_pressure: int,
    skin_thickness: int,
    insulin: int,
    bmi: float,
    diabetes_pedigree_function: float,
    age: int,
):
    return random() > 0.5


def save_patient_data(patient_data: PatientData):
    try:
        db.session.add(patient_data)
        db.session.commit()
    except SQLAlchemyError as e:
        raise DBException(e)


def get_patient_data(patient_data_id: int) -> PatientData:
    patient_data = PatientData.query.get(patient_data_id)

    if not patient_data:
        raise ResourceNotFound("The patient data with this id is not found")

    return patient_data


def update_diabetes_test(patient_data: PatientData, diabetes_test: bool) -> PatientData:
    try:
        patient_data.diabetes_test = diabetes_test
        db.session.commit()
        return patient_data
    except SQLAlchemyError as e:
        raise DBException(e)

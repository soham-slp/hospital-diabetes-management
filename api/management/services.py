from random import random
from management.models import PatientData
from db import db
from sqlalchemy.exc import SQLAlchemyError
from common.exceptions import DBException


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

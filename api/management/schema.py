from marshmallow import fields, validates_schema, ValidationError, post_load
from management.models import PatientData
from db import ma
from common.constants import UserRole
from auth.services import get_user
from management.services import get_prediction


class PatientDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PatientData
        load_instance = True
        include_fk = True  # To include foreign keys if necessary

    id = fields.Int(dump_only=True)
    patient_id = fields.Int(required=True)
    doctor_id = fields.Int(required=True)
    pregnancies = fields.Int(required=True)
    glucose = fields.Int(required=True)
    blood_pressure = fields.Int(required=True)
    skin_thickness = fields.Int(required=True)
    insulin = fields.Int(required=True)
    bmi = fields.Float(required=True)
    diabetes_pedigree_function = fields.Float(required=True)
    age = fields.Int(required=True)
    diabetes_test = fields.Bool(required=False)
    diabetes_prediction = fields.Bool(dump_only=True)

    @validates_schema
    def validate_ids(self, data, **kwargs):
        patient = get_user(data["patient_id"])
        if patient.role != UserRole.PATIENT:
            raise ValidationError("Provided patient_id does not belong to a patient.")

        doctor = get_user(data["doctor_id"])
        if doctor.role != UserRole.DOCTOR:
            raise ValidationError("Provided doctor_id does not belong to a doctor.")

    @post_load
    def add_prediction(self, data, **kwargs):
        data["diabetes_prediction"] = self.calculate_diabetes_prediction(data)
        return data

    def calculate_diabetes_prediction(self, data):
        return get_prediction(
            pregnancies=data["pregnancies"],
            glucose=data["glucose"],
            blood_pressure=data["blood_pressure"],
            skin_thickness=data["skin_thickness"],
            insulin=data["insulin"],
            bmi=data["bmi"],
            diabetes_pedigree_function=data["diabetes_pedigree_function"],
            age=data["age"],
        )


class UpdateTestSchema(ma.Schema):
    class Meta:
        pass

    id = fields.Int(required=True)
    diabetes_test = fields.Bool(required=True)

from db import db
from sqlalchemy.orm import mapped_column, Mapped, validates
from sqlalchemy import CheckConstraint
from auth.services import get_user
from common.constants import UserRole
from common.exceptions import LogicalException


class PatientData(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    patient_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=False)
    doctor_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "patient_id != doctor_id",
            name="Patient and doctor id should not be same",
        ),
    )

    @validates("patient_id")
    def validate_patient_id(self, key, patient_id):
        user = get_user(patient_id)

        if user.role != UserRole.PATIENT:
            raise LogicalException("Patient id does not belong to a patient user.")

    @validates("doctor_id")
    def validate_doctor_id(self, key, doctor_id):
        user = get_user(doctor_id)

        if user.role != UserRole.DOCTOR:
            raise LogicalException("Doctor id does not belong to a doctor user.")

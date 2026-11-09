"""Stage 7 domain tests: Patient, Practitioner and Appointment behaviour.

Each test name begins with a TEST ID (T-7xx). The matching requirement or
public contract is quoted in its docstring. Domain tests give partial
evidence only: storage criteria such as AC-01.1 and AC-03.1 also need the
service tests in test_services.py.
"""

from datetime import datetime, timezone

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)

WHEN = datetime(2026, 10, 1, 9, 0)


def make_people() -> tuple[Patient, Practitioner]:
    """Return a fresh synthetic patient and practitioner."""
    return (
        Patient('P1', 'Alex Example'),
        Practitioner('D1', 'Taylor Example', 'General'),
    )


def make_appointment(
    status: AppointmentStatus = AppointmentStatus.SCHEDULED,
) -> Appointment:
    """Return a fresh appointment A1 with the given status."""
    patient, practitioner = make_people()
    return Appointment('A1', patient, practitioner, WHEN, status)


# ---- Patient: FR-01 (partial domain evidence for AC-01.1) -------------


def test_t701_patient_keeps_trimmed_id_and_name() -> None:
    """T-701 (FR-01, partial AC-01.1): valid data is kept, trimmed."""
    patient = Patient('  P1  ', '  Alex Example  ')
    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Example'


@pytest.mark.parametrize('bad_id', ['', '   ', '\t\n', None, 123])
def test_t702_patient_rejects_blank_or_non_text_id(bad_id: object) -> None:
    """T-702 (validation contract): IDs are non-blank strings."""
    with pytest.raises(ValueError):
        Patient(bad_id, 'Alex Example')  # type: ignore[arg-type]


@pytest.mark.parametrize('bad_name', ['', '   ', None])
def test_t703_patient_rejects_blank_name(bad_name: object) -> None:
    """T-703 (FR-01): a required name cannot be blank."""
    with pytest.raises(ValueError):
        Patient('P1', bad_name)  # type: ignore[arg-type]


def test_t704_patient_id_keeps_its_case() -> None:
    """T-704 (validation contract): IDs are case-sensitive."""
    assert Patient('p1', 'Alex Example').patient_id == 'p1'
    assert Patient('P1', 'Alex Example').patient_id != 'p1'


def test_t705_patient_id_is_read_only() -> None:
    """T-705 (public contract): identity is changed only at creation."""
    patient = Patient('P1', 'Alex Example')
    with pytest.raises(AttributeError):
        patient.patient_id = 'P2'  # type: ignore[misc]
    assert patient.patient_id == 'P1'


# ---- Practitioner: FR-03 (partial domain evidence) --------------------


def test_t711_practitioner_keeps_trimmed_fields() -> None:
    """T-711 (FR-03): ID, name and specialty are kept, trimmed."""
    practitioner = Practitioner(' D1 ', ' Taylor Example ', ' General ')
    assert practitioner.practitioner_id == 'D1'
    assert practitioner.name == 'Taylor Example'
    assert practitioner.specialty == 'General'


@pytest.mark.parametrize(
    ('practitioner_id', 'name', 'specialty'),
    [
        ('', 'Taylor Example', 'General'),
        ('D1', '   ', 'General'),
        ('D1', 'Taylor Example', ''),
        ('D1', 'Taylor Example', '   '),
    ],
)
def test_t712_practitioner_rejects_each_blank_required_field(
    practitioner_id: str,
    name: str,
    specialty: str,
) -> None:
    """T-712 (FR-03): ID, name and specialty are each required."""
    with pytest.raises(ValueError):
        Practitioner(practitioner_id, name, specialty)


# ---- Appointment construction: FR-04 (partial AC-03.1) ---------------


def test_t721_new_appointment_is_scheduled_with_same_objects() -> None:
    """T-721 (FR-04, partial AC-03.1): starts SCHEDULED, refers to the
    actual participant objects.
    """
    patient, practitioner = make_people()
    appointment = Appointment('A1', patient, practitioner, WHEN)
    assert appointment.status is AppointmentStatus.SCHEDULED
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.appointment_id == 'A1'
    assert appointment.date_time == WHEN


def test_t722_appointment_rejects_blank_id() -> None:
    """T-722 (validation contract): appointment ID is required."""
    patient, practitioner = make_people()
    with pytest.raises(ValueError):
        Appointment('  ', patient, practitioner, WHEN)


def test_t723_appointment_rejects_wrong_participant_types() -> None:
    """T-723 (BR-04, BR-09): participants must be real domain objects."""
    patient, practitioner = make_people()
    with pytest.raises(ValueError):
        Appointment('A1', 'P1', practitioner, WHEN)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        Appointment('A1', patient, 'D1', WHEN)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    'bad_time',
    [
        datetime(2026, 10, 1, 9, 0, 30),
        datetime(2026, 10, 1, 9, 0, 0, 5),
        datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc),
        '2026-10-01 09:00',
        None,
    ],
)
def test_t724_appointment_rejects_invalid_date_time(
    bad_time: object,
) -> None:
    """T-724 (public contract): naive minute-precision datetime only."""
    patient, practitioner = make_people()
    with pytest.raises(ValueError):
        Appointment('A1', patient, practitioner, bad_time)  # type: ignore[arg-type]


def test_t725_appointment_rejects_non_enum_status() -> None:
    """T-725 (BR-08): status must be an AppointmentStatus member."""
    patient, practitioner = make_people()
    with pytest.raises(ValueError):
        Appointment(
            'A1',
            patient,
            practitioner,
            WHEN,
            'scheduled',  # type: ignore[arg-type]
        )


def test_t726_completed_status_can_be_supplied_at_construction() -> None:
    """T-726 (BR-08): COMPLETED is a valid test fixture state."""
    appointment = make_appointment(AppointmentStatus.COMPLETED)
    assert appointment.status is AppointmentStatus.COMPLETED


# ---- Appointment cancellation: FR-06, FR-07 ---------------------------


def test_t731_cancel_changes_scheduled_to_cancelled() -> None:
    """T-731 (FR-06, AC-05.1): SCHEDULED becomes CANCELLED."""
    appointment = make_appointment()
    appointment.cancel()
    assert appointment.status is AppointmentStatus.CANCELLED


def test_t732_cancel_keeps_the_record_and_its_fields() -> None:
    """T-732 (FR-07, BR-07): cancelling changes state only."""
    patient, practitioner = make_people()
    appointment = Appointment('A1', patient, practitioner, WHEN)
    appointment.cancel()
    assert appointment.appointment_id == 'A1'
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == WHEN


def test_t733_repeated_cancel_is_rejected_without_change() -> None:
    """T-733 (FR-06, AC-05.3): a second cancel raises ValueError."""
    appointment = make_appointment()
    appointment.cancel()
    with pytest.raises(ValueError):
        appointment.cancel()
    assert appointment.status is AppointmentStatus.CANCELLED


def test_t734_completed_appointment_cannot_be_cancelled() -> None:
    """T-734 (BR-06, BR-08): only SCHEDULED can be cancelled."""
    appointment = make_appointment(AppointmentStatus.COMPLETED)
    with pytest.raises(ValueError):
        appointment.cancel()
    assert appointment.status is AppointmentStatus.COMPLETED


def test_t735_status_cannot_be_assigned_directly() -> None:
    """T-735 (public contract): state changes only through cancel()."""
    appointment = make_appointment()
    with pytest.raises(AttributeError):
        appointment.status = AppointmentStatus.CANCELLED  # type: ignore[misc]
    assert appointment.status is AppointmentStatus.SCHEDULED

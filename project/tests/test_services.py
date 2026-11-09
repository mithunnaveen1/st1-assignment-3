"""Stage 6 checks for the three service operations.

Each test name starts with a TEST ID and names the requirement or
acceptance criterion it supports. Every test builds its own fresh store.
"""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

WHEN = datetime(2026, 10, 1, 9, 0)


def fresh_session() -> tuple[
    SmartCareDataStore,
    PatientService,
    PractitionerService,
    AppointmentService,
]:
    """Return a new store and the three services that share it."""
    data_store = SmartCareDataStore()
    return (
        data_store,
        PatientService(data_store),
        PractitionerService(data_store),
        AppointmentService(data_store),
    )


def booked_session() -> tuple[
    SmartCareDataStore,
    AppointmentService,
    Appointment,
]:
    """Return a session holding one SCHEDULED appointment A1."""
    data_store, patients, practitioners, appointments = fresh_session()
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    booked = appointments.book_appointment('A1', 'P1', 'D1', WHEN)
    return data_store, appointments, booked


# ---- Patient lookup: FR-02, AC-02.1, AC-02.2 -------------------------


def test_t601_find_patient_returns_registered_object() -> None:
    """T-601 (AC-02.1): lookup returns the actual stored patient."""
    data_store, patients, _, _ = fresh_session()
    registered = patients.register_patient('P1', 'Alex Example')
    found = patients.find_patient('P1')
    assert found is registered
    assert found.name == 'Alex Example'


def test_t602_find_patient_unknown_id_raises_lookup_error() -> None:
    """T-602 (AC-02.2): a valid but unknown ID reports absence."""
    _, patients, _, _ = fresh_session()
    patients.register_patient('P1', 'Alex Example')
    with pytest.raises(LookupError):
        patients.find_patient('P9')


def test_t603_find_patient_unknown_id_creates_nothing() -> None:
    """T-603 (AC-02.2): a failed lookup does not add a replacement."""
    data_store, patients, _, _ = fresh_session()
    patients.register_patient('P1', 'Alex Example')
    with pytest.raises(LookupError):
        patients.find_patient('P9')
    assert data_store.find_patient('P9') is None
    assert len(data_store.list_patients()) == 1


@pytest.mark.parametrize('bad_id', ['', '   ', '\t'])
def test_t604_find_patient_blank_id_raises_value_error(bad_id: str) -> None:
    """T-604 (FR-02): a blank ID is invalid, which differs from absent."""
    _, patients, _, _ = fresh_session()
    patients.register_patient('P1', 'Alex Example')
    with pytest.raises(ValueError):
        patients.find_patient(bad_id)


def test_t605_find_patient_trims_whitespace() -> None:
    """T-605 (FR-02): surrounding spaces are trimmed before lookup."""
    _, patients, _, _ = fresh_session()
    registered = patients.register_patient('P1', 'Alex Example')
    assert patients.find_patient('  P1  ') is registered


def test_t606_find_patient_is_case_sensitive() -> None:
    """T-606 (FR-02): P1 and p1 are different identifiers."""
    _, patients, _, _ = fresh_session()
    patients.register_patient('P1', 'Alex Example')
    with pytest.raises(LookupError):
        patients.find_patient('p1')


# ---- Practitioner lookup: supporting operation for FR-03 --------------


def test_t611_find_practitioner_returns_registered_object() -> None:
    """T-611 (FR-03 support): lookup returns the stored practitioner."""
    _, _, practitioners, _ = fresh_session()
    registered = practitioners.register_practitioner(
        'D1',
        'Taylor Example',
        'General',
    )
    found = practitioners.find_practitioner('D1')
    assert found is registered
    assert found.specialty == 'General'


def test_t612_find_practitioner_unknown_id_raises_lookup_error() -> None:
    """T-612: a valid but unknown practitioner ID reports absence."""
    data_store, _, practitioners, _ = fresh_session()
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    with pytest.raises(LookupError):
        practitioners.find_practitioner('D9')
    assert data_store.find_practitioner('D9') is None
    assert len(data_store.list_practitioners()) == 1


@pytest.mark.parametrize('bad_id', ['', '   '])
def test_t613_find_practitioner_blank_id_raises_value_error(
    bad_id: str,
) -> None:
    """T-613: a blank practitioner ID is invalid."""
    _, _, practitioners, _ = fresh_session()
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    with pytest.raises(ValueError):
        practitioners.find_practitioner(bad_id)


def test_t614_find_practitioner_trims_and_is_case_sensitive() -> None:
    """T-614: IDs are trimmed and case-sensitive."""
    _, _, practitioners, _ = fresh_session()
    registered = practitioners.register_practitioner(
        'D1',
        'Taylor Example',
        'General',
    )
    assert practitioners.find_practitioner(' D1 ') is registered
    with pytest.raises(LookupError):
        practitioners.find_practitioner('d1')


# ---- Cancellation: FR-06, FR-07, AC-05.1, AC-05.2, AC-05.3 ------------


def test_t621_cancel_changes_status_and_returns_same_object() -> None:
    """T-621 (AC-05.1): a SCHEDULED appointment becomes CANCELLED."""
    _, appointments, booked = booked_session()
    result = appointments.cancel_appointment('A1')
    assert result is booked
    assert result.status is AppointmentStatus.CANCELLED


def test_t622_cancelled_appointment_is_retained_in_history() -> None:
    """T-622 (AC-05.2, FR-07): the same object is still retrievable."""
    data_store, appointments, booked = booked_session()
    appointments.cancel_appointment('A1')
    assert appointments.find_appointment('A1') is booked
    assert data_store.list_appointments() == [booked]
    assert booked.status is AppointmentStatus.CANCELLED


def test_t623_repeated_cancellation_is_rejected_without_change() -> None:
    """T-623 (AC-05.3): cancelling twice raises and changes nothing."""
    data_store, appointments, booked = booked_session()
    appointments.cancel_appointment('A1')
    with pytest.raises(ValueError):
        appointments.cancel_appointment('A1')
    assert booked.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [booked]


def test_t624_completed_appointment_cannot_be_cancelled() -> None:
    """T-624 (BR-06, BR-08): COMPLETED is not cancellable."""
    data_store, patients, practitioners, appointments = fresh_session()
    patient = patients.register_patient('P1', 'Alex Example')
    practitioner = practitioners.register_practitioner(
        'D1',
        'Taylor Example',
        'General',
    )
    completed = Appointment(
        'A2',
        patient,
        practitioner,
        WHEN,
        AppointmentStatus.COMPLETED,
    )
    data_store.add_appointment(completed)
    with pytest.raises(ValueError):
        appointments.cancel_appointment('A2')
    assert completed.status is AppointmentStatus.COMPLETED
    assert appointments.find_appointment('A2') is completed


def test_t625_cancel_unknown_id_raises_lookup_error_without_change() -> None:
    """T-625: an unknown appointment ID raises LookupError."""
    data_store, appointments, booked = booked_session()
    with pytest.raises(LookupError):
        appointments.cancel_appointment('A9')
    assert booked.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [booked]


@pytest.mark.parametrize('bad_id', ['', '   '])
def test_t626_cancel_blank_id_raises_value_error(bad_id: str) -> None:
    """T-626: a blank appointment ID is invalid, not merely absent."""
    _, appointments, booked = booked_session()
    with pytest.raises(ValueError):
        appointments.cancel_appointment(bad_id)
    assert booked.status is AppointmentStatus.SCHEDULED


def test_t627_cancel_trims_id_and_other_appointments_unchanged() -> None:
    """T-627: a padded ID works and only the target changes."""
    _, appointments, first = booked_session()
    second = appointments.book_appointment(
        'A2',
        'P1',
        'D1',
        datetime(2026, 10, 1, 10, 0),
    )
    appointments.cancel_appointment(' A1 ')
    assert first.status is AppointmentStatus.CANCELLED
    assert second.status is AppointmentStatus.SCHEDULED


def test_t628_cancelled_slot_does_not_block_rebooking() -> None:
    """T-628 (BR-05): a CANCELLED appointment no longer conflicts."""
    _, appointments, _ = booked_session()
    appointments.cancel_appointment('A1')
    rebooked = appointments.book_appointment('A3', 'P1', 'D1', WHEN)
    assert rebooked.status is AppointmentStatus.SCHEDULED

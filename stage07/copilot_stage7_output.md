# Stage 7 GitHub Copilot test-design review: record of the actual output

Member: mithunnaveen1. Tool: GitHub Copilot Free, Copilot Chat on github.com, normal chat (no agent mode). Date: Tue 10 Nov 2026, about 9:20 pm (Sydney).
Prompt: the Stage 7 handout prompt (Part F) for FR-05 / AC-04.1 and AC-04.2, with the public contracts listed. Prompt text drafted with Claude; the Copilot session and output below are real.
Note: the text below is the output as it was pasted into the working session. Its formatting (line breaks between code blocks and the "Intended to verify" lines) was lost in the paste; the words and code are unchanged.

## Copilot output (pasted unedited)

Use a fresh service setup for each candidate, with `PatientService`, `PractitionerService`, and `AppointmentService` wired to the same `SmartCareDataStore`. The fixture names below are illustrative; adapt them to the project's existing test setup. These candidates use service contracts and observable results, not datastore internals.

```python
from datetime import datetime

import pytest

def test_same_practitioner_same_time_is_rejected_without_storing_booking(
    patient_service, practitioner_service, appointment_service
):
    patient_service.register_patient("P1", "Patient One")
    patient_service.register_patient("P2", "Patient Two")
    practitioner_service.register_practitioner("R1", "Practitioner One", "General")

    when = datetime(2026, 5, 12, 9, 0)
    appointment_service.book_appointment("A1", "P1", "R1", when)
    existing_before = appointment_service.find_appointment("A1")

    with pytest.raises(ValueError):
        appointment_service.book_appointment("A2", "P2", "R1", when)

    existing_after = appointment_service.find_appointment("A1")
    assert existing_after.status is AppointmentStatus.SCHEDULED
    assert existing_after.appointment_id == existing_before.appointment_id

    with pytest.raises(LookupError):
        appointment_service.find_appointment("A2")
```
Intended to verify: AC-04.1: a second booking for the same practitioner at the same date/time raises `ValueError`; the existing appointment remains retrievable and scheduled, and the rejected appointment ID is not stored. If the public `Appointment` contract exposes other relevant booking fields, snapshot and compare those too to strengthen the unchanged-state check.

```python
def test_different_practitioner_at_same_time_is_allowed(
    patient_service, practitioner_service, appointment_service
):
    patient_service.register_patient("P1", "Patient One")
    patient_service.register_patient("P2", "Patient Two")
    practitioner_service.register_practitioner("R1", "Practitioner One", "General")
    practitioner_service.register_practitioner("R2", "Practitioner Two", "General")

    when = datetime(2026, 5, 12, 9, 0)
    appointment_service.book_appointment("A1", "P1", "R1", when)

    returned = appointment_service.book_appointment("A2", "P2", "R2", when)

    stored = appointment_service.find_appointment("A2")
    assert stored.appointment_id == "A2"
    assert stored.status is AppointmentStatus.SCHEDULED
    assert returned.appointment_id == stored.appointment_id
```
Intended to verify: AC-04.2: a booking for a different practitioner at the same date/time is allowed and is retrievable as scheduled.

```python
def test_same_practitioner_at_adjacent_minute_is_not_same_time(
    patient_service, practitioner_service, appointment_service
):
    patient_service.register_patient("P1", "Patient One")
    patient_service.register_patient("P2", "Patient Two")
    practitioner_service.register_practitioner("R1", "Practitioner One", "General")

    appointment_service.book_appointment(
        "A1", "P1", "R1", datetime(2026, 5, 12, 9, 0)
    )

    returned = appointment_service.book_appointment(
        "A2", "P2", "R1", datetime(2026, 5, 12, 9, 1)
    )

    assert appointment_service.find_appointment("A2").status is AppointmentStatus.SCHEDULED
    assert returned.appointment_id == "A2"
```
Intended to verify: the conflict condition is the same date and time, not merely the same date or hour. The supplied context says times have minute precision, so this checks that one minute later is a distinct time.

```python
def test_cancelled_appointment_at_same_time_does_not_trigger_scheduled_conflict(
    patient_service, practitioner_service, appointment_service
):
    patient_service.register_patient("P1", "Patient One")
    patient_service.register_patient("P2", "Patient Two")
    practitioner_service.register_practitioner("R1", "Practitioner One", "General")

    when = datetime(2026, 5, 12, 9, 0)
    appointment_service.book_appointment("A1", "P1", "R1", when)
    appointment_service.cancel_appointment("A1")

    assert appointment_service.find_appointment("A1").status is AppointmentStatus.CANCELLED

    returned = appointment_service.book_appointment("A2", "P2", "R1", when)

    assert returned.appointment_id == "A2"
    assert appointment_service.find_appointment("A2").status is AppointmentStatus.SCHEDULED
    assert appointment_service.find_appointment("A1").status is AppointmentStatus.CANCELLED
```
Intended to verify: the conflict applies to an existing SCHEDULED appointment, not a retained CANCELLED one. This follows from the requirement's stated status condition; confirm that interpretation against the baseline before treating this as a mandatory acceptance test.

A comparable COMPLETED boundary test is not proposed: the supplied public contracts provide no public way to create or complete an appointment, so setting its status directly would rely on an unstated or private mechanism. These are proposed tests only; they have not been run.

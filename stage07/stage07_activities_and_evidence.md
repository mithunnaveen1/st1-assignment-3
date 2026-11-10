# Stage 7 Testing and Verification Record

Group/tutorial: Solo group (UG), approved by the tutor  Members/cohorts: Mithun Naveen (mithunnaveen1), UG, sole member (solo group approved by tutor)
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | Register a patient with a valid ID and name and check it is stored | Register with a blank ID, or a duplicate ID, and check ValueError | The stored patient has the trimmed ID and name; bad input raises ValueError and nothing is stored or overwritten |
| FR-05 Prevent practitioner conflict | Book the same practitioner at two different times, or two practitioners at the same time, and check both succeed | Book the same practitioner at the same time as a SCHEDULED appointment and check ValueError | The conflicting booking raises ValueError and the store still holds only the first appointment |
| FR-06 Cancel appointment | Cancel a scheduled appointment and check it returns | Cancel an unknown ID (LookupError) and cancel an already cancelled appointment (ValueError) | status == AppointmentStatus.CANCELLED after cancelling; failed attempts leave state unchanged |
| FR-07 Retain cancelled history | After cancelling, find the appointment by ID and check it is still stored | Check a cancelled appointment is not deleted, and that a cancelled slot can be booked again without a false conflict | find_appointment returns the same object with CANCELLED status, and a new booking at that time succeeds |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak/unclear  Why: It can never fail, so it checks no behaviour and would pass even if the code were broken.

`assert appointment is not None`
Judgement: Weak/unclear  Why: It only shows an object exists. It would still pass if the status, patient, practitioner or time were wrong.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong for stated behaviour  Why: It checks the exact status expected after cancelling, so a wrong or unchanged status fails it. It does not show the appointment was retained or that other fields are unchanged.

`assert len(results) > 0`
Judgement: Weak/unclear  Why: It only shows something was returned. It would pass with wrong, extra or unordered results, so it needs the exact expected contents.

`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong for stated behaviour  Why: It checks that the store holds the very same object under that ID, which shows it was stored and retained. It does not check the object's status or field values.

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract:
- Blank or whitespace-only patient ID or name: ValueError and nothing stored (required_text validation, FR-01).
- Whitespace around a valid ID or name: trimmed and stored trimmed.
- Same practitioner, same time, existing SCHEDULED appointment: ValueError (BR practitioner conflict, FR-05).
- Same time with a different practitioner, or the same practitioner at a different time: allowed.
- Same slot after the earlier appointment was cancelled: allowed, because only SCHEDULED appointments conflict.
- Cancel an unknown ID: LookupError. Cancel a blank ID: ValueError.
- Cancel an already cancelled appointment: ValueError and state unchanged. Cancel a completed appointment: ValueError and state unchanged.
- Date/time with seconds or an invalid type: ValueError (validate_date_time).

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | Asserts only that an object is not None, so it passes whatever the object contains. | Check the registered patient has the expected trimmed ID and name, and that the store returns that same patient. |
| 2 | Another not-None check: it would pass even if the appointment had the wrong status, patient or time. | Book an appointment and assert its status is SCHEDULED, its patient and practitioner are the ones given, and the store holds it. |
| 3 | assert True can never fail, so it proves nothing and gives false confidence. | Cancel an appointment and assert its status is CANCELLED and it is still found in the store. |
| 4 | Assumes SMS notifications exist, but the requirements baseline has no such feature, so the test checks behaviour that is not required (scope creep). | Remove it, and instead test a real requirement such as a practitioner conflict raising ValueError. |
| 5 | Also assumes SMS notifications, which are not in the requirements, so it cannot be traced to any FR or AC. | Remove it. Only keep tests that trace to a requirement, such as cancelled history being retained. |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
Coverage only shows that lines were executed, not that the results were checked. A test with weak or no assertions (such as assert True) can run every line and still pass with wrong code. Coverage also cannot show missing requirements, untested inputs and boundaries, or wrong expected values.

## B Requirement to Test Traceability Matrix

Note: the TEST IDs (T-601 to T-764) were assigned in the Claude-drafted plan, not independently by the student before drafting. Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| Supplied starter checks (not mine) | AC-01.2, AC-03.1, AC-03.2, AC-04.1, AC-04.2, AC-05.1 to AC-05.3 (partial) | Supplied | Supplied scaffold | tests/test_starter.py (8 tests) | Supplied behaviour only | Passed (8 of 76) | Supplied by teaching staff |
| FR-01 | partial AC-01.1 | T-701 | Domain unit | tests/test_domain.py::test_t701_patient_keeps_trimmed_id_and_name | valid data is kept, trimmed. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| Supporting contract (see docstring) | Quoted contract: validation contract | T-702 | Domain unit | tests/test_domain.py::test_t702_patient_rejects_blank_or_non_text_id | IDs are non-blank strings. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| FR-01 | No canonical AC; quoted contract: see test docstring | T-703 | Domain unit | tests/test_domain.py::test_t703_patient_rejects_blank_name | a required name cannot be blank. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| Supporting contract (see docstring) | Quoted contract: validation contract | T-704 | Domain unit | tests/test_domain.py::test_t704_patient_id_keeps_its_case | IDs are case-sensitive. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| Supporting contract (see docstring) | Quoted contract: public contract | T-705 | Domain unit | tests/test_domain.py::test_t705_patient_id_is_read_only | identity is changed only at creation. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| FR-03 | No canonical AC; quoted contract: see test docstring | T-711 | Domain unit | tests/test_domain.py::test_t711_practitioner_keeps_trimmed_fields | ID, name and specialty are kept, trimmed. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| FR-03 | No canonical AC; quoted contract: see test docstring | T-712 | Domain unit | tests/test_domain.py::test_t712_practitioner_rejects_each_blank_required_field | ID, name and specialty are each required. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| FR-04 | partial AC-03.1 | T-721 | Domain unit | tests/test_domain.py::test_t721_new_appointment_is_scheduled_with_same_objects | starts SCHEDULED, refers to the actual participant objects. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| Supporting contract (see docstring) | Quoted contract: validation contract | T-722 | Domain unit | tests/test_domain.py::test_t722_appointment_rejects_blank_id | appointment ID is required. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| BR-04, BR-09 | No canonical AC; quoted contract: see test docstring | T-723 | Domain unit | tests/test_domain.py::test_t723_appointment_rejects_wrong_participant_types | participants must be real domain objects. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| Supporting contract (see docstring) | Quoted contract: public contract | T-724 | Domain unit | tests/test_domain.py::test_t724_appointment_rejects_invalid_date_time | naive minute-precision datetime only. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| BR-08 | No canonical AC; quoted contract: see test docstring | T-725 | Domain unit | tests/test_domain.py::test_t725_appointment_rejects_non_enum_status | status must be an AppointmentStatus member. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| BR-08 | No canonical AC; quoted contract: see test docstring | T-726 | Domain unit | tests/test_domain.py::test_t726_completed_status_can_be_supplied_at_construction | COMPLETED is a valid test fixture state. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| FR-06 | AC-05.1 | T-731 | Domain unit | tests/test_domain.py::test_t731_cancel_changes_scheduled_to_cancelled | SCHEDULED becomes CANCELLED. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| FR-07, BR-07 | No canonical AC; quoted contract: see test docstring | T-732 | Domain unit | tests/test_domain.py::test_t732_cancel_keeps_the_record_and_its_fields | cancelling changes state only. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| FR-06 | AC-05.3 | T-733 | Domain unit | tests/test_domain.py::test_t733_repeated_cancel_is_rejected_without_change | a second cancel raises ValueError. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| BR-06, BR-08 | No canonical AC; quoted contract: see test docstring | T-734 | Domain unit | tests/test_domain.py::test_t734_completed_appointment_cannot_be_cancelled | only SCHEDULED can be cancelled. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| Supporting contract (see docstring) | Quoted contract: public contract | T-735 | Domain unit | tests/test_domain.py::test_t735_status_cannot_be_assigned_directly | state changes only through cancel(). | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| Supporting contract (see docstring) | AC-02.1 | T-601 | Service (real objects and shared store) | tests/test_services.py::test_t601_find_patient_returns_registered_object | lookup returns the actual stored patient. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| Supporting contract (see docstring) | AC-02.2 | T-602 | Service (real objects and shared store) | tests/test_services.py::test_t602_find_patient_unknown_id_raises_lookup_error | a valid but unknown ID reports absence. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| Supporting contract (see docstring) | AC-02.2 | T-603 | Service (real objects and shared store) | tests/test_services.py::test_t603_find_patient_unknown_id_creates_nothing | a failed lookup does not add a replacement. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| FR-02 | No canonical AC; quoted contract: see test docstring | T-604 | Service (real objects and shared store) | tests/test_services.py::test_t604_find_patient_blank_id_raises_value_error | a blank ID is invalid, which differs from absent. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| FR-02 | No canonical AC; quoted contract: see test docstring | T-605 | Service (real objects and shared store) | tests/test_services.py::test_t605_find_patient_trims_whitespace | surrounding spaces are trimmed before lookup. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| FR-02 | No canonical AC; quoted contract: see test docstring | T-606 | Service (real objects and shared store) | tests/test_services.py::test_t606_find_patient_is_case_sensitive | P1 and p1 are different identifiers. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| FR-03 support | No canonical AC; quoted contract: see test docstring | T-611 | Service (real objects and shared store) | tests/test_services.py::test_t611_find_practitioner_returns_registered_object | lookup returns the stored practitioner. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| Supporting contract (see docstring) | No canonical AC; quoted contract: see test docstring | T-612 | Service (real objects and shared store) | tests/test_services.py::test_t612_find_practitioner_unknown_id_raises_lookup_error | a valid but unknown practitioner ID reports absence. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| Supporting contract (see docstring) | No canonical AC; quoted contract: see test docstring | T-613 | Service (real objects and shared store) | tests/test_services.py::test_t613_find_practitioner_blank_id_raises_value_error | a blank practitioner ID is invalid. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| Supporting contract (see docstring) | No canonical AC; quoted contract: see test docstring | T-614 | Service (real objects and shared store) | tests/test_services.py::test_t614_find_practitioner_trims_and_is_case_sensitive | IDs are trimmed and case-sensitive. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| Supporting contract (see docstring) | AC-05.1 | T-621 | Service (real objects and shared store) | tests/test_services.py::test_t621_cancel_changes_status_and_returns_same_object | a SCHEDULED appointment becomes CANCELLED. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| FR-07 | AC-05.2 | T-622 | Service (real objects and shared store) | tests/test_services.py::test_t622_cancelled_appointment_is_retained_in_history | the same object is still retrievable. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| Supporting contract (see docstring) | AC-05.3 | T-623 | Service (real objects and shared store) | tests/test_services.py::test_t623_repeated_cancellation_is_rejected_without_change | cancelling twice raises and changes nothing. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| BR-06, BR-08 | No canonical AC; quoted contract: see test docstring | T-624 | Service (real objects and shared store) | tests/test_services.py::test_t624_completed_appointment_cannot_be_cancelled | COMPLETED is not cancellable. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| Supporting contract (see docstring) | No canonical AC; quoted contract: see test docstring | T-625 | Service (real objects and shared store) | tests/test_services.py::test_t625_cancel_unknown_id_raises_lookup_error_without_change | an unknown appointment ID raises LookupError. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| Supporting contract (see docstring) | No canonical AC; quoted contract: see test docstring | T-626 | Service (real objects and shared store) | tests/test_services.py::test_t626_cancel_blank_id_raises_value_error | a blank appointment ID is invalid, not merely absent. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| Supporting contract (see docstring) | No canonical AC; quoted contract: see test docstring | T-627 | Service (real objects and shared store) | tests/test_services.py::test_t627_cancel_trims_id_and_other_appointments_unchanged | a padded ID works and only the target changes. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| BR-05 | No canonical AC; quoted contract: see test docstring | T-628 | Service (real objects and shared store) | tests/test_services.py::test_t628_cancelled_slot_does_not_block_rebooking | a CANCELLED appointment no longer conflicts. | Passed (76 passed on main b7496a8) | Student-authored (Stage 6); drafted with Claude, disclosed |
| FR-01 | AC-01.1 | T-741 | Service (real objects and shared store) | tests/test_services.py::test_t741_registered_patient_is_stored_and_retrievable | complete service evidence of storage. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| Supporting contract (see docstring) | AC-01.2 | T-742 | Service (real objects and shared store) | tests/test_services.py::test_t742_trimmed_duplicate_patient_id_is_rejected | a padded copy of an existing ID is a duplicate, and the original record is not overwritten. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| Supporting contract (see docstring) | Quoted contract: validation contract | T-743 | Service (real objects and shared store) | tests/test_services.py::test_t743_different_case_patient_id_is_a_different_patient | IDs are case-sensitive, so P1 and p1 can both be registered. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| NFR-01 | Quoted contract: validation contract | T-744 | Service (real objects and shared store) | tests/test_services.py::test_t744_blank_patient_registration_leaves_store_empty | rejection stores nothing. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| FR-03, BR-02 | No canonical AC; quoted contract: see test docstring | T-745 | Service (real objects and shared store) | tests/test_services.py::test_t745_duplicate_practitioner_id_is_rejected_without_overwrite | the original practitioner is preserved. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| FR-04 | AC-03.1 | T-751 | Service (real objects and shared store) | tests/test_services.py::test_t751_booking_stores_scheduled_appointment_with_real_objects | registered participants, unique ID and a free time give a stored SCHEDULED appointment. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| Supporting contract (see docstring) | AC-03.2 | T-752 | Service (real objects and shared store) | tests/test_services.py::test_t752_booking_unknown_patient_is_rejected_and_nothing_stored | an unknown patient prevents booking. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| Supporting contract (see docstring) | AC-03.2 | T-753 | Service (real objects and shared store) | tests/test_services.py::test_t753_booking_unknown_practitioner_is_rejected | an unknown practitioner prevents booking. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| NFR-01 | No canonical AC; quoted contract: see test docstring | T-754 | Service (real objects and shared store) | tests/test_services.py::test_t754_booking_with_invalid_time_stores_nothing | an invalid datetime leaves the store unchanged. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| BR-03 | No canonical AC; quoted contract: see test docstring | T-755 | Service (real objects and shared store) | tests/test_services.py::test_t755_duplicate_appointment_id_does_not_replace_original | a repeated appointment ID is rejected and the original time is kept. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| FR-08 | AC-06.1 | T-756 | Service (real objects and shared store) | tests/test_services.py::test_t756_find_appointment_known_unknown_and_blank | known ID returns the object, a valid unknown ID raises LookupError, a blank ID raises ValueError. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| FR-05 | AC-04.1 | T-761 | Service (real objects and shared store) | tests/test_services.py::test_t761_same_practitioner_same_time_conflicts | same practitioner, exact time and an existing SCHEDULED appointment is rejected without changing state. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| FR-05 | AC-04.2 | T-762 | Service (real objects and shared store) | tests/test_services.py::test_t762_different_practitioner_same_time_is_allowed | conflicts belong to a practitioner. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| FR-05 boundary | No canonical AC; quoted contract: see test docstring | T-763 | Service (real objects and shared store) | tests/test_services.py::test_t763_one_minute_apart_does_not_conflict | the rule is exact time, not an overlap. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |
| FR-05, BR-05, BR-08 | No canonical AC; quoted contract: see test docstring | T-764 | Service (real objects and shared store) | tests/test_services.py::test_t764_completed_appointment_does_not_block_the_slot | only SCHEDULED appointments conflict, so a COMPLETED one at the same time does not. | Passed (76 passed on main b7496a8) | Student-authored (Stage 7); drafted with Claude, disclosed |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| T-701 | FR-01 | partial AC-01.1 | Positive | valid data is kept, trimmed. | Patient keeps trimmed ID and name | Adds positive evidence not covered by the 8 supplied tests |
| T-702 | Supporting contract (see docstring) | Quoted contract: validation contract | Negative | IDs are non-blank strings. | ValueError for blank or non-text ID | Adds negative evidence not covered by the 8 supplied tests |
| T-703 | FR-01 | No canonical AC; quoted contract: see test docstring | Negative | a required name cannot be blank. | ValueError for blank name | Adds negative evidence not covered by the 8 supplied tests |
| T-704 | Supporting contract (see docstring) | Quoted contract: validation contract | Boundary | IDs are case-sensitive. | ID keeps its case; P1 differs from p1 | Adds boundary evidence not covered by the 8 supplied tests |
| T-705 | Supporting contract (see docstring) | Quoted contract: public contract | Negative | identity is changed only at creation. | AttributeError on ID assignment; ID unchanged | Adds negative evidence not covered by the 8 supplied tests |
| T-711 | FR-03 | No canonical AC; quoted contract: see test docstring | Positive | ID, name and specialty are kept, trimmed. | Practitioner keeps trimmed ID, name, specialty | Adds positive evidence not covered by the 8 supplied tests |
| T-712 | FR-03 | No canonical AC; quoted contract: see test docstring | Negative | ID, name and specialty are each required. | ValueError for each blank required field | Adds negative evidence not covered by the 8 supplied tests |
| T-721 | FR-04 | partial AC-03.1 | Positive | starts SCHEDULED, refers to the actual participant objects. | Starts SCHEDULED; same participant objects and values | Adds positive evidence not covered by the 8 supplied tests |
| T-722 | Supporting contract (see docstring) | Quoted contract: validation contract | Negative | appointment ID is required. | ValueError for blank appointment ID | Adds negative evidence not covered by the 8 supplied tests |
| T-723 | BR-04, BR-09 | No canonical AC; quoted contract: see test docstring | Negative | participants must be real domain objects. | ValueError for non-Patient or non-Practitioner participants | Adds negative evidence not covered by the 8 supplied tests |
| T-724 | Supporting contract (see docstring) | Quoted contract: public contract | Boundary | naive minute-precision datetime only. | ValueError for seconds, microseconds, timezone-aware, string, None | Adds boundary evidence not covered by the 8 supplied tests |
| T-725 | BR-08 | No canonical AC; quoted contract: see test docstring | Negative | status must be an AppointmentStatus member. | ValueError for a string status | Adds negative evidence not covered by the 8 supplied tests |
| T-726 | BR-08 | No canonical AC; quoted contract: see test docstring | Positive | COMPLETED is a valid test fixture state. | COMPLETED can be supplied at construction | Adds positive evidence not covered by the 8 supplied tests |
| T-731 | FR-06 | AC-05.1 | Positive | SCHEDULED becomes CANCELLED. | Status becomes CANCELLED | Adds positive evidence not covered by the 8 supplied tests |
| T-732 | FR-07, BR-07 | No canonical AC; quoted contract: see test docstring | Positive | cancelling changes state only. | ID, participants and time unchanged after cancel | Adds positive evidence not covered by the 8 supplied tests |
| T-733 | FR-06 | AC-05.3 | Negative | a second cancel raises ValueError. | Second cancel raises ValueError; status stays CANCELLED | Adds negative evidence not covered by the 8 supplied tests |
| T-734 | BR-06, BR-08 | No canonical AC; quoted contract: see test docstring | Negative | only SCHEDULED can be cancelled. | COMPLETED cancel raises ValueError; status unchanged | Adds negative evidence not covered by the 8 supplied tests |
| T-735 | Supporting contract (see docstring) | Quoted contract: public contract | Negative | state changes only through cancel(). | AttributeError on status assignment; status unchanged | Adds negative evidence not covered by the 8 supplied tests |
| T-741 | FR-01 | AC-01.1 | Positive | complete service evidence of storage. | Registered patient is found in the store and listed | Adds positive evidence not covered by the 8 supplied tests |
| T-742 | Supporting contract (see docstring) | AC-01.2 | Boundary | a padded copy of an existing ID is a duplicate, and the original record is not overwritten. | " P1 " rejected as duplicate; original name kept; one patient stored | Adds boundary evidence not covered by the 8 supplied tests |
| T-743 | Supporting contract (see docstring) | Quoted contract: validation contract | Boundary | IDs are case-sensitive, so P1 and p1 can both be registered. | P1 and p1 both register; two patients stored | Adds boundary evidence not covered by the 8 supplied tests |
| T-744 | NFR-01 | Quoted contract: validation contract | Negative | rejection stores nothing. | ValueError for blank ID or name; store empty | Adds negative evidence not covered by the 8 supplied tests |
| T-745 | FR-03, BR-02 | No canonical AC; quoted contract: see test docstring | Negative | the original practitioner is preserved. | Padded duplicate ID rejected; original specialty kept | Adds negative evidence not covered by the 8 supplied tests |
| T-751 | FR-04 | AC-03.1 | Positive | registered participants, unique ID and a free time give a stored SCHEDULED appointment. | Stored SCHEDULED appointment with the registered objects | Adds positive evidence not covered by the 8 supplied tests |
| T-752 | Supporting contract (see docstring) | AC-03.2 | Negative | an unknown patient prevents booking. | LookupError for unknown patient; nothing stored | Adds negative evidence not covered by the 8 supplied tests |
| T-753 | Supporting contract (see docstring) | AC-03.2 | Negative | an unknown practitioner prevents booking. | LookupError for unknown practitioner; nothing stored | Adds negative evidence not covered by the 8 supplied tests |
| T-754 | NFR-01 | No canonical AC; quoted contract: see test docstring | Negative | an invalid datetime leaves the store unchanged. | ValueError for seconds in time; nothing stored | Adds negative evidence not covered by the 8 supplied tests |
| T-755 | BR-03 | No canonical AC; quoted contract: see test docstring | Negative | a repeated appointment ID is rejected and the original time is kept. | ValueError; original appointment and time kept; one stored | Adds negative evidence not covered by the 8 supplied tests |
| T-756 | FR-08 | AC-06.1 | Positive | known ID returns the object, a valid unknown ID raises LookupError, a blank ID raises ValueError. | Known ID returns object; unknown LookupError; blank ValueError | Adds positive evidence not covered by the 8 supplied tests |
| T-761 | FR-05 | AC-04.1 | Negative | same practitioner, exact time and an existing SCHEDULED appointment is rejected without changing state. | ValueError; second appointment not stored | Adds negative evidence not covered by the 8 supplied tests |
| T-762 | FR-05 | AC-04.2 | Positive | conflicts belong to a practitioner. | Different practitioner at the same time is stored | Adds positive evidence not covered by the 8 supplied tests |
| T-763 | FR-05 boundary | No canonical AC; quoted contract: see test docstring | Boundary | the rule is exact time, not an overlap. | Booking one minute later is allowed | Adds boundary evidence not covered by the 8 supplied tests |
| T-764 | FR-05, BR-05, BR-08 | No canonical AC; quoted contract: see test docstring | Boundary | only SCHEDULED appointments conflict, so a COMPLETED one at the same time does not. | COMPLETED appointment does not block a new booking | Adds boundary evidence not covered by the 8 supplied tests |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| T-701 | Patient("  P1  ", "  Alex Example  ") | Construct the patient | patient_id == "P1" and name == "Alex Example" | Proves trimming and storing of valid data (partial AC-01.1); fails if values were left untrimmed. |
| T-724 | Valid patient and practitioner; times with seconds, microseconds, a timezone, a string and None | Construct an Appointment with each time | pytest.raises(ValueError) for each | Proves the minute-precision naive datetime contract; a broad pass-anything check would not. |
| T-733 | Appointment A1 SCHEDULED | cancel() twice | Second call raises ValueError; status is still CANCELLED | Proves AC-05.3 and that the rejection leaves state unchanged. |
| T-742 | Patient P1 registered | register_patient("  P1  ", "Someone Else") | ValueError; store returns the original object; name unchanged; one patient | Proves AC-01.2 with trimming, and that nothing was overwritten. |
| T-751 | P1 and D1 registered | book_appointment("A1", "P1", "D1", time) | status is SCHEDULED; patient and practitioner are the registered objects; store returns the same object | Proves AC-03.1 through the full workflow, not just construction. |
| T-761 | A1 booked for D1 at 09:00 | book A2 for D1 at 09:00 | ValueError; A2 not found; list equals [A1] | Proves AC-04.1 and rejection without partial state. |
| T-762 | A1 booked for D1; D2 registered | book A2 for D2 at the same time | A2 is SCHEDULED; list is [A1, A2] | Proves AC-04.2, conflicts belong to a practitioner. |
| T-764 | COMPLETED A1 for D1 at 09:00 added via the store | book A2 for D1 at 09:00 | A2 is SCHEDULED | Proves only SCHEDULED appointments conflict (FR-05, BR-05, BR-08). |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| T-701 | valid data is kept, trimmed. | tests/test_domain.py::test_t701_patient_keeps_trimmed_id_and_name | Passed |
| T-702 | IDs are non-blank strings. | tests/test_domain.py::test_t702_patient_rejects_blank_or_non_text_id | Passed |
| T-703 | a required name cannot be blank. | tests/test_domain.py::test_t703_patient_rejects_blank_name | Passed |
| T-704 | IDs are case-sensitive. | tests/test_domain.py::test_t704_patient_id_keeps_its_case | Passed |
| T-705 | identity is changed only at creation. | tests/test_domain.py::test_t705_patient_id_is_read_only | Passed |
| T-711 | ID, name and specialty are kept, trimmed. | tests/test_domain.py::test_t711_practitioner_keeps_trimmed_fields | Passed |
| T-712 | ID, name and specialty are each required. | tests/test_domain.py::test_t712_practitioner_rejects_each_blank_required_field | Passed |
| T-721 | starts SCHEDULED, refers to the actual participant objects. | tests/test_domain.py::test_t721_new_appointment_is_scheduled_with_same_objects | Passed |
| T-722 | appointment ID is required. | tests/test_domain.py::test_t722_appointment_rejects_blank_id | Passed |
| T-723 | participants must be real domain objects. | tests/test_domain.py::test_t723_appointment_rejects_wrong_participant_types | Passed |
| T-724 | naive minute-precision datetime only. | tests/test_domain.py::test_t724_appointment_rejects_invalid_date_time | Passed |
| T-725 | status must be an AppointmentStatus member. | tests/test_domain.py::test_t725_appointment_rejects_non_enum_status | Passed |
| T-726 | COMPLETED is a valid test fixture state. | tests/test_domain.py::test_t726_completed_status_can_be_supplied_at_construction | Passed |
| T-731 | SCHEDULED becomes CANCELLED. | tests/test_domain.py::test_t731_cancel_changes_scheduled_to_cancelled | Passed |
| T-732 | cancelling changes state only. | tests/test_domain.py::test_t732_cancel_keeps_the_record_and_its_fields | Passed |
| T-733 | a second cancel raises ValueError. | tests/test_domain.py::test_t733_repeated_cancel_is_rejected_without_change | Passed |
| T-734 | only SCHEDULED can be cancelled. | tests/test_domain.py::test_t734_completed_appointment_cannot_be_cancelled | Passed |
| T-735 | state changes only through cancel(). | tests/test_domain.py::test_t735_status_cannot_be_assigned_directly | Passed |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| T-601 | lookup returns the actual stored patient. | Supporting contract (see docstring); AC-02.1 | tests/test_services.py::test_t601_find_patient_returns_registered_object | Passed |
| T-602 | a valid but unknown ID reports absence. | Supporting contract (see docstring); AC-02.2 | tests/test_services.py::test_t602_find_patient_unknown_id_raises_lookup_error | Passed |
| T-603 | a failed lookup does not add a replacement. | Supporting contract (see docstring); AC-02.2 | tests/test_services.py::test_t603_find_patient_unknown_id_creates_nothing | Passed |
| T-604 | a blank ID is invalid, which differs from absent. | FR-02; No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t604_find_patient_blank_id_raises_value_error | Passed |
| T-605 | surrounding spaces are trimmed before lookup. | FR-02; No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t605_find_patient_trims_whitespace | Passed |
| T-606 | P1 and p1 are different identifiers. | FR-02; No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t606_find_patient_is_case_sensitive | Passed |
| T-611 | lookup returns the stored practitioner. | FR-03 support; No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t611_find_practitioner_returns_registered_object | Passed |
| T-612 | a valid but unknown practitioner ID reports absence. | Supporting contract (see docstring); No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t612_find_practitioner_unknown_id_raises_lookup_error | Passed |
| T-613 | a blank practitioner ID is invalid. | Supporting contract (see docstring); No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t613_find_practitioner_blank_id_raises_value_error | Passed |
| T-614 | IDs are trimmed and case-sensitive. | Supporting contract (see docstring); No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t614_find_practitioner_trims_and_is_case_sensitive | Passed |
| T-621 | a SCHEDULED appointment becomes CANCELLED. | Supporting contract (see docstring); AC-05.1 | tests/test_services.py::test_t621_cancel_changes_status_and_returns_same_object | Passed |
| T-622 | the same object is still retrievable. | FR-07; AC-05.2 | tests/test_services.py::test_t622_cancelled_appointment_is_retained_in_history | Passed |
| T-623 | cancelling twice raises and changes nothing. | Supporting contract (see docstring); AC-05.3 | tests/test_services.py::test_t623_repeated_cancellation_is_rejected_without_change | Passed |
| T-624 | COMPLETED is not cancellable. | BR-06, BR-08; No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t624_completed_appointment_cannot_be_cancelled | Passed |
| T-625 | an unknown appointment ID raises LookupError. | Supporting contract (see docstring); No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t625_cancel_unknown_id_raises_lookup_error_without_change | Passed |
| T-626 | a blank appointment ID is invalid, not merely absent. | Supporting contract (see docstring); No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t626_cancel_blank_id_raises_value_error | Passed |
| T-627 | a padded ID works and only the target changes. | Supporting contract (see docstring); No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t627_cancel_trims_id_and_other_appointments_unchanged | Passed |
| T-628 | a CANCELLED appointment no longer conflicts. | BR-05; No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t628_cancelled_slot_does_not_block_rebooking | Passed |
| T-741 | complete service evidence of storage. | FR-01; AC-01.1 | tests/test_services.py::test_t741_registered_patient_is_stored_and_retrievable | Passed |
| T-742 | a padded copy of an existing ID is a duplicate, and the original record is not overwritten. | Supporting contract (see docstring); AC-01.2 | tests/test_services.py::test_t742_trimmed_duplicate_patient_id_is_rejected | Passed |
| T-743 | IDs are case-sensitive, so P1 and p1 can both be registered. | Supporting contract (see docstring); Quoted contract: validation contract | tests/test_services.py::test_t743_different_case_patient_id_is_a_different_patient | Passed |
| T-744 | rejection stores nothing. | NFR-01; Quoted contract: validation contract | tests/test_services.py::test_t744_blank_patient_registration_leaves_store_empty | Passed |
| T-745 | the original practitioner is preserved. | FR-03, BR-02; No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t745_duplicate_practitioner_id_is_rejected_without_overwrite | Passed |
| T-751 | registered participants, unique ID and a free time give a stored SCHEDULED appointment. | FR-04; AC-03.1 | tests/test_services.py::test_t751_booking_stores_scheduled_appointment_with_real_objects | Passed |
| T-752 | an unknown patient prevents booking. | Supporting contract (see docstring); AC-03.2 | tests/test_services.py::test_t752_booking_unknown_patient_is_rejected_and_nothing_stored | Passed |
| T-753 | an unknown practitioner prevents booking. | Supporting contract (see docstring); AC-03.2 | tests/test_services.py::test_t753_booking_unknown_practitioner_is_rejected | Passed |
| T-754 | an invalid datetime leaves the store unchanged. | NFR-01; No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t754_booking_with_invalid_time_stores_nothing | Passed |
| T-755 | a repeated appointment ID is rejected and the original time is kept. | BR-03; No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t755_duplicate_appointment_id_does_not_replace_original | Passed |
| T-756 | known ID returns the object, a valid unknown ID raises LookupError, a blank ID raises ValueError. | FR-08; AC-06.1 | tests/test_services.py::test_t756_find_appointment_known_unknown_and_blank | Passed |
| T-761 | same practitioner, exact time and an existing SCHEDULED appointment is rejected without changing state. | FR-05; AC-04.1 | tests/test_services.py::test_t761_same_practitioner_same_time_conflicts | Passed |
| T-762 | conflicts belong to a practitioner. | FR-05; AC-04.2 | tests/test_services.py::test_t762_different_practitioner_same_time_is_allowed | Passed |
| T-763 | the rule is exact time, not an overlap. | FR-05 boundary; No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t763_one_minute_apart_does_not_conflict | Passed |
| T-764 | only SCHEDULED appointments conflict, so a COMPLETED one at the same time does not. | FR-05, BR-05, BR-08; No canonical AC; quoted contract: see test docstring | tests/test_services.py::test_t764_completed_appointment_does_not_block_the_slot | Passed |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Blank patient ID | "", "   ", tab/newline, None, 123 | ValueError | T-702 |
| Whitespace-only patient name | "", "   ", None | ValueError | T-703 |
| Whitespace-only practitioner ID, name, specialty | Each field blank in turn | ValueError | T-712 |
| Case-sensitive ID | "p1" versus "P1" | Different identities | T-704, T-743, T-606 |
| Trimmed duplicate patient ID | Register "  P1  " when P1 exists | ValueError; original unchanged | T-742 |
| Trimmed duplicate practitioner ID | Register " D1 " when D1 exists | ValueError; original unchanged | T-745 |
| Invalid appointment time | Seconds, microseconds, timezone, string, None | ValueError; nothing stored | T-724, T-754 |
| Non-enum status | "scheduled" as a string | ValueError | T-725 |
| Same practitioner, same exact time, SCHEDULED | Second booking at the same time | ValueError; second not stored | T-761 |
| Different practitioner, same time | D2 at the same time as D1 | Allowed | T-762 |
| One minute apart | 09:01 after 09:00 for the same practitioner | Allowed (exact-time rule, no overlap rule) | T-763 |
| COMPLETED or CANCELLED appointment at the slot | New booking for the same practitioner and time | Allowed | T-764, T-628 |
| Repeated cancellation | cancel() twice | ValueError; status stays CANCELLED | T-733, T-623 |
| Cancel a COMPLETED appointment | cancel() on COMPLETED | ValueError; status unchanged | T-734, T-624 |
| Unknown participant at booking | P9 or D9 | LookupError; nothing stored | T-752, T-753 |
| Duplicate appointment ID | Book A1 again at another time | ValueError; original time kept | T-755 |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
Acceptance criterion: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
Behaviour to test: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
Human-first test idea/categories: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
Prompt and purpose: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
- What it claims to verify: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
- Requirement trace: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
- Assertion quality: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
- Human critique: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
- Decision: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
- Reason: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
- Final test reference if accepted/modified: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
- Actual verification result: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
Why was it weak? PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
How did you strengthen it? PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session
Accepted / modified / rejected test decisions and evidence: PENDING: GitHub Copilot has not been used yet; to be completed from a real Copilot session

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| python -m pytest | project/ | b7496a8da4d1929c59c63ec21d756dfb39abc336 (merged main after PR #6); PR branch head 4878b8755859beb3e62c1bdc68a95afc37e366d8 | 76 | 0 | None | None found | Run before the PR on the branch (76 passed) and again on main after the merge (76 passed): 31 test_domain.py, 37 test_services.py, 8 test_starter.py. Python 3.14.2, pytest 8.3.5. |

Individual test runs and changed-order independence evidence: python -m pytest tests/test_domain.py::test_t733_repeated_cancel_is_rejected_without_change gave 1 passed. python -m pytest tests/test_services.py::test_t764_completed_appointment_does_not_block_the_slot tests/test_domain.py::test_t733_repeated_cancel_is_rejected_without_change tests/test_services.py::test_t761_same_practitioner_same_time_conflicts (an order different from the files) gave 3 passed. Both run in project/ on the PR branch at 4878b87.
Optional tutor-led demonstration notes: Not used.
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: No failures or defects occurred in Stage 7, so no diagnosis or production change. Separate note: in an isolated copy (not run by the student), Claude deliberately broke the production code nine ways and ran the new suite. Eight changes were detected by a failing test (conflict ignoring status, practitioner or exact time, untrimmed IDs, seconds allowed, duplicate patient overwrite, repeat cancel, missing unknown-patient check). One was not detected: removing the service duplicate-appointment-ID check, because the data store rejects duplicates as well, so behaviour is unchanged.

## K What the Suite Still Does Not Prove

What does your test suite still not prove? DRAFT from the Claude review, to be checked and reworded by the student: it does not test the console menu or practitioner listing and sorting (Stage 9), and it does not test whole multi-step workflows across the program. Passing tests cover only the cases they check, not every possible input.
Coverage if used: not used
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? The console menu, practitioner listing and sorting (Stage 9) and whole multi-step workflows matter most, because users reach the system through them and they are not yet tested. A coverage percentage only counts executed lines, not whether the assertions are meaningful or the inputs and boundaries are covered, so it cannot show correctness.
Optional fixtures/parametrisation used and why, if any: Parametrisation (pytest.mark.parametrize) is used for several blank and invalid inputs (T-702, T-703, T-712, T-724) so each bad value is its own case. Fixtures are not used; plain helper functions (fresh_session, booked_session, make_people) give fresh setup in each test.

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| https://github.com/mithunnaveen1/st1-assignment-3/issues/5 (Stage 7: Requirement-linked domain and service tests) | feature/stage7-tests | https://github.com/mithunnaveen1/st1-assignment-3/pull/6 | None independent (solo group; tutor approved self-review). Self-review comment and a Claude review comment (not independent, not Copilot) on the PR | Claude review: Optional notes on T-755 overlap (rejected), service duplicate-appointment-ID check not caught by a test because the store also checks it (accepted as a note), PR wording of 31 test cases from 18 functions (accepted and corrected), gaps in test ID numbering (accepted as a note) | Merged into main as b7496a8da4d1929c59c63ec21d756dfb39abc336; 76 passed on main |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| mithunnaveen1 | Reviewed the tests, ran the full and individual suites, created the issue and PR, wrote the self-review, merged and re-verified main. The tests and TEST IDs were drafted with Claude (AI assistant, not Copilot) and the tutor allowed this; Claude also wrote a labelled review. | https://github.com/mithunnaveen1/st1-assignment-3/pull/6 and https://github.com/mithunnaveen1/st1-assignment-3/issues/5 |

## N Formative Questions

1. What question does verification answer?
Verification asks: are we building the product right? That is, does the code meet its specified requirements and contracts, which tests help check.

2. What question does validation answer?
Validation asks: are we building the right product? That is, does it meet the real needs of its users and stakeholders.

3. What is a unit test?
A unit test checks one small piece of behaviour, such as one function or method, in isolation and with a clear expected result.

4. What is a pytest fixture?
A pytest fixture is reusable setup code (for example creating a fresh data store) that tests receive automatically, so each test starts from a known state. This project used plain helper functions instead.

5. What is parametrisation in pytest?
Parametrisation runs the same test with several input and expected-value sets, so each case is reported separately without duplicating test code. It is used here for blank and invalid inputs.

6. What is regression testing?
Regression testing re-runs the accumulated tests after a change to check that existing behaviour still works. Here the full suite was run on the branch and again on main after the merge.

7. What does code coverage tell us, and what does it not prove?
Coverage tells us which lines or branches the tests executed. It does not prove the assertions are strong, that the requirements are met, or that untested inputs and boundaries are handled.

8. What makes an assertion weak?
An assertion is weak when it cannot fail for a wrong result or checks too little, such as assert True or is not None, so it would still pass when the code is broken.

9. What is the appropriate role of GitHub Copilot as a test assistant?
Copilot can suggest test ideas and extra cases, but it is only an assistant. Its tests must be traced to requirements, checked for meaningful assertions and scope, and failing or weak ones rejected. The author stays responsible.

10. What is the Stage 7 engineering rule?
Every test must trace to a requirement and contain a meaningful assertion, tests must be run rather than trusted, and AI-generated tests are reviewed before use. Passing tests are evidence only for what they actually check.

## O Stage Completion

Tested Stage 7 main SHA: b7496a8da4d1929c59c63ec21d756dfb39abc336
Full-suite result: 76 passed, 0 failed (python -m pytest in project/ on main, Python 3.14.2, pytest 8.3.5)
Unresolved defects and effect on baseline: No product or test defects found. Open items: GitHub Copilot candidate-test activity (H, I) not done; sections A, K and N were drafted with Claude and reviewed by the student (disclosed).
Clean working tree and integration evidence: PR #6 merged; git pull --ff-only moved main from 562d157 to b7496a8 with no local changes; full suite re-run on main.
Stage 8 handover status: Code and tests are integrated and verified. Only the Copilot items (H, I) remain outstanding. No Stage 8 work has been done.
All tutorial/formative responses and traceability/Copilot decisions complete: Not fully. Traceability and sections A, K and N are complete (Claude-drafted, student-reviewed). The Copilot items (H, I) are pending until real Copilot use.

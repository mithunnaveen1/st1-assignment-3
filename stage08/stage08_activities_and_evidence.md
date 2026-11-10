# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Solo group (UG), approved by the tutor
Members and UG/PG cohorts: Mithun Naveen (mithunnaveen1), UG
Record owner / contribution links for each member: mithunnaveen1 (sole member). Contribution links are in section I once the PR exists. Tutorial and formative responses (A, K) were drafted with Claude (AI assistant, not Copilot; the tutor allows Claude) and reviewed by the student.

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason:
1. "Appointment disappears after cancellation." Symptom. It is what a user observes. It says nothing about why it happens.
2. "The data-store removal path is probably being called." Hypothesis. It is a testable guess ("probably"), and it must be checked against the code, which has no public delete operation.
3. "The failing test shows store.find_appointment('A1') returns None." Evidence. It is a concrete observed result from a test run.
4. "The service layer is badly designed." Opinion. It is a vague judgement with no check that could confirm or refute it.
5. "Traceback points to smartcare/services.py line 42 in the example." Evidence, but only of where the failure was observed. It is a location, not proof of the root cause, which may be elsewhere.

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason (cancelled-history scenario):
- Expected: after cancel_appointment('A1'), the same appointment object is still stored with status CANCELLED, and find_appointment('A1') returns it and it appears in listings (FR-06, FR-07, BR-07, AC-05.2).
- Observed (tutorial example): after cancelling, find_appointment('A1') returns None.
- Minimal reproduction: register one patient and one practitioner, book A1, cancel A1, then call data_store.find_appointment('A1') and check its status.
- Hypothesis: the cancellation path or a store method removes the appointment instead of just changing its status.
- Evidence to inspect: the cancel code in domain.py and services.py, the store's find and list methods, and whether the stored list still contains the object after cancel. A competing explanation is that the store's find method filters out cancelled appointments, so the data is kept but not found.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: Change the test, not the code. FR-07 requires cancelled appointments to be retained with CANCELLED status, so a test expecting deletion contradicts the requirement and is a test defect. A failing test is only a signal and is not automatically right. A test expecting different practitioners at the same time to conflict does not reflect AC-04.2, which allows different practitioners at the same time. Only the same practitioner at the same time conflicts (AC-04.1), so that test is also a test defect and should be corrected.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason:
Smells: duplicate status strings (magic strings), direct manipulation of a collection instead of the SmartCareDataStore boundary, printing inside a service (mixed responsibilities), validation mixed into the booking logic, and four nested conditionals, all in a 70-line method.
Small refactorings: replace the strings with AppointmentStatus, call the store's add/find/list methods, remove printing and return values or raise exceptions instead, move validation into the domain constructors or helper functions, and use early returns or guard clauses to flatten the nesting. Do each change on its own with the tests passing.
Classification:
- Rename appt to appointment: refactoring (behaviour unchanged).
- Extract a repeated conflict helper: refactoring.
- Add rescheduling: feature (new behaviour, outside debugging).
- Restore retained cancellation lookup: repair (it restores required behaviour from FR-07/FR-08).
- Replace a magic status string with the existing enum: refactoring.
Behaviour that must stay unchanged: return values and object identity, the exceptions raised (LookupError for absent, ValueError for invalid), state transitions, and that failed operations leave state unchanged.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: NOT DONE. This needs a real failure from the prepared faulty project, and the Stage 8 utility was not available to me, so no failure was observed and nothing is claimed.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: Changing code straight away is guessing. The change may fix a symptom while the real cause remains, may introduce new faults, and destroys the evidence of the original failure. It is better to reproduce the failure, state the expected behaviour from a requirement, form a hypothesis, check it with evidence, then make the smallest fix and keep a regression test.


Classification responses (1–5, each with reason): see A.1.
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: see A.2.
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: NOT DONE, see A.5.

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: b7496a8da4d1929c59c63ec21d756dfb39abc336 (main after PR #6); SmartCare A3 Requirements Baseline 2026, revision 2.
- Baseline test command / working directory / observed result / evidence: python -m pytest in project/ gave 76 passed (31 test_domain.py, 37 test_services.py, 8 test_starter.py), Python 3.14.2, pytest 8.3.5. Stage 7 record, section J.
- Clean preparation SHA if a record-only commit followed Stage 7: f07a51a (PR #7, evidence-only: Stage 6 and 7 records; no code changes). To be confirmed with git rev-parse HEAD just before preparation.
- Branch and preparer / how teammates obtained this branch: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Downloaded tool version, source SHA256 and --check outcome: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- --apply and --verify output summaries / artefact references: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Bounded diff inspected and recovery location (not committed): NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Prepared faulty-state commit SHA: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Preparation or recovery issues and resolution, if any: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Initial prepared full-suite command / result / key failures: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Expected behaviour and requirement: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Minimal synthetic reproduction steps: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Meaningful failing test path/name and exact relevant failure: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Smallest justified fix / diff / why other behaviour is preserved: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Repair SHA / focused verification result: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Expected behaviour and requirement: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Minimal synthetic reproduction steps: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Meaningful failing test path/name and exact relevant failure: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Smallest justified fix / diff / why other behaviour is preserved: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
- Repair SHA / focused verification result: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Evidence intended to inspect / competing explanation / discriminating check: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Member and saved sequence/time or commit showing this preceded consultation: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.

### F8-02 human entry
Likely cause and why plausible: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Evidence intended to inspect / competing explanation / discriminating check: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Member and saved sequence/time or commit showing this preceded consultation: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Final human conclusion and comparison with initial hypothesis: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.

### F8-02 Copilot review
Actual prompt / output reference and member: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Final human conclusion and comparison with initial hypothesis: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. |
| F8-01 after repair | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. |
| F8-02 before repair | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. |
| F8-02 after repair | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. |
| Full suite after both repairs, before refactor | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. | NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed. |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Unrelated failures investigated / resolution: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.

## H. Refactoring decision and before/after verification

Smell and exact location: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Small proposed structural change / why justified: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
External behaviour to preserve / relevant tests: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Focused and full after-refactor commands / working directory / results / evidence: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Branch / prepared, repair and refactor checkpoints: NOT DONE (no Stage 8 branch or PR exists).
PR link and another member's reviewer identity: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Key human feedback, difference from Copilot findings and response/outcome: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Actual review approval / merge evidence: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Integrated code SHA and team pull/retest command / working directory / result: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Evidence-only later SHA / explanation if different: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.
Each member's substantive contribution and artefact: NOT DONE: the Stage 8 preparation utility (prepare_debugging.py v1.1) was not available to me, so the two prepared defects were never applied. No results are claimed.

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? No Stage 8 Copilot diagnosis exists, because the defects were never prepared. The closest real example is from Stage 7: Copilot's candidate test for AC-04.2 (different practitioner at the same time) looked complete, but its assertions mostly compared an appointment ID with itself and could hardly fail (see stage07/copilot_stage7_output.md).
2. What evidence changed your group's view? NOT DONE for Stage 8. From Stage 6: Copilot said the test count could not be verified and that T-601 to T-628 looked inconsistent with 22 tests; counting the real file (18 functions, 22 collected cases, deliberate ID gaps) showed that part of the claim was a gap in what I gave Copilot, not a defect.
3. How did regression tests protect the refactoring? NOT DONE: no Stage 8 refactor was made. The retained 76-test suite is the safety net that would protect one, and it passed on main after each merge.

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: Stop and diagnose first. Observe the exact failure, reproduce it with a small input, state the expected behaviour from a requirement and form a hypothesis, then gather evidence before changing any code.

2. Where should expected behaviour come from during debugging?

Response: From the requirements and the published contracts (for example FR-05, FR-07, AC-04.1, AC-04.2, BR-07), not from what the current code or a failing test happens to do.

3. What is a debugging hypothesis?

Response: A testable explanation of why a failure occurs, such as "the store method filters out cancelled appointments". It can be confirmed or disproved by a specific check. An opinion with no check is not a hypothesis.

4. What is a regression test and why is it retained?

Response: A test that protects behaviour that already works or that a defect broke, so a later change cannot silently break it again. It is retained and re-run in the full suite after every change.

5. What is meant by root cause?

Response: The underlying reason the failure happens, such as the faulty decision in the code, rather than where the failure is observed. Fixing the root cause removes the defect, while fixing the symptom may not.

6. What is refactoring?

Response: Changing the internal structure of code without changing its external behaviour, to improve readability or responsibility. It is done in small steps with the tests passing before and after.

7. What is a swallowed exception?

Response: An exception that is caught and ignored or hidden (for example a bare except with pass), so the failure is not reported and the problem is hidden instead of fixed.

8. What is a code smell?

Response: A sign in the code that may point to a deeper problem, such as duplication, a very long method, magic strings, unclear names or misplaced responsibility. It is not itself a bug.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: As hypotheses, not facts. Each suggestion is checked against requirements, execution and code evidence, classified as correct, partly correct or wrong, and accepted, modified or rejected. Confidence is not proof.

10. What is the Stage 8 engineering rule?

Response: Diagnose before you fix: reproduce, use the requirement and evidence to find the cause, make the smallest repair, keep a regression test, and verify with the full suite.

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: main at submission. The last code/test SHA is b7496a8da4d1929c59c63ec21d756dfb39abc336 (76 passed); later commits (f07a51a, 7d6d4ce and this record) are evidence-only. No Stage 8 code changes exist.
Unresolved issues or incomplete checks / owner / next action: Stage 8 diagnosis, repairs, regression tests, refactor, Copilot diagnosis reviews and PR review were not done, because the Stage 8 preparation utility was not supplied to me and I could not reach the tutor before the deadline. Owner: mithunnaveen1. Next action: obtain prepare_debugging.py v1.1 from the tutor and complete Stage 8 following section 3 of the handout. Nothing in this record claims a result that did not happen.
Handover note: Stages 6 and 7 are complete, integrated and verified (76 tests pass on main). The tutorial and formative parts of this Stage 8 record (A.1 to A.4, A.6, K) are complete and were drafted with Claude and reviewed by the student. All other Stage 8 sections are marked NOT DONE with the reason. Stage 9 was not started, as the handout requires Stage 8 to be integrated first.

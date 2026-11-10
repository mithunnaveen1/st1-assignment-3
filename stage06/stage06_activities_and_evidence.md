# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: [response]
- Members, GitHub usernames and cohorts: Mithun Naveen, mithunnaveen1, UG (sole member; solo group approved by tutor)
- Repository URL: https://github.com/mithunnaveen1/st1-assignment-3
- Starting SHA: 6f7bf1e (Add shared SmartCare Assignment 3 starter)

## A Requirement to issue activities

### FR-02 Patient Search

- Title: FR-02: Find a patient by patient ID
- Context: PatientService.find_patient raised NotImplementedError, so staff could not retrieve a registered patient through the service layer.
- Requirement: FR-02 (AC-02.1, AC-02.2). IDs are strings, trimmed, non-blank and case-sensitive.
- Acceptance criteria: A registered ID returns the same stored Patient object; a valid but unknown ID raises LookupError and adds nothing to the store; a blank or whitespace-only ID raises ValueError; " P1 " finds P1 but "p1" does not.
- Scope: PatientService.find_patient in project/smartcare/services.py and its tests in project/tests/test_services.py only. No changes to domain.py or data_store.py.
- Definition of Done: Criteria covered by passing tests, full suite passes, diff reviewed, PR merged, main re-tested.
- Owner: mithunnaveen1
- Actual issue link: https://github.com/mithunnaveen1/st1-assignment-3/issues/1

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: FR-06/FR-07: Cancel a scheduled appointment and keep its history
- Context: AppointmentService.cancel_appointment raised NotImplementedError. The domain method Appointment.cancel() already enforces the state rule.
- Requirement: FR-06, FR-07 (AC-05.1, AC-05.2, AC-05.3), BR-06, BR-07.
- Acceptance criteria: Cancelling a SCHEDULED appointment sets CANCELLED and returns the same object; the cancelled appointment stays retrievable by ID and in the session list; cancelling again or cancelling a COMPLETED appointment raises ValueError and leaves status unchanged; an unknown ID raises LookupError and a blank ID raises ValueError; booking and the conflict rule still work.
- Scope: AppointmentService.cancel_appointment and its tests only. The service uses Appointment.cancel(); it does not set the status itself and does not delete anything.
- Definition of Done: Criteria covered by passing tests, full suite passes, diff reviewed, PR merged, main re-tested.
- Owner: mithunnaveen1
- Actual issue link: https://github.com/mithunnaveen1/st1-assignment-3/issues/3

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | [select] | [response] |
| final version | [select] | [response] |
| Add patient search by ID | [select] | [response] |
| fix stuff | [select] | [response] |
| Prevent cancellation of completed appointments | [select] | [response] |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: [response]
- Responsibility and architecture concerns: [response]
- Testing and review concerns: [response]
- Changes to remove or separate, with reasons: [response]

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: [response]
- Follow-up review question 1: [response]
- Follow-up review question 2: [response]
- Follow-up review question 3: [response]
- Follow-up review question 4: [response]
- Follow-up review question 5: [response]
- Additional questions if useful: [response]

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | [response] |
| Commit message convention | [response] |
| PR size | [response] |
| Another-member review requirement | [response] |
| Merge rule | [response] |
| Significant Copilot disclosure rule | [response] |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| https://github.com/mithunnaveen1/st1-assignment-3/issues/1 | FR-02 | mithunnaveen1 | Issue #1 acceptance criteria (stored lookup, LookupError, ValueError, trimmed and case-sensitive IDs) | Open; closes when PR #4 merges |
| https://github.com/mithunnaveen1/st1-assignment-3/issues/2 | Supporting practitioner lookup for FR-03 | mithunnaveen1 | Issue #2 acceptance criteria (same contract for practitioners) | Open; closes when PR #4 merges |
| https://github.com/mithunnaveen1/st1-assignment-3/issues/3 | FR-06 and FR-07 | mithunnaveen1 | Issue #3 acceptance criteria (guarded cancellation, retained history, errors) | Open; closes when PR #4 merges |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: https://github.com/mithunnaveen1/st1-assignment-3/pull/4 , Add patient/practitioner lookup and appointment cancellation (Stage 6)
- Linked issue and requirement: Closes #1 (FR-02), #2 (practitioner lookup supporting FR-03), #3 (FR-06 and FR-07)
- Feature branch: feature/stage6-lookups-and-cancel
- Changed behaviour: find_patient and find_practitioner return the stored object, raise LookupError for a valid unknown ID and ValueError for a blank ID; cancel_appointment finds the appointment, calls Appointment.cancel() and returns the same object, keeping history. New project/tests/test_services.py with 22 tests (T-601 to T-628).
- Meaningful commits: https://github.com/mithunnaveen1/st1-assignment-3/commit/c404b17
- Test command, directory and observed result: python -m pytest, run in project/, 30 passed (8 supplied plus 22 new), Python 3.14.2, pytest 8.3.5, tested code SHA c404b17
- Another-member reviewer: None. The group has a single member (solo group approved by the tutor), and the tutor approved self-review for this arrangement.
- Human observations recorded before Copilot: https://github.com/mithunnaveen1/st1-assignment-3/pull/4 (Conversation tab, self-review comment by mithunnaveen1, posted before the Claude review and before any Copilot use).
- Requirement, responsibilities, test assertions and unrelated-scope checks: Read the Files changed tab. Checked that find_patient raises LookupError for a valid unknown ID through the "if patient is None" check, that the rule stopping a second cancellation is in Appointment.cancel() in domain.py with the service only calling it, and that test T-623 would fail if the second cancel did not raise ValueError. Only two files changed. No risks or missing items noticed.
- Key feedback: Claude review (AI assistant, not independent, not Copilot): (1) Optional: test T-627 had unused setup lines; (2) Optional: find_patient and find_practitioner are near-identical; (3) Optional: test IDs skip some numbers (for example T-607 to T-610).
- Author response/change and verification: Accepted finding 1 and removed the unused lines in commit 069aa91 (1 insertion, 4 deletions). Rejected finding 2 (3 lines each, an abstraction adds complexity). Finding 3 accepted as a note here only: IDs T-607 to T-610 and T-615 to T-620 are intentionally unused; no code change. Verified by python -m pytest in project/ after the merge: 30 passed.
- Reviewer recheck and approval: No independent approval exists. GitHub does not allow approving your own PR, so the review was submitted as a Comment. The author merged after the self-review under the tutor-approved solo arrangement.
- Merge outcome and SHA: PR #4 merged into main with a merge commit, 562d15712c8de0bb587b7f3b72b6fa9022c9594b. The branch head merged was 069aa91162edc30b065913070cd4584473a918e9.
- Significant Copilot assistance: None so far. GitHub Copilot has not been used and its comparison is pending (see H and I). Significant AI assistance from Claude (not Copilot) is disclosed: Claude drafted the three service methods, test_services.py and the issue drafts, and wrote the Claude review. The author read the code, ran the tests and wrote the self-review. The tutor said using Claude is allowed.
- Linked issue closure: [response]
- Each member updated main: mithunnaveen1 (sole member) ran git switch main and git pull --ff-only; main moved from 6f7bf1e to 562d157.
- Integrated verification after merge: python -m pytest in project/ on main, 30 passed (8 supplied plus 22 new), Python 3.14.2, pytest 8.3.5, code SHA 562d15712c8de0bb587b7f3b72b6fa9022c9594b

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: PENDING. No GitHub Copilot interaction has taken place yet, so nothing is recorded here. This section will be completed from a real Copilot session, not written in advance.
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: find_patient raises LookupError via the "if patient is None" check; the rule stopping a repeat cancellation is in Appointment.cancel() in domain.py and the service only calls it; test T-623 would fail if the second cancel did not raise ValueError; no risks or missing items noticed.
- Copilot noticed: PENDING. The Copilot comparison has not been done. The comparison below is with a Claude review only, clearly not a Copilot review.
- Overlap: PENDING for Copilot. With the Claude review: both agreed the three methods meet the issue criteria and that the cancellation rule lives in the domain method.
- What did the human reviewer notice that Copilot did not: PENDING for Copilot.
- What did Copilot identify that the human reviewer initially missed: PENDING for Copilot. The Claude review found unused setup lines in test T-627, near-duplicate lookup code, and gaps in the test ID numbering, which the human review had missed. Claude also noted that its own review is not independent because it drafted the code.
- Unsupported or incorrect Copilot suggestion: PENDING for Copilot. None identified in the Claude review.
- Human judgement accepted, modified or rejected, and why: Accepted the T-627 cleanup (small and removes clutter), rejected the duplication point (an abstraction is not worth it for 3-line methods), and accepted the test ID gap as a note only.
- Which evidence justified merge approval: The self-review against the issue criteria, 30 passing tests (8 supplied plus 22 new), the reviewed two-file diff, and the T-627 fix. There was no independent approval and the Copilot comparison was still pending at merge, which is a recorded gap.

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[response]

## L Stage 6 formative questions

1. What is version control?

[response]

2. Why is a feature branch useful?

[response]

3. What makes a commit a good engineering commit?

[response]

4. What is a pull request?

[response]

5. What is the purpose of code review?

[response]

6. What does a Git diff show?

[response]

7. What is a Definition of Done?

[response]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[response]

9. Why should individual contribution not be judged only by commit count?

[response]

10. What is the Stage 6 engineering rule?

[response]

## M Completion and handover

- Starting SHA: 6f7bf1e
- Final Stage 6 code SHA: 069aa91162edc30b065913070cd4584473a918e9 (PR branch head); merged main SHA 562d15712c8de0bb587b7f3b72b6fa9022c9594b
- Test command: python -m pytest
- Working directory: project/
- Observed result: 30 passed on merged main (562d157), run in project/ with python -m pytest, Python 3.14.2, pytest 8.3.5
- PR and another-member reviewer: https://github.com/mithunnaveen1/st1-assignment-3/pull/4 ; no other member (solo group, self-review approved by tutor)
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.

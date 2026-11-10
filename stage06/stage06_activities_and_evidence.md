# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Solo group (UG), one member, approved by the tutor
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
| changes | Weak | Says nothing about what changed or why, so the history cannot be searched or reviewed. |
| final version | Weak | Vague and misleading: nothing is ever final, and it does not describe the change. |
| Add patient search by ID | Strong | Starts with a verb and states exactly what was added, in one specific sentence. |
| fix stuff | Weak | Does not say what was fixed or where, so a reviewer cannot tell the purpose or scope. |
| Prevent cancellation of completed appointments | Strong | Verb-led and states the rule enforced, so it maps directly to a business rule and a test. |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR mixes four unrelated changes (cancellation, field renames, restructuring, a new dependency) in one PR, so it is no longer one focused change and does not match the issue it claims to close.
- Responsibility and architecture concerns: Cancellation rules belong in the domain (Appointment.cancel) with the service only coordinating. Renaming patient fields and restructuring other code changes the shared domain and data store contracts that other code and tests depend on, with no justification. A new dependency adds maintenance and security risk and was not agreed.
- Testing and review concerns: The reviewer cannot tell which changes caused a test failure or regression. Existing tests may break because of the renames, which hides whether cancellation itself works. The diff is large and mixed, so review is shallow and mistakes are easy to miss. Rolling back one change means rolling back all of them.
- Changes to remove or separate, with reasons: Keep only the cancellation change and its tests in this PR. Move the field renames and the restructuring to separate PRs, each with its own issue and tests. Remove the new dependency unless a separate PR justifies it. Each change can then be reviewed, tested and reverted on its own.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: It names no criteria it checked, no tests or what they cover, no test output, no edge cases, and no reference to the issue's acceptance criteria. It does not say which files or lines were reviewed.
- Follow-up review question 1: Which acceptance criteria in the linked issue did you check, and which line of code satisfies each?
- Follow-up review question 2: Which tests did you run, how many passed, and which requirement does each test cover?
- Follow-up review question 3: What happens for an unknown ID, a blank ID, and an already cancelled or completed appointment, and is each case tested?
- Follow-up review question 4: Does the change leave state unchanged when it raises an error, and does it stay within the domain and service responsibilities?
- Follow-up review question 5: Which files and lines did you actually review, and what risks or missing tests did you find?
- Additional questions if useful: Did any existing tests change or get removed? Is any change outside the issue's scope?

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | feature/short-description, for example feature/stage6-lookups-and-cancel and feature/stage7-tests |
| Commit message convention | A short sentence starting with a verb that says what changed, for example "Add patient/practitioner lookup and appointment cancellation" |
| PR size | One focused change per PR, linked to its issue(s), touching only the files needed |
| Another-member review requirement | The group has one member, so no other member can review. With the tutor's approval the author self-reviews the Files changed diff against the issue criteria and posts that review on the PR before any AI review. Any AI review is recorded separately and labelled with the tool that produced it. |
| Merge rule | Merge only after the self-review is posted and the full test suite passes. Then update main with git pull --ff-only, re-run the full suite and record the merged SHA. |
| Significant Copilot disclosure rule | Disclose significant AI help in the PR description and the record, naming the tool accurately. GitHub Copilot use is recorded only from real sessions. |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| https://github.com/mithunnaveen1/st1-assignment-3/issues/1 | FR-02 | mithunnaveen1 | Issue #1 acceptance criteria (stored lookup, LookupError, ValueError, trimmed and case-sensitive IDs) | Closed when PR #4 merged |
| https://github.com/mithunnaveen1/st1-assignment-3/issues/2 | Supporting practitioner lookup for FR-03 | mithunnaveen1 | Issue #2 acceptance criteria (same contract for practitioners) | Closed when PR #4 merged |
| https://github.com/mithunnaveen1/st1-assignment-3/issues/3 | FR-06 and FR-07 | mithunnaveen1 | Issue #3 acceptance criteria (guarded cancellation, retained history, errors) | Closed when PR #4 merged |

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
- Significant Copilot assistance: None in the code or tests. GitHub Copilot (Free, Copilot Chat) was used afterwards for the required review comparison only, after the merge (see H and I, and stage06/copilot_stage6_output.md). Significant AI assistance from Claude (not Copilot) is disclosed: Claude drafted the three service methods, test_services.py and the issue drafts, and wrote the Claude review. The author read the code, ran the tests and wrote the self-review. The tutor said using Claude is allowed.
- Linked issue closure: PR #4 linked issues #1, #2 and #3 with Closes, so they closed on merge. (Verify on GitHub that they show as Closed.)
- Each member updated main: mithunnaveen1 (sole member) ran git switch main and git pull --ff-only; main moved from 6f7bf1e to 562d157.
- Integrated verification after merge: python -m pytest in project/ on main, 30 passed (8 supplied plus 22 new), Python 3.14.2, pytest 8.3.5, code SHA 562d15712c8de0bb587b7f3b72b6fa9022c9594b

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

Timing note: the human self-review (section G and I) was posted on PR #4 before this Copilot session. The Copilot comparison was done afterwards on the already merged diff (PR #4, merge commit 562d157), so it did not influence the merge decision. Copilot did not run the tests.

- Member and task: mithunnaveen1. Required Copilot review comparison of the Stage 6 diff (find_patient, find_practitioner, cancel_appointment) against issues #1 to #3. Tool: GitHub Copilot Free, Copilot Chat on github.com, normal chat, 10 Nov 2026 about 8:14 pm Sydney.
- Prompt/purpose and relevant issue/diff: The Stage 6 handout (Part H) review prompt with the criteria of issues #1, #2 and #3 and the three service methods from PR #4. The prompt wording was drafted with Claude; the Copilot session is real. Full prompt and unedited output: stage06/copilot_stage6_output.md.
- Summary of output: Copilot correctly summarised the diff and judged the service methods consistent with the requirements, with the cancellation rule left in Appointment.cancel(). It raised two findings. (1) Important: test coverage could not be verified because the test contents were not supplied. (2) Optional: the "22 new tests" count looks inconsistent with the range T-601 to T-628.
- Human check against actual code, requirements and tests: Checked against test_services.py and the code. Finding 1: the tests do assert the points it asked about: T-601 (lookup returns the same object with `is`), T-603 (unknown ID adds nothing), T-604 (blank ID, 3 cases), T-605 and T-606 (trimming, case sensitivity), T-621 (cancel changes status and returns the same object), T-622 (retained by ID and in list_appointments()), T-623 and T-624 (repeat and completed cancellation raise ValueError with unchanged state). Finding 2: counted the file: 18 test functions with IDs T-601 to T-606, T-611 to T-614 and T-621 to T-628. T-607 to T-610 and T-615 to T-620 are intentionally unused. Three parametrised tests (3 + 2 + 2 cases) add 4 extra cases, so 22 tests were collected. Together with the 8 supplied tests, python -m pytest gave 30 passed.
- Decision — Accept / Modify / Reject: Finding 1: Modify (partly correct). Finding 2: Modify (partly correct). Copilot's summary and requirement alignment: Accept.
- Reason: Finding 1 is a valid thing to check, but not a defect in the PR: Copilot was not given the test code, so it could not see the assertions. Its "Important" ranking therefore overstates the risk. Finding 2 is a correct observation (the range spans 28 numbers) but not an inconsistency: the gaps are deliberate and the count of 22 is correct once parametrised cases are counted. I already recorded the gaps as a note in the Claude review decision.
- Verification/evidence: Test file read and test IDs counted (18 functions, 22 collected cases). python -m pytest in project/ on main gave 30 passed after PR #4 (562d157). No code change was needed.

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: find_patient raises LookupError via the "if patient is None" check; the rule stopping a repeat cancellation is in Appointment.cancel() in domain.py and the service only calls it; test T-623 would fail if the second cancel did not raise ValueError; no risks or missing items noticed.
- Copilot noticed: The service methods match the requirements and do not bypass the domain rule or remove the appointment; no unrelated changes are visible; test coverage could not be verified from what it was given; the test count and ID range looked ambiguous.
- Overlap: Both found the three methods consistent with the issue criteria and the cancellation rule kept in the domain method. Both found no unrelated changes. The Claude review agreed as well.
- What did the human reviewer notice that Copilot did not: The human read the actual test file and could confirm the specific assertions (T-601 identity, T-622 retained and listed, T-623 unchanged state), which Copilot could not because it only had the code and a description. The human also knew the ID gaps were deliberate.
- What did Copilot identify that the human reviewer initially missed: Nothing significant. It asked for the test count and ID range to be reconciled, which the human review had not explained explicitly in the PR; the human then confirmed the count (18 functions, 22 cases) and the intentional gaps. The unused setup lines in T-627, the near-duplicate lookup methods and the ID gaps were found by the Claude review, not by Copilot.
- Unsupported or incorrect Copilot suggestion: No claim was factually incorrect. One finding (test coverage cannot be verified) was a limitation of the context given to it, and its "Important" ranking was too high. The count/range point was an accurate observation that was resolved by checking the file.
- Human judgement accepted, modified or rejected, and why: Accepted the T-627 cleanup (small and removes clutter), rejected the duplication point (an abstraction is not worth it for 3-line methods), and accepted the test ID gap as a note only. For Copilot: accepted its summary and requirement alignment, and modified both findings as described in H after checking the real tests.
- Which evidence justified merge approval: The self-review against the issue criteria, 30 passing tests (8 supplied plus 22 new), the reviewed two-file diff, and the T-627 fix. There was no independent approval, and the Copilot comparison was done after the merge, so it did not form part of the merge decision. This is a recorded gap.

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: Mithun Naveen (mithunnaveen1), sole member
- Implementation: Completed find_patient, find_practitioner and cancel_appointment in services.py with Claude's drafting; read and ran the code. PR #4, merged 562d157.
- Testing: Added test_services.py (T-601 to T-628) and ran the suite on the branch and on merged main: 30 passed.
- Review: Self-reviewed the Files changed diff against the issue criteria and posted it on PR #4 (tutor-approved solo arrangement); recorded the Claude review separately and decided which findings to accept.
- Issue refinement: Issues #1 to #3 with acceptance criteria, drafted with Claude and approved by the author.
- Design and responsibility discussion: Decided that services raise LookupError for absent records and ValueError for invalid ones, and that the cancellation rule lives in Appointment.cancel() in domain.py while the service only calls it.
- Debugging or integration: Found that the wrong test_services.py was committed ("nothing to commit"), copied the corrected file and committed 069aa91; pulled main with --ff-only and re-ran the suite.
- Documentation or team support: Not applicable (no other members). Completed this evidence record.

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

A high commit count can come from many tiny, trivial or repeated commits, formatting churn or generated files, and says nothing about their quality, difficulty or value. Strong contribution shows in the substance: issues refined, tests written, careful reviews, debugging, design decisions and how well the work meets the requirements. Evidence such as PRs, reviews and test results is better than counting commits.

## L Stage 6 formative questions

1. What is version control?

Version control records every change to a project over time, who made it and why, so the team can compare versions, undo mistakes and work together without overwriting each other's work. Git is an example.

2. Why is a feature branch useful?

A feature branch lets one change be developed and tested in isolation from main, so unfinished or broken work does not affect the stable code. It also gives a clear unit to review through a pull request, and is easy to discard or revert.

3. What makes a commit a good engineering commit?

A good commit is small and focused on one change, builds and passes the tests, and has a clear message starting with a verb that says what changed and why, so it can be reviewed and reverted on its own.

4. What is a pull request?

A pull request proposes merging the changes from one branch into another (usually main). It shows the diff, links the issue, and is where review, discussion and tests happen before the merge.

5. What is the purpose of code review?

Code review checks that a change meets the requirements, is correct, readable and tested, stays in scope, and is safe to merge. It catches defects early and shares understanding of the code.

6. What does a Git diff show?

A Git diff shows the exact lines added, removed or changed between two versions, such as a branch against main or a commit against its parent.

7. What is a Definition of Done?

A Definition of Done is the agreed checklist a piece of work must meet before it counts as finished, for example criteria met, tests written and passing, reviewed, scope respected, and documentation updated.

8. What is the appropriate role of GitHub Copilot in pull-request review?

Copilot can be an extra reviewer that raises possible issues and questions, but it does not replace the human. Its comments are checked against the issue criteria and tests, weak or unsupported comments are challenged, and the author stays responsible for the decision to merge.

9. Why should individual contribution not be judged only by commit count?

Commit count measures activity, not value. Commits vary in size and quality and can be inflated, so contribution should be judged on the work itself: code, tests, reviews, issue refinement, debugging and design, backed by evidence.

10. What is the Stage 6 engineering rule?

Review the change against the issue criteria and the tests, keep each PR focused on one change, and do not merge on trust. Do not accept an AI review as evidence unless it is specific and checked, and record honestly what is done and what is still pending.

## M Completion and handover

- Starting SHA: 6f7bf1e
- Final Stage 6 code SHA: 069aa91162edc30b065913070cd4584473a918e9 (PR branch head); merged main SHA 562d15712c8de0bb587b7f3b72b6fa9022c9594b
- Test command: python -m pytest
- Working directory: project/
- Observed result: 30 passed on merged main (562d157), run in project/ with python -m pytest, Python 3.14.2, pytest 8.3.5
- PR and another-member reviewer: https://github.com/mithunnaveen1/st1-assignment-3/pull/4 ; no other member (solo group, self-review approved by tutor)
- Unresolved issue or none: (1) GitHub Copilot comparison done after the merge (H and I), so it was not part of the merge decision. (2) Sections B to L were drafted with Claude and reviewed by the student (disclosed). (3) No independent reviewer exists (solo group, tutor-approved self-review).
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: Not yet decided. A later evidence-only commit will add this record; the tested code SHA stays 562d15712c8de0bb587b7f3b72b6fa9022c9594b (merged main).

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

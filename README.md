# dialysis-dashboard

A full-stack application designed to assist dialysis centers in tracking patient treatment sessions and quickly identifying potentially unsafe situations through real-time anomaly detection. The goal is to provide a **minimal but realistic** intake API and UI to support nurses efficiently during their shifts.

## Scenario

Dialysis centers need to meticulously track each patient's treatment sessions, including pre/post weight, vitals, duration, and machine events. A critical requirement is the ability to rapidly surface potential risks, such as excessive interdialytic weight gain or elevated post-dialysis blood pressure. This project aims to deliver a minimal yet realistic intake API and UI to support nurses efficiently during their shifts.

## Core Requirements

### Backend (FastAPI or Express)

-   Register a patient with **dry weight** and basic demographics.
-   Record a dialysis session event: timestamps, pre/post weight, key vitals, machine ID, nurse notes.
-   Fetch **"today's schedule"** and sessions for a given unit (in-memory schedule or simple collection is acceptable).

### Data Layer (MongoDB)

-   Schema design of your choice (document shape, indexes, embedding vs. referencing).

### Anomaly Detection (Backend)

Implement basic per-session anomaly detection. Examples include:

| Anomaly                           | Expectation                                                              |
| :-------------------------------- | :----------------------------------------------------------------------- |
| Excess interdialytic weight gain  | You define the threshold and justify it in the `Clinical Assumptions & Thresholds` section. |
| High post-dialysis systolic BP    | You define the threshold and justify it in the `Clinical Assumptions & Thresholds` section. |
| Abnormal session duration         | Short or long relative to a configurable target.                         |

Anomalies must be surfaced in the "today's schedule" API response so the UI can highlight them.

### Frontend (React / TypeScript)

-   List all patients scheduled for today with status: *not started / in progress / completed*.
-   Display key fields per session (pre/post weight, BP, duration) and **clearly mark anomalies**.
-   Nurse actions:
    -   Add a session for a patient.
    -   Edit session notes.
    -   Filter to **"only show patients with anomalies."**
-   Handle **loading, empty, and error states** for all API calls, including partial failures.

## Intentional Ambiguity

What counts as "clinically significant" weight gain, high BP, or abnormal duration is **not specified** in the initial problem. As part of this project, explicit assumptions will be made, encoded in configuration (no magic numbers scattered in code), and thoroughly documented in the `Clinical Assumptions & Thresholds` section of this README.

## Deliverables

-   Running service (API + UI) plus seed script or instructions to populate example patients.
-   API documentation (OpenAPI/Swagger or markdown) and a short architecture overview (one page).
-   Tests for:
    -   Core business logic (anomaly detection).
    -   One API route.
    -   One UI component or view.

## Sections:
-   **Setup:** Instructions for setting up and running the project locally.
-   **Architecture:** Overview of the system design, components, and their interactions.
-   **Data Model:** Detailed MongoDB schema, including document shapes, indexing strategies, and embedding vs. referencing decisions.
-   **Clinical Assumptions & Thresholds:** Explicit assumptions made regarding clinical significance for anomaly detection, along with their justifications and configurable thresholds.
-   **Trade-offs:** Documented design decisions and their rationale.
-   **Failure Handling:** Strategies for error handling, logging, and system resilience.
-   **Tests:** Overview of the testing strategy and coverage.
-   **Future Improvements:** A roadmap for potential enhancements and new features.
-   **AI Usage:** (Optional) Documentation for any potential future AI/ML components.
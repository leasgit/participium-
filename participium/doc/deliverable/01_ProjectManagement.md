# Product Breakdown Structure (PBS)

| ID | Deliverable | Type  | Notes |
|:---|:------------|:--------------------------------------------------|:------|
| S1 | Map Visualization |  Software          |  Provides an interactive map interface for users on web client     |
| S2 | Report and statistics tables/dashboards | Software          |   Provides users with statistics and data filtering options to support platform transparency for Web-Client (displaying statistics, etc)    |
| S3 | Notifications & Comunications in-platform |  Software          |  In-platform notifications and messaging  to agents  to support user communication     |
| S4 | Account management service (Registration and Authentication) |  Software          |  Handles user account creation, authentication and profile settings     |
| S5 | Report management service |  Software          |  Enables users to report, to view and to filter through urban issues     |
| S6 | Social service (Notifications and Comunication service) |  Software          |  Back-end service for managing notifications and user communications (on  and off the platform, e.g. mail notifications)      |
| S7 | Public consultation service |  Software          |  Back-end service for collecting user feedback, reviews and etc     |
| S8 | Statistics service |  Software          | Back-end service for generating, managing platform statistics      |
| D1 | Requirements document |  Documentation          |       |
| D2 | Architecture and design document |  Documentation          |       |
| D3 | Test documentation |  Documentation          |       |
| D4 | User manual (one for each different type of user) |  Documentation          | Documents containing informations on how to use the application. One for Visitors and Registered citizens, one for Municipal officers and one for System administrators      |
| D5 | API documentation |  Documentation          |       |
| D6 | Governance and Contribution deliverables |  Documentation          | Document containing informations about how to contribute to the project, as it is open source     |
| D7 | Legal and Compliance documentation |  Documentation          | Document containing informations to clarify the "open" part of the project. Which part cant be contributed, and which informations are accessible by all the contributors     |
| I1 | Cloud/Server for deployment |  Infrastructure          | Defines the computing environment where the application is based and executed      |
| I2 | Storage (Geo-location) |  Infrastructure          | Stores geographical location data related to reports such as coordinates or location information |
| I3 | Relational DB (Account Report content & status) |  Infrastructure          | Uses a relational database to store structured information such as user accounts, report details, and report status, etc... |
| I4 | Media Storage (photoes in the reports) |  Infrastructure          |       Stores images and other media file inputs that are uploaded in user reports |
| I5 | Backup and disaster recovery |  Infrastructure          | Ensures system reliability by backing up data and monitoring system performance |
| I6 | Email management |  Infrastructure          | Manages automated emails such as notifications, account activity, and communication with users

The PBS was organized into three main deliverables to cover the scope of the Participum platform; software, documentation, and infrastructure. The software part was split into front-end and back-end features so that each major functionality of the system is treated as a seperate deliverable. Documentation and infrastructure were also included because it is not enough to only develop the application, we must also deploy and maintain it by providing proper documentation for users, administrators, and future contributors. 

---
# Work Breakdown Structure (WBS)

### WBS with traceability to PBS
| ID  | Work package | Traced PBS outputs (IDs) |
|:----|:-------------|:--------------------------|
| 1 | Requirement |    D1, D6, D7          |
| 2 | Desgin and Architecture | D2, I1, I6|
| 3 | Development | I2, I3, I4, I5, S1, S2, S3, S4, S5, S6, S7, S8 |
| 4 | Verification and Validation| D3 |
| 5 | Development and Go-live| D4, D5 |

The WBS was organized into five main work packages representing major phases of the project: requirements, desgin, development, verification, and deployment. Each work package corresponds to and groups specific PBS deliverables, ensuring consistency between project activities and outputs. In this structure we reflect a phased development approach, where requirements and design and completed first, followed by implementation, testing, and deployment.

---

# Gantt, dependencies, and critical path

M1: License and legal document confirmation
M2: Backend MVP released
M3: Beta testing done with the users
M4: Application deployed

## Activity table
| ID | Activity | Duration | Dependencies | Start | End | Critical | Milestone |
|:---|:---------|:---------|:-------------|:------|:----|:------|:---------|
| T1.1 |Definition of Funcitonal Requirements|3|-|1|3|yes|no|
| T1.2 |Definition of Non-Funcitonal Requirements|3|-|1|3|yes|no|
| T1.3 |Definition of Requirement Document| 4    |   T1.1, T1.2  |  4   |   7   |   yes |   no  |
| T1.4 |Definition of Legal constraints Document|7|   T1.1, T1.2  |4|10|yes|yes - M1|
| T2.1 |Architecture and design document（Report)|2|   T1.1, T1.2  |11|12|yes|no|
| T2.2 |Design the user database (Account, Report content & status and the storage (geo-location, media)|2|   T1.1, T1.2  |11|12|yes|no|
| T2.3 |Definition of the Email  management and system|2|   T1.1, T1.2  |11|12|yes|no|
| T3.1 |Development of APIs and back-end skeleton|6|T2.1, T2.2, T2.3|13|18|yes|yes - M2|
| T3.2 |Development of the backend|18|T3.1|19|36|no|no|
| T3.3 |Development of Web app frontend|22|T3.1|19|40|yes|no|
| T4.1 |Definition of Test documentation|2|T3.1, T3.2, T3.3|41|42|yes|no|
| T4.2 |Beta testing with the users|1|T4.1|43|43|yes|yes - M3|
| T5.1 |Deployment of the system|1|T4.2|44|44|yes|yes - M4|
| T5.2 |Monitoring and bug fixing |4|T5.1|45|48|yes|no|

The Gantt chart was constructed based on the WBS, where eacg scheduled activity corresponds to a work package, and each work package corresponds to certain deliverables in tbe PBS. This ensures traceability from project deliverables to activities and schedule. The timeline follows a phased development approach, with some parallel activities during the development phase to optimize total project duration. 


![Diagram](doc/additional_docs/image_123.png)

## Critical path
T1.1|T1.2 -> T1.3|T1.4 -> T2.1|T2.2 |T2.3 -> T3.1 -> T3.2|T3.3 -> T4.1 -> T4.2 -> T5.1 -> T5.2


---

# Risk Management

**Scales and thresholds**
- **Probability (P)**: 1 (rare) … 5 (almost certain)
- **Impact (I)**: 1 (minor) … 5 (critical)
- **Exposure**: `P × I` (range 1–25)

Risk level thresholds (by exposure):
- **Low**: 1–5
- **Medium**: 6–10
- **High**: 11–16
- **Very High**: >16



## Risks table
| ID | Risk | Category | P | I | P×I | Level | Mitigation / Response strategy |
|:---|:-----|:---------|--:|--:|----:|:------|:-------------------------------|
| R1 | Data privacy | Security | 2   |  5 |  10   |       Medium|   Use strong encryption and double-check that "Anonymous" mode works |
| R2 | storage limit | Infrastructure | 2   |  3 |  6   |       Medium|   set a max file size and limit uploads to 3 photos per report |
| R3 | Map API failure | Technical | 2   |  4 |  8   |       Medium|   use a free, reliable map provider  |
| R4 | Fake reports | Operational | 5   |  3 |  15   |       High|   require email verification for registration so registered citizens can submit report  |
| R5 | Low user engagement | Operational | 4   |  3 |  12   |       High |   keep the UI user-friendly and simple  |
| R6 | Running out of time | Management | 3  |  4 |  12   |       High|   focus on main features before adding extras  |

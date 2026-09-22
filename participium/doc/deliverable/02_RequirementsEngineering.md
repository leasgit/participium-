# 1) Stakeholders

| ID     | Stakeholder name | Description | Role | Main concerns | Goals/Expected value | Influence/Priority |
|:-------|:-----------------|:------------|:-----|:--------------|:---------------------|:-------------------|
| STK-01 | Visitor | Person who access the public portal to consult the situation about the issues reported | User | transparency, usability, accessibility | Consult urban issues and check if a specific problem has already been reported | Medium |
| STK-02 | Registered Citizen | Person who access the public portal to submit reports about issues in the city, track the evolution of them and interact with the municipality | User | privacy, usability, communication, efficiency |Easily send geolocated reports complete with photos, monitor progress, and interact with municipal offices. | High |
| STK-03 | Municipal Officier | Person who works in a municipal office and who access the platform to review incoming submissions and manage accepted reports | User | workload | Efficiency in validate the reports and communicate them to the competent offices and services | High |
| STK-04 | System Administrator | Person who manage the configuration of the platform and can access to extended analytics | User | usability, security, scalability | Ability to ensure the correct technical functioning of the platform, configure its parameters and view advanced statistics | High |
| STK-05 | Politician | A senior executive in the municipality of Turin, interested in the platform's performance in order to gain consensus | Political | efficiency | Demonstrate concrete results to citizens and optimize the use of resources | Low |
| STK-06 | Agency/Service | External company interested in resolving the issues reported on the platform | Tecnical | workload, clarity | Receive specific assignments related to the urban condition | Medium |
---

# 2) Context Diagram
![alt text](<context diagram.jpeg>)
---

# 3) Interfaces

| ID    | Interface | Actor       | Physical interface | Logical interface |
|:------|:----------|:------------|:-------------------|:------------------|
| IF-01 |Public access interface|Viewer|Web Client/Smartphone|WEB/Mobile GUI|
| IF-02 |Report submission interface|Reporter|Web Client/Smartphone|WEB/Mobile GUI|
| IF-03 |Administration interface|System Administrator|Web Client/workstation with  internet connection|WEB GUI|
| IF-04 |Report management interface|Municipal Officer|Web Client/workstation with  internet connection|WEB GUI|
| IF-05 |Statistics Interface|Visitor, Registered  Citizen, Politician|Web Client/Smartphone|WEB/Mobile GUI|
| IF-06 |Authentication interface|Authentication system|Internet connection|Authentication APIs|
| IF-07 |Notification interface|Notification service|Internet  connection|Notification APIs|
| IF-08 |Email verification|Email service|Internet connection|Email APIs|
| IF-09 |Map interface|OpenStreetMap service|Internet connection|OpenStreetMap API|
---

# 4) Personas

| ID     | Name | Role | Background / Context | Goals | Constraints | Devices / Usage setting | Accessibility / Additional needs |
|:-------|:-----|:-----|:---------------------|:------|:------------|:------------------------|:---------------------------------|
| PER-01 |Travis Scott|Visitor|Travis is a resident of Turin who  wants  to stay in touch about the issues in his neighborhood without  necessarily creasting an account.|View issues  on the map, check the problem status and  whether certain issues have already been solved|Doesn't want to create an account and impatient|Smartphone, has no interest to spend time and effort using laptop|Interface should be simple,  responsive and easy to navigate.|
| PER-02 |Bruno Centrella|Registered Citizen|Bruno is a  student at  PoliTo, living in Turin. He  reports urban issues like broken streetlights whenever he can|Submit  reports, upload photos, pin-point the geolocation on the map, track report progress|No constraints|Mainly smartphone|Mobile-friendly design, clear forms for report submission, easy map interaction|
| PER-03 |Alain Rizzi|Municipal Officer|Alan Rizzi is a Municipal Officer, working in a office that manage the issues reported by the citizens in the city of Tourin. | Review the issues reported by the citizens, assign them to the right Agency/Service and provide updates the user who reported the issue  | Want to have a clear interface to the platform | Laptop or Desktop PC | No additional needs |
| PER-04 |Luca Martinelli|System Administrator| Luca Martinelli is a System Administrator encharged to manage the configuration aspects of the platform and access extended analytics about the users and the reported issues | Change system configuration to garantee a good user experience to users who access the platform. |needs acccess to technical tools|PC or laptop|Needs advanced admin interface, system logs, and analytics dashboard|
| PER-05 |Steve Harrington|Politician|Steve is a politician   interested in the overall effectiveness of the platform  and public perception|View statistics, understand trends, report to  authorities|Limited time, not interested in operational details|Laptop|Clear charts and  summaries, easy access to statistics|
| PER-06 |Elton John|Registered Citizen|Elton is a retired citizen of Turin who wants to report architectural barriers, cracked sidewalks, or street lighting problems in his area.|Submit reports and track their progress|Not very familiar with technology, may have difficulty seeing|Tablet or smartphone|Large buttons, easy-to-read fonts, simple navigations and instructions.|
| PER-07 |Daenerys Targaryen|Municipal field worker|Daenerys works for the municipal maintenance team, she recieves assigned tasks related to reports and updates their status afterwards.|View assigned reports, update report status.|Needs quick access to information|Smartphone|mobile interface, map navigation and quick status update buttons|
| PER-08 |Andrea bocelli|Registered citizen|Andrea is a blind resident that relies on assistive technologies to use web applications. He wants to report issues such as architectural barriers and unsafe sidewalks.|Submit reports, track progress and recieve updates about issues in the city.|Cannot use visual map interfaces, relies on screen readers and keyboard navigation|Laptop with screen reader or smartphone with voice control|Screen reader compatibility, keyboard navigation, voice support, text alternatives for maps and images.|
---

# 5) User Stories

| ID    | Persona/Role | User story (As a… I want… so that…) |
|:------|:-------------|:------------------------------------|
| US-01 |  PER-02            |  As a registered citizen I want to select a position on OpenStreetMap-based map of Turin so that I can report the issues                                   |
| US-02 |   PER-02          |     As a registered citizen I want to upload one or more photos(maximum 3) to my report so that there is visual evidence of the problem                               |
| US-03 |    PER-02          |   As a registered citizen I want to mark my report as anonymous for public view so that i can protect my personal privacy                                  |
| US-04 |   PER-01           |  As a visitor I want to  view public statistics based on category and trends over time,aggregated by day,week or month so that i can find information about the area i want                                    |
| US-05 |     PER-03         |    As a municipal officer I want to review incoming submissions and manage accepted reports(update the status of a report) so that citizens be aware of the progress                                |
| US-06 |   PER-04           |   As an Administrator I want to have an access to private statistics(e.g, number of reports by status/type/reporter) so that i can be aware of the efficiency of the responses and also some important information that can help fix problems more easier                              |
| US-07 | PER-02 | As a Registered citizen, I want to register and authenticate to the platform and recive an email for Verification and confirmation of the creation of the account
| US-08 | PER-02 | As a Registered citizen, I want to be able to check the status of my reported issue (Pending, Assigned, In Progress, etc.)
| US-09 | PER-02 | As a Registered citizen, I want to be able to directly communicate with Municipal Officers through direct messaging
| US-10 | PER-03 | As a Municipal Officer, I want to be able to direct message Registered citizens to ask for clarifications about a reported issue or provide updates
| US-11 | PER-02 | As a Registered citizen, I want to be able to log out from the platform
| US-12 | PER-06 | As an elderly citizen I want the platform to use large text and easy navigations so that I can use the platform easily.
| US-13 | PER-08 | As a blind user, I want the platform to be compatible with screen readers so that i can access all features
| US-14 | PER-08 | As a blind user, I want to enter a location using speech-to-text address instead of only a map so that I can submit a report
| US-15 | PER-07 | As a municipal worker, I want to update the report status after completing the task so that the system reflects progress
---

# 6) Functional Requirements (FR)

| ID    | Requirement statement (The system shall…) | Priority | User story ID | Notes |
|:------|:------------------------------------------|:---------|:--------------|:------|
| FR-1 |   user registeration and authentication                                       | critical     | 
| FR-1.1 |   the system shall allow users to creat account with first name and last name                                        | critical     | US-07
| FR-1.2 |   the system shall send an email for Verification to confirm the account                                        | critical     | US-07         |       |              |       |
| FR-1.3 |  user log in                                        |    critical      |  US-01,US-02  
| FR-1.4 |   user log out                                        | critical     |     US-11      |       |
| FR-2 |  report submissions                                         |    critical      |               |       |
| FR-2.1 |   the system shall provide geo-located items so The citizen selects a position on an OpenStreetMap-based map which is stored as latitude/longitude                                        |    critical      |   US-01            |       |
| FR-2.2 |   The system shall allow users to attach a maximum of 3 photos to each report.                                        |      critical    | US-02              |       |
| FR-2.3 |  the system shall provide an option which reporters can report anonymously                                         |    important      |  US-03             | identity hidden from publib views      |   |               |       |
| FR-3 |    monitoring                                     |    critical      |               |       |
| FR-3.1 |  The system shall display reports in a structured list supporting filtering by category, status, and time period                                         |    important      |      US-04         |       |
| FR-3.2 |   the system shall provide a page with details(e.g, description,category,status updates)                                      | critical     |   US-04,US-05            |       |
| FR-4 |   The system shall send in-platform notifications to reporters and followers when a status changes updates                                        | important     |            |    for all status updates   |
| FR-5 |   The system shall display public statistics to all users                                       | critical     | US-04 | accessible also to unregistered users
| FR-6 |   The system shall display private analytics (by status/reporter/type) only to administrators                                       | important     | US-06






---

# 7) Non-Functional Requirements (NFR)

| ID     | Category | Requirement statement | Metric / Target | Verification                           | Priority | Notes |
|:-------|:---------|:----------------------|:----------------|:---------------------------------------|:---------|:------|
| NFR1 | Reliability | the system should support multiple kinds of users | the system shall support 1000 users to access the portal web in same time  | test | critical |
| NFR2 | Portability | The system should be compatible with the major browsers (chrome, firefox, edge) | using different browsers open the website to check if there is an incompatible condition | test | important | it should also working and compatible among different system, opening the website in android/IOS platform |
| NFR3 | Reliability+Security | The system shall provide an encryption on users data(profile, identity information, email address, password) | all the sensitive segment should be encrypted in database (email address, IP address, password) | inspection | critical |
| NFR4 |  Usability | an User/visitor is able to correctly learn how to use the website | the user can update or fill their basic information within 5mins | analysis  |
| NFR5 | Efficiency | The report should appear in the map immediately when it was created | the report should appear in the city map within 2s after it was created | test | important  |
| NFR6 | Usability | an User/Visitor can understand the report details page | The user can easily check the report details page in 5mins | inspection | important |
| NFR7 | Reliability | The website should keep stable | The system must provide an up-time period of 99% over the year even in 1000 concurrent accessing | test | critical |
| NFR8 | Maintainability | The user allows to submit a bug on the website | The bug can be fixed in 1 week | inspection | important/critical | the bug priority depends on whether this bug affects to the performance of website |
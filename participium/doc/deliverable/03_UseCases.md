# 1) Use Case Diagram

Attach your use case diagram as an image under `../data/img/` and link it here:

- [UseCaseDiagram](https://git-softeng.polito.it/se2025-26/group-03/participium/-/blob/3a9fe81284d56a335806e1fff3867b11caca2a84/data/img/UseCaseDiagram.svg)
- [JSON source file](https://git-softeng.polito.it/se2025-26/group-03/participium/-/blob/3a9fe81284d56a335806e1fff3867b11caca2a84/data/UseCaseDiagram.json)

Also, make sure to include the JSON source file downloaded from the UML Modeler used to draw the diagram in the `../data/` folder.

# 2) Use Case Narratives

Add one narrative for each use case shown in the diagram.

| Use Case                | Create account|
|:------------------------|:----------------------------|
| ID                      | UC1|
| Scope                   | Participium|
| Level                   | User Goal|
| Intention in Context    | Allow a Visitor user to become a Registered Citizen and be able to report issues and interact with the municipality of Turin|
| Primary actor           | Visitor|
| Supporting actors       | Verification & Authentication system (External System)|
| Stakeholders' interests | Visitor: wants to report urban issues and monitor their solving. Municipal Officer: wants issues reports to be submitted only by registered citizen|
| Precondition            | The user accessed the public portal and he is still not registered|
| Minimum guarantees      | If the registration fails, personal data of the user are not memorized and any incomplete account is created|
| Success guarantees      | A new Registered Citizen account is created|
| Trigger                 | The Visitor user select the command for the creation of a new account|
| Main success scenario   | 1. The system shows the sign up page and asks for basic identity informations (username, first name, last name) and the email. <br>2. The user inserts personal data, the email and optionally a profile picture. <br>3. The system sends a verification link to the email address provided by the user. <br>4. The user confirms his identity by clicking on the Verification link received by email. <br>5. The system confirm the creation of the new account and display the login page <br>**The use case terminates with success**|
| Extensions              | 2a.1 The user cancels the registration. <br>2a.2 The system does not register the new account. <br>**Use case fails**. <br><br>2b.1 The user inserts a username or an email already registered. <br>2b.2 The system shows an error and the use case restarts from step 1. <br><br>4a.1 The user do not click in time on the verification link, which expires. <br>4a.2 The system allow the sending of a new verification link and the use case restarts from step 3|

| Use Case                | Access Public Portal Website |
|:------------------------|:----------------------------|
| ID                      | UC2 |
| Scope                   | Participium |
| Level                   | User-Goal |
| Intention in Context    | Allow a Visitor user to Access Participium Public Website to check issues reported by other citizens |
| Primary actor           | Visitor |
| Supporting actors       | - |
| Stakeholders' interests | Visitor: wants to know about urban issues in Turin |
| Precondition            | - |
| Minimum guarantees      | - |
| Success guarantees      | - |
| Trigger                 | - |
| Main success scenario   | 1. The user search the web page of the Participium Platform. <br>2. The system shows the main page with the interactive map of the city of Turin, with the issues repoted by all the users. <br>**The use case terminates with success** |
| Extensions              | - |

| Use Case                | Loggin |
|:------------------------|:----------------------------|
| ID                      | UC3 |
| Scope                   | Participium |
| Level                   | User-Goal |
| Intention in Context    | Allow Visitor user to Log in the Participium Platform |
| Primary actor           | Visitor |
| Supporting actors       | - |
| Stakeholders' interests | Visitor: wants to log in with his personal account to be able to report an issue or check evolving on already reported ones |
| Precondition            | The user accessed the public portal and he is salready registered |
| Minimum guarantees      | - |
| Success guarantees      | User is logged in with his personal account |
| Trigger                 | The Visitor user select the command for the log in |
| Main success scenario   | 1. The system shows the log in page and asks for username and password. <br>2. The user type his username and password. <br>3. The system shows the user personal page with his reported issues. **The use case terminates with success** |
| Extensions              | 2a.1 The user type a non existing username. <br>2a.1 The system says that the typed username is non existent and the use case restarts from step 1. <br><br>2b.1 The user type a wrong password. <br>2b.2 The system says that the typed password is wrong and the use case restarts from step 1. |
  
| Use Case | Submit Report |
|:------------------------|:----------------------------|
| ID                      |UC4|
| Scope                   |Participium|
| Level                   |User-Goal                    |
| Intention in Context    |Submit an urban issue for officials to handle the problem (?)|
| Primary actor           |Registered Citizen|
| Supporting actors       |-|
| Stakeholders' interests | Miniciple: the problem in a report is physically existing in the city, which means that it is not a fake report|
| Precondition            |Successfully login a citizen account|
| Minimum guarantees      |the unfinished report will be save automatically|
| Success guarantees      |The report is uploaded and is ready to be viewed in the map|
| Trigger                 |   -                          |
| Main success scenario   | 1. Registered Citizen comes accross an urban issue. <br>2. User pin-points the geolocation of the issue. <br>3. Citizen chooses a category selected from a predefined set, and a title and a textual description,<br>4. User uploads photos among 1 to 3. <br>5. Citizen can select the report published as an Anonymity Option<br>6. Citizen can choose whether follows one or many of any report, so that Citizen will be authenticated as a follower to this/those report(s)<br>7. the municipal will check the report if it is valid<br>8. the system updates the report in the map and table view <br>**The use case terminates with success** |
| Extensions              | 2a.1 The citizen cancels the report<br>2a.2 The use case ends with failure<br><br>4a.1 The photos are not valided<br>4a.2 The system requires re-upload the photos<br><br>7a.1 the status of the report will be marked as Pending Approval<br>7a.2 if the report is rejected, the status of the report will be marked as Rejected<br>7a.3 if the report is assigned, the status of the report will be marked as Assigned<br>7a.4 whatever the status changed, the followed citizen will receive a notification which modified status |

| Use Case                | Edit Profile |
|:------------------------|:----------------------------|
| ID                      | UC5 |
| Scope                   | Participium |
| Level                   | User-Goal |
| Intention in Context    | Allow a Registered Citizen to update his personal informations and the communications preferences |
| Primary actor           | Registered Citizen |
| Supporting actors       | - |
| Stakeholders' interests | Registered Citizen: wants to personalize his profile (profile picture, etc.) and manage how to recieve notifications about Reports |
| Precondition            | The user is logged into its account |
| Minimum guarantees      | In case of error or cancellation, user's profile informations remain unchanged |
| Success guarantees      | User profile informations and preferences are updated in the system |
| Trigger                 | The Registered Citizen select the option to modify its profile in the profile page |
| Main success scenario   | 1. The system displays the current profile information (username, first name, last name, email, image) and active preferences. <br>2. The user edits the desired information (e.g., first name, last name, or adding/changing a profile photo). <br>3. The user updates notification preferences (enabling/disabling emails in addition to in-app notifications). <br>4. The user confirms the changes by saving the profile. <br>5. The system validates the data and confirms the update. <br>**The use case terminates with success** |
| Extensions              | 2a.1 The user uploads a photo in an unsupported format.<br>2a.2 The system displays an error and requires a new upload.<br><br>4a.1 The user discards changes before saving.<br>4a.2 The system restores the original data display. <br>**Use case fails** |

| Use Case                | View State |
|:------------------------|:----------------------------|
| ID                      | UC6 |
| Scope                   | Participium |
| Level                   | User-Goal |
| Intention in Context    | Allow a Registered Citizen to visualize the current status of a Reported issue (Work in Progress, Solved, etc.) |
| Primary actor           | Registered Citizen |
| Supporting actors       | - |
| Stakeholders' interests | Registered Citizen: wants to know the status of its Reported issues or one he is intrested in |
| Precondition            | The user is logged into its account |
| Minimum guarantees      | The system shows the most recent status saved in the system |
| Success guarantees      | The user correctly visualize the current status of the selected Report |
| Trigger                 | The Registerd Citizen select a Report from its personal area, from the map or from the search table to show its details |
| Main success scenario   | 1. The system displays a list of reports.<br>2. The user selects a specific report.<br>3. The system retrieves updated information from the database.<br>4. The system displays the report detail page, including the current status (e.g., Pending Approval, Assigned, In Progress, Suspended, Rejected, Resolved).<br>**The use case terminates with success**  |
| Extensions              | 3a.1 The selected report is no longer available or has been removed.<br>3a.2 The system displays an error message and the use case fails.<br>**Use case fails** |

| Use Case                | Track an Update |
|:------------------------|:----------------------------|
| ID                      | UC7 |
| Scope                   | Participium |
| Level                   | User-Goal |
| Intention in Context    | Allow a Registered Citizen to follow a Report to get automatic notifications about its evolution |
| Primary actor           | Registered Citizen |
| Supporting actors       | Notification Service (External System) |
| Stakeholders' interests | Registered Citizen: wants to be updated about progresses in solving an urban issue, without needing to manually consult the platform.<br>Politician: wants to improve citizen consensus through a clear communication |
| Precondition            | The used is logged into its personal account |
| Minimum guarantees      | The system keep the association between the user and the tracked Report. No notifications are sent if the Report status does not change |
| Success guarantees      | The user get notified every time that the followed Report change its status |
| Trigger                 | The user select the option to track ("Follow") a specific Report |
| Main success scenario   | 1. The citizen views a report via the map or table.<br>2. The citizen opens the report detail page.<br>3. The citizen selects the option to follow the report.<br>4. The system registers the citizen as a "follower" of the report.<br>5. When the report status changes (e.g., from "Assigned" to "In Progress"), the system generates an in-app notification for the citizen.<br>**The use case terminates with success** |
| Extensions              | 3a.1 The citizen is already a follower of the report.<br>3a.2 The system offers the option to stop tracking the report ("unfollow").<br><br>5a.1 The citizen has enabled email notifications in their profile (UC5).<br>5a.2 The system sends an update email in addition to the notification on the platform. |

| Use Case                | Report Status |
|:------------------------|:----------------------------|
| ID                      | UC8 |
| Scope                   | Participium |
| Level                   | User-Goal |
| Intention in Context    | Allow a Municipal Officer to update the status of a Report |
| Primary actor           | Municipal Officer |
| Supporting actors       | - |
| Stakeholders' interests | Municipal Officer: wants to organize and manage upcoming Reports.<br>Registered Citizen: wants transparency on the handling of the reported Issue |
| Precondition            | The Municipal Officer is logged into its account and selected a Report to review |
| Minimum guarantees      | If the operation is interrupted, the state of the Report is not changed |
| Success guarantees      | The status of the Report is updated |
| Trigger                 | The Municipal Officer select the option to change the status of a specific Report |
| Main success scenario   | 1. The Municipal Officer views the details of a pending report. <br>2. The Municipal Officer selects a new status from the predefined set (Pending Approval, Assigned, In Progress, Suspended, Resolved, Rejected). <br>3. The system updates the status in the database and records the change. <br>4. The system automatically generates in-app notifications (and optionally emails) for the original reporter and all followers (UC7).<br>**The use case terminates with success** |
| Extensions              | 2a.1 Lo stato selezionato è "Rejected". <br>2a.2 Il sistema richiede l'inserimento obbligatorio di una motivazione esplicita per il rifiuto. <br><br>2b.1 Lo stato selezionato è "Assigned". <br>2b.2 L'ufficiale specifica l'ufficio tecnico competente incaricato dell'intervento. |

| Use Case                | Ping Point the Location |
|:------------------------|:----------------------------|
| ID                      | UC9 |
| Scope                   | Participium |
| Level                   | Sub-function |
| Intention in Context    | Allow user to pin point with precision the Geographical location of the Issue on the interactive map |
| Primary actor           | Registered Citizen |
| Supporting actors       | Map Interface (External System) |
| Stakeholders' interests | Registered Citizen: wants to easily point the location of the reported Issue<br>Municipal Officer: needs precise GPS coordinates to locate the intervention |
| Precondition            | The user is in the creation phase of a Report (UC4) |
| Minimum guarantees      | If the operation is interrupted, the coordinates are not saved |
| Success guarantees      | The system acquire the precise coordinates of the selected point on the map |
| Trigger                 | The report submission process (UC4) asks the geolocation of the issue |
| Main success scenario   | 1. The system loads and displays a map of Turin based on OpenStreetMap.<br>2. The user interacts with the map (zoom/pan) to locate the exact problem area.<br>3. The user clicks or taps the specific point on the map to place the "pin."<br>4. The system displays a visual indicator at the selected location.<br>5. The system extracts the latitude and longitude coordinates of the point.<br>6. The system returns the coordinates to the reporting module.<br>**The use case terminates with success** |
| Extensions              | - |

| Use Case                | Report Displayment |
|:------------------------|:----------------------------|
| ID                      | UC10 |
| Scope                   | Participium |
| Level                   | User-Goal |
| Intention in Context    | Allow the user to visualize the Issues Reported in the system through an interactive map or a table view with filters |
| Primary actor           | Municipal Officer |
| Supporting actors       | Map Interface (External System) |
| Stakeholders' interests | Municipal Officer: needs a panoramical view of the Reported Issues to manage their resolution |
| Precondition            | The user is logged into its personal account |
| Minimum guarantees      | The system correctly load data from the database and visualize markers on the map |
| Success guarantees      | The user gets a panoramical and optionally filtered view of the Reported Issues |
| Trigger                 | The user access the Manage Reports sections in the platform |
| Main success scenario   | 1. The system loads geolocated reports and displays them on the Turin map. <br> 2. The user can switch between Map View and Table View.<br>3. The user applies specific filters by category, report status, or time period.<br>4. The system updates the view, showing only reports that meet the selected criteria.<br>5. The user selects a specific report for more information.<br>6. The system opens the report detail page (UC15). <br>**The use case terminates with success** |
| Extensions              | 3a.1 The user sorts the table by date or specific field. <br> 3a.2 The system reorganizes the list based on the requested sort order.<br><br>4a.1 No reports match the selected filters.<br>4a.2 The system displays an empty map/table with an informational message. |

| Use Case                | Access Report |
|:------------------------|:----------------------------|
| ID                      | UC11 |
| Scope                   | Participium |
| Level                   | User-Goal |
| Intention in Context    | Allow the user to consult Reported Issues selecting them from the map or using filters in the Table view |
| Primary actor           | Registered Citizen |
| Supporting actors       | - |
| Stakeholders' interests | Registered Citizen: wants to consult Reported Issues |
| Precondition            | The user is logged in its account |
| Minimum guarantees      | Reported Issues are correctly displayed without allowing changes |
| Success guarantees      | The user select and access informations about a specific area or Reported Issue |
| Trigger                 | - |
| Main success scenario   | 1. The system presents the public portal with two viewing modes: Map and Table. <br> 2. The user visually explores the city of Turin via the interactive map.<br>3. The user can optionally apply filters by category, status, or period in the table view.<br>4. The user selects a specific report by clicking directly on the marker on the map or the corresponding row in the table.<br>5. The system identifies the selected report and displays the full details. |
| Extensions              | 3a.1 The user sorts the table using filters. <br> 3a.2 The system updates the list order.<br><br>4a.1 The user filters an area of ​​the map with no flags.<br>4a.2 The system informs the user and suggests changing the area or filters. |

| Use Case                | Export Result |
|:------------------------|:----------------------------|
| ID                      | UC12 |
| Scope                   | Participium |
| Level                   | User-Goal |
| Intention in Context    | Allow the user to download data of the Reported Issues |
| Primary actor           | Registered Citizen |
| Supporting actors       | - |
| Stakeholders' interests | Registered Citizen: wants to have structured data of the Reported Issues to be used for personal offline analysis |
| Precondition            | The user is consulting the list of the of the reports (UC11) |
| Minimum guarantees      | In case of error, any corrupted file is generated and the user is alerted |
| Success guarantees      | A file containing all the data of the Reports selected by the user is generated and downloaded on the user device |
| Trigger                 | The user select the command to export the results from te Table view |
| Main success scenario   | 1. The citizen applies the desired filters (category, status, period) in the table view (UC11). <br> 2. The user presses the button to export results.<br>3. The system extracts the data corresponding to the active filters from the database.<br>4. The system generates a structured file.<br>5. The system automatically downloads the file to the user's device.<br>**The use case terminates with success** |
| Extensions              | 2a.1 La lista dei report risultante dai filtri è vuota.<br>2a.2 Il sistema disabilita la funzione di export.<br>**Use case fails**  |

| Use Case                | Message Channel |
|:------------------------|:----------------------------|
| ID                      | UC13 |
| Scope                   | Participium |
| Level                   | User-Goal |
| Intention in Context    | Allow the direct comunication between Registered Citizen and Municipal Officers |
| Primary actor           | Registered Citizen |
| Supporting actors       | Municipal Officer |
| Stakeholders' interests | Registered Citizen: wants to provide clarifications and gets direct feedbacks about its Reported Issues <br> Municipal Officer: wants to ask additional informations to handle the Issue |
| Precondition            | The user is logged in its account and selected a specific Report |
| Minimum guarantees      | Messages in the chat are saved and permanently associated to the Report |
| Success guarantees      | The message is sent to the receiver |
| Trigger                 | A Registered Citizen or a Municipal Officer decide to send a message to get or provide informations |
| Main success scenario   | 1. The user accesses the report details page.<br>2. The user selects the messaging/chat section.<br>3. The user composes a text message and sends it.<br>4. The system saves the message in the database, associating it with the report ID.<br>5. The system generates an in-app notification for the other interested party (reporting Registered Citizen or designated Municipal Officer). <br>**The use case terminates with success** |
| Extensions              | 3a.1 The user cancels the operation before sending.<br>3a.2 The system does not save the message. <br>**Use case fails**<br><br>5a.1 The recipient has enabled email notifications.<br>5a.2 The system sends an email notification of the new message received. |

| Use Case                | Track Status |
|:------------------------|:----------------------------|
| ID                      | UC14 |
| Scope                   | Participium |
| Level                   | User-Goal |
| Intention in Context    | Allow the Municipal Officer to monitor the management process of reports to coordinate the technical offices and ensure problem resolution |
| Primary actor           | Municipal Officer |
| Supporting actors       | - |
| Stakeholders' interests | Municipal Officer: Oversees the progress of work and manages priorities among the various "In Progress" reports. <br>Politician: Ensures efficient response times. |
| Precondition            | The user is logged in its account and is in the dashboard to manage Reports |
| Minimum guarantees      | The system shows the immutable history of status changes (audit trail) for each report |
| Success guarantees      | The Municipal Officer gets a clear view of who managed the report and what stage the intervention is currently in |
| Trigger                 | The Municipal Officer accesses the list of reports assigned or awaiting review |
| Main success scenario   | 1. The Municipal Officer accesses the dashboard and filters reports by status (e.g., "Assigned" or "In Progress").<br>2. The Municipal Officer selects a specific report to monitor its progress.<br>3. The system displays the current status and complete history of each step (e.g., who approved it, which technical office it was assigned to).<br>4. The Municipal Officer checks for any clarification messages between citizens and technical offices (UC13). <br>**The use case terminates with success** |
| Extensions              | - |

| Use Case                |Report details page|
|:------------------------|:----------------------------|
| ID                      |UC15                         |
| Scope                   |Participium                  |
| Level                   |Subfunction                  |
| Intention in Context    |citizens and municipal staff can view the complete content of a report and understand the issue and follow updates.|
| Primary actor           |citizens                     |
| Supporting actors       |-        |
| Stakeholders' interests |Citizens can watch the updated evolution in the webpage and physics|
| Precondition            |The report has been submitted successfully|
| Minimum guarantees      |Citizens can watch the complete content of a report that submitted from the Citizen and updated processing from the staff                             |
| Success guarantees      | The report is  analyzed|
| Trigger                 |after submitting a report or received a notification|
| Main success scenario   | 1. the citizen choose one of the submitted report from the map view<br>2. the citizen access the report details page <br>3. the system displays the detailed information regarding the report including:<br>* title, description, category,<br>* location (shown on the map),<br>* attached photos,<br>* current status and available updates.<br>4. the citizen check the current status<br>**The use case terminates with success**|
| Extensions              |-                            |

| Use Case                |Public statistics|
|:------------------------|:----------------------------|
| ID                      |UC16                             |
| Scope                   |Participium                  |
| Level                   |User Goal                    |
| Intention in Context    |Every actor is able to check transparent reports in statistaically by category and trends over time|
| Primary actor           |Visitor                      |
| Supporting actors       |-           |
| Stakeholders' interests |Visitors and municiple officers want watch transparent aggregated information about reports.<br>The admini. office wants to provide unsensitive data to public|
| Precondition            |Reports have been uploaded and categorized successfully|
| Minimum guarantees      |                             |
| Success guarantees      |Visitors can see public statistics only|
| Trigger                 |-                            |
| Main success scenario   |1.The visitor opens the statistics page and then accesses the public statistics page.<br>2.The webpage shows the number of reports statistics by means of category and trends over time<br>3.The visitor can choose which category, day, week and month.<br>**The use case terminates with success**|
| Extensions              | 3a.1 There is not available data<br>3a.2 the entry will be present an blank space|

| Use Case                |Private Statistics|
|:------------------------|:----------------------------|
| ID                      |UC17                         |
| Scope                   |Participium                  |
| Level                   |User Goal                    |
| Intention in Context    |analytics features for both transparency and internal management|
| Primary actor           |administrators|
| Supporting actors       |-                            |
| Stakeholders' interests |-                            |
| Precondition            |Reports have been uploaded and categorized successfully and login in administrators' account |
| Minimum guarantees      |Only administrator's account can access the private statistics page.|
| Success guarantees      |Private Statistics are presented by charts and tables| 
| Trigger                 |click the private page link|
| Main success scenario   |1. The actor opens the statistics page and then selects the private channel<br>2. The system asks for the administrator's account to login<br>3. The system displays the number of 1:status, 2:type, 3:type and status, 4:reporter, 5:reporter and type 6:reporter, type, and status<br>4. The system displays number of reports submitted by the top 1% of reporters by type and number of reports submitted by the top 5% of reporters, by type.<br>**The use case terminates with success** |
| Extensions              | 2a.1 the actor has loged as an administrator,<br>2a.2 skiping to the step 2 in which goes to step 3<br><br>2b.1 the actor loged into an account except administrator account, <br>2b.2 the system will redirect to public statistics page and print the message that dont have an authorization.<br><br>3a.1 there is not available data<br>3a.2 then it will be present an blank space|

# 3) Traceability Table

| UC ID | REQ ID |
| :---- | :----- |
| UC-01 | FR-1.1, FR-1.2  |
| UC-02 | FR-5  |
| UC-03 | FR-1.3  |
| UC-04 | FR-2.1, FR-2.2, FR-2.3  |
| UC-05 | FR-1  |
| UC-06 | FR-3.2  |
| UC-07 | FR-4  |
| UC-08 | FR-3.1, FR-3.2  |
| UC-09 | FR-2.1  |
| UC-10 | FR-3.1  |
| UC-11 | FR-3.1 |
| UC-12 | FR-8  |
| UC-13 | FR-7  |
| UC-14 | FR-3.1  |
| UC-15 | FR-3.2  |
| UC-16 | FR-5  |
| UC-17 | FR-6  |
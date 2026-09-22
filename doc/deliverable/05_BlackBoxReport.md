## 1 `participium.services.auth_service.AuthService.authenticate`

Suggested test file: `test_authenticate.py`

Prototype: `authenticate(identifier: str, password: str) -> User`

| TC-ID | identifier | password | Expected | Fixture |
| :---- | :--------- | :------- | :------- | :------ |
| 1.1 | "example_citizen" | "Pass123!" | Return User object | Citizen account is registered and email is verified. |
| 1.2 | "example_citizen" | "wrong_pass" | Raise `UnauthorizedError` | Account exists in the database. |
| 1.3 | "unknown_user" | "any_pass" | Raise `NotFoundError` | No matching identifier found in the system. |
## 2 `participium.core.utils.parse_date`

Suggested test file: `test_parse_date.py`

Prototype: `parse_date(value: str | None) -> datetime | None`

| TC-ID | value | Expected | Fixture |
| :---- | :---- | :------- | :------ |
| 2.1 | "2026-04-25" | `datetime(2026, 4, 25)` | None |
| 2.2 | None | `None` | None |
| 2.3 | "invalid_date" | Raise `ValueError` | None |
## 3 `participium.core.status_flow.ensure_transition_allowed`

Suggested test file: `test_status_flow.py`

Prototype: `ensure_transition_allowed(current_status: ReportStatus, next_status: ReportStatus) -> bool`

Allowed transitions:
`Pending Approval -> Pending Approval | Assigned | Rejected`;
`Assigned -> Assigned | In Progress | Suspended | Resolved`;
`In Progress -> In Progress | Suspended | Resolved`;
`Suspended -> Suspended | In Progress | Resolved`;
`Rejected -> Rejected`;
`Resolved -> Resolved`.

| TC-ID | current_status | next_status | Expected | Fixture |
| :---- | :------------- | :---------- | :------- | :------ |
| 3.1  |  Pending_approval| Pending_approval | True | None |
| 3.2| Pending_approval | Assigned | True|None|
|3.3|Pending_approval|Rejected|True|None|
|3.4|Pending_approval|In_progress|False|None|
|3.5|Pending_approval|Suspended|False|None|
|3.6|Pending_approval|Resolved|False|None|
|3.7|Assigned| Pending_approval | False |None  |
|3.8|Assigned| Assigned | True|None|
|3.9|Assigned|Rejected|False|None|
|3.10|Assigned|In_progress|True|None|
|3.11|Assigned|Suspended|True|None|
|3.12|Assigned|Resolved|True|None|
|3.13|In_progress| Pending_approval | False | None |
|3.14|In_progress| Assigned | False|None|
|3.15|In_progress|Rejected|False|None|
|3.16|In_progress|In_progress|True|None|
|3.17|In_progress|Suspended|True|None|
|3.18|In_progress|Resolved|True|None|
|3.19|Suspended| Pending_approval | False | None |
|3.20|Suspended| Assigned | False|None|
|3.21|Suspended|Rejected|False|None|
|3.22|Suspended|In_progress|True|None|
|3.23|Suspended|Suspended|True|None|
|3.24|Suspended|Resolved|True|None|
|3.25|Rejected| Pending_approval | False |None  |
|3.26|Rejected| Assigned | False|None|
|3.27|Rejected|Rejected|True|None|
|3.28|Rejected|In_progress|False|None|
|3.29|Rejected|Suspended|False|None|
|3.30|Rejected|Resolved|False|None|
|3.31|Resolved| Pending_approval | False | None |
|3.32|Resolved| Assigned | False|None|
|3.33|Resolved|Rejected|False|None|
|3.34|Resolved|In_progress|False|None|
|3.35|Resolved|Suspended|False|None|
|3.36|Resolved|Resolved|True|None|

## 4 `participium.services.report_service.ReportService.create_report`

Suggested test file: `test_create_report.py`

Prototype: `create_report(reporter: User, category_id: int | str | None, title: str | None, description: str | None, latitude: float | str | None, longitude: float | str | None, photos: list[FileStorage], is_anonymous: bool = False) -> Report`

| TC-ID | reporter | category_id | title | description | latitude | longitude | photos | is_anonymous | Expected | Fixture |
| :---- | :------- | :---------- | :---- | :---------- | :------- | :-------- | :----- | :----------- | :------- | :------ |
| 4.1 | valid_user | 3 | "Broken streetlight" | "Streetlight on Via Moretta has been broken for 4 days"  | 45.0680 | 7.6531 | [lamp.jpg] | False | Returns Report | VALID_USER, ACTIVE_CATEGORY, VALID_PHOTO |
| 4.2 | valid_user | 3 | "Broken streetlight" | "Streetlight on Via Moretta has been broken for 4 days"  | 45.0680 | 7.6531 | [lamp.jpg] | True | Returns Report with is_anonymous = True | VALID_USER, ACTIVE_CATEGORY, VALID_PHOTO |
| 4.3 | valid_user | 3 | "Broken streetlight" | "Streetlight on Via Moretta has been broken for 4 days"  | 45.0680 | 7.6531 | [lamp1.jpg, lamp2.jpg, lamp3.jpg] | False | Returns Report with 3 photos | VALID_USER, ACTIVE_CATEGORY, VALID_PHOTO |
| 4.4 | valid_user | 3 | "Broken streetlight" | "Streetlight on Via Moretta has been broken for 4 days"  | "45.0680" | "7.6531" | [lamp1.jpg] | False | Returns Report(string coordinates) | VALID_USER, ACTIVE_CATEGORY, VALID_PHOTO |
| 4.5 | valid_user | None | "Pothole" | "Large pothole on Via Roma"  | 45.0653 | 7.6808 | [hole.jpg] | False | Raises ValidationError (missing category) | VALID_USER |
| 4.6 | valid_user | "road damage" | "Pothole" | "Large pothole on Via Roma"  | 45.0653 | 7.6808 | [hole.jpg] | False | Raises ValidationError (malformed category) | VALID_USER |
| 4.7 | valid_user | 101 | "Pothole" | "Large pothole on Via Roma"  | 45.0653 | 7.6808 | [hole.jpg] | False | Raises ValidationError (inactive/unknown category) | VALID_USER, INACTIVE_CATEGORY |
| 4.8 | valid_user | 2 | None | "Large pothole on Via Roma"  | 45.0653 | 7.6808 | [hole.jpg] | False | Raises ValidationError (missing title) | VALID_USER,ACTIVE_CATEGORY |
| 4.9 | valid_user | 2 | "Pothole" | None  | 45.0653 | 7.6808 | [hole.jpg] | False | Raises ValidationError (missing description) | VALID_USER, ACTIVE_CATEGORY |
| 4.10 | valid_user | 1 | "Damaged road sign" | "Stop sign knocked over"  | None | 7.6808 | [sign.jpg] | False | Raises ValidationError (missing latitude) | VALID_USER, ACTIVE_CATEGORY |
| 4.11 | valid_user | 1 | "Damaged road sign" | "Stop sign knocked over"  | 45.0653 | None | [sign.jpg] | False | Raises ValidationError (missing longitude) | VALID_USER, ACTIVE_CATEGORY |
| 4.12 | valid_user | 1 | "Damaged road sign" | "Stop sign knocked over"  | "south" | 7.6808 | [sign.jpg] | False | Raises ValidationError (invalid latitude) | VALID_USER, ACTIVE_CATEGORY |
| 4.13 | valid_user | 1 | "Damaged road sign" | "Stop sign knocked over"  | 45.0653 | "west" | [sign.jpg] | False | Raises ValidationError (invalid longitude) | VALID_USER, ACTIVE_CATEGORY |
| 4.14 | valid_user | 4 | "broken bench" | "completely broken bench in parco del valentino"  | 45.0558 | 7.6883 | [] | False | Raises ValidationError (no photos provided) | VALID_USER, ACTIVE_CATEGORY |
| 4.15 | valid_user | 4 | "broken bench" | "completely broken bench in parco del valentino"  | 45.0558 | 7.6883 | [bench1.jpg, bench2.jpg, bench3.jpg, bench4.jpg] | False | Raises ValidationError (more than 3 photos provided) | VALID_USER, ACTIVE_CATEGORY |
|4.16|valid_user|4|"broken bench"|"completely broken bench in parco del valentino"| 45.0558 | 7.6883 | [photo_no_name] | False | Raises ValidationError (no valid photos) | VALID_USER, ACTIVE_CATEGORY, PHOTO_NO_FILENAME |


## 5 `participium.services.report_service.ReportService.update_status`

Suggested test file: `test_update_status.py`

Prototype: `update_status(report_id: int, operator: User, next_status_value: str, note: str | None = None) -> Report`

| TC-ID | report_id | operator | next_status_value | note | Expected | Fixture |
| :---- | :-------- | :------- | :---------------- | :--- | :------- | :------ |
| 5.1 | existing_id | admin | valid_status | None | Return a updated report | Report and User |
| 5.2 | non-existing_id | admin | valid_status | None | raises NotFoundError | Report and User |
| 5.3 | existing_id | citizen | valid_status | None | raises AuthorizationError | Report and User |
| 5.4 | existing_id_with_category B | authorized_operator_with_cateogy A |valid_status | None | raises AuthorizationError | report.category_id and operator.category_id and User |
| 5.5 | existing_id | admin | invalid_status | None | raises ValidationError |ReportStatus and User |
| 5.6 | existing_id with PENDING_APPROVAL status | admin | IN PROGRESS | None | raises ValidationError | Report.status and allowed_transitions and User |
| 5.7 | existing_id | admin | REJECTED | None | raises ValidationError | Report and User |
| 5.8 | existing_id | admin | REJECTED | "" | raises ValidationError | Report and User |
| 5.9 | existing_id with category A | authorized_operator with category A | ASSIGNED | None | Returns updated Report | report pending approval in category A and User |
| 5.10 | existing_id with PENDING_APPROVAL | admin | REJECTED | "👍reson👍" | Return updated Report | report_pending_approval and User |
| 5.11 | existing_id with ASSIGNED | admin | ASSIGNED | None | Return updated Report | report and User |

## 6 `participium.services.report_service.ReportService.list_public_reports`

Suggested test file: `test_public_reports.py`

Prototype: `list_public_reports(category_id: int | None = None, status: ReportStatus | None = None, date_from: datetime | None = None, date_to: datetime | None = None, sort: str = "desc") -> list[Report]`

| TC-ID | category_id | status | date_from | date_to | sort | Expected | Fixture |
| :---- | :---------- | :----- | :-------- | :------ | :--- | :------- | :------ |
| 6.1 | None | None | None | None | "asc" | Return a list of all visible reports in ascending creation timestamp order | storageDB |
| 6.2 | None | None | None | None |  | Return a list of all visible reports in descendingcreation timestamp order | storageDB |
| 6.3 | category_id | None | None | None | "asc" | Return a list of reports following category_id in ascending | storageDB |
| 6.4 | None | status in Reportstatus | None | None | "asc" | Returns only reports with certain status | storageDB |
| 6.5 | None | None | x_datetime | None | "asc" | Return reports after x_datetime |storageDB|
| 6.6 | None | None | None | y_datetime | "asc" | Return reports before y_datetime |storageDB|
| 6.7 | None | None | x_datetime | y_datetime | "asc" | Return reports between x_datetime and y_datetime |storageDB|
| 6.8 | category_id | PENDING_APPROVAL | x_datetime | y_datetime | "asc" | Return a list of certain reports |storageDB|U
| 6.9 | category_id | PENDING_APPROVAL | x_datetime | y_datetime | "asc" | Return an enpty list |storageDB|

## 7 `participium.services.messaging_service.MessagingService.send_message`

Suggested test file: `test_send_message.py`

Prototype: `send_message(report: Report, sender: User, body: str) -> Message`

| TC-ID | report | sender | body | Expected | Fixture |
| :---- | :----- | :----- | :--- | :------- | :------ |
| TC-7.1 | existing_with_recipient | authorized | "Valid message" | Return persisted `Message` | REPORT_WITH_RECIPIENT, AUTHORIZED_USER |
| TC-7.2 | existing_with_recipient | authorized | " Valid message " | Return persisted `Message` with trimmed body | REPORT_WITH_RECIPIENT, AUTHORIZED_USER |
| TC-7.3 | existing_with_recipient | unauthorized | "Valid message" | Raises `AuthorizationError` | REPORT_WITH_RECIPIENT, UNAUTHORIZED_USER |
| TC-7.4 | existing_without_recipient | authorized | "Valid message" | Raises `ValidationError` | REPORT_WITHOUT_RECIPIENT, AUTHORIZED_USER |
| TC-7.5 | existing_with_recipient | authorized | "" | Raises `ValidationError` | REPORT_WITH_RECIPIENT, AUTHORIZED_USER |
| TC-7.6 | existing_with_recipient | authorized | "  " | Raises `ValidationError` | REPORT_WITH_RECIPIENT, AUTHORIZED_USER |

## 8 `participium.core.security.verify_password`

Suggested test file: `test_verify_password.py`

Prototype: `verify_password(password: str, password_hash: str) -> bool`

| TC-ID | password | password_hash | Expected | Fixture |
| :---- | :------- | :------------ | :------- | :------ |
| TC-8.1 | "correct_pwd" | "correct_hash" | True | - |
| TC-8.2 | "wrong_pwd" | "correct_hash" | False | - |
| TC-8.3 | "" | "correct_hash" | False | - |
| TC-8.4 | "correct_pwd" | "not-an-hash" | False | - |
| TC-8.5 | "correct_pwd" | "" | False | - |

## 9 `participium.services.notification_service.NotificationService.create_notification`

Suggested test file: `test_create_notification.py`

Prototype: `create_notification(user: User | None, notification_type: NotificationType, title: str, body: str, report: Report | None = None) -> Notification | None`

| TC-ID | user | notification_type | title | body | report | Expected | Fixture |
| :---- | :--- | :---------------- | :---- | :--- | :----- | :------- | :------ |
| TC-9.1 | non_null_user | SYSTEM | "title" | "body" | None | Return a persisted `Notification` associated to the user | NON_NULL_USER |
| TC-9.2 | non_null_user | STATUS_CHANGE  | "title" | "body" | valid_report | Return a persisted `Notification` associated to the user and the report | NON_NULL_USER, VALID_REPORT |
| TC-9.3 | non_null_user | MESSAGE | "title" | "body" | valid_report | Return a persisted `Notification` associated to the user and the report | NON_NULL_USER, VALID_REPORT |
| TC-9.4 | None | SYSTEM | "title" | "body" | None | Return `None` |  |
| TC_9.5 | None | STATUS_CHANGE | "title" | "body" | valid_report | Return `None` | VALID_REPORT |
| TC_9.6 | None | MESSAGE | "title" | "body" | valid_report | Return `None` | VALID_REPORT |
| TC-9.7 | non_null_user | SYSTEM | "" | "body" | None | Return a `Notification` (with empty title) | NON_NULL_USER |
| TC-9.8 | non_null_user | SYSTEM | "title" | "" | None | Return a `Notification` (with empty body) | NON_NULL_USER |
| TC-9.9 | user_without_email | SYSTEM | "title" | "body" | None | Return a `Notification` that will not be sent | USER_WITHOUT_EMAIL |

## 10 `participium.services.user_service.UserService.update_profile`

Suggested test file: `test_update_profile.py`

Prototype: `update_profile(user: User, username: str | None = None, first_name: str | None = None, last_name: str | None = None, email_notifications_enabled: bool | None = None, profile_picture: FileStorage | None = None) -> User`

| TC-ID | user | username | first_name | last_name | email_notifications_enabled | profile_picture | Expected | Fixture |
| :---- | :--- | :------- | :--------- | :-------- | :-------------------------- | :-------------- | :------- | :------ |
| TC-10.1 | existing_user | "new_username" | "Mario" | "Rossi" | True | valid_img | Return `User` object with updated fields | EXISTING_USER |
| TC-10.2 | existing_user | None | None | None | None | None | Return `User` object (fields are not overwritten by None) | EXISTING_USER |
| TC-10.3 | existing_user | EXISTING_USER_B.username | None | None | None | None | Raise `ValidationError` exception (and the username is not updated) | EXISTING_USER, EXISTING_USER_B |
| TC-10.4 | existing_user | existing_user.username | None | None | None | None | Return `User` object (updating the username with the same username must not raise an exception) | EXISTING_USER |
| TC-10.5 | existing_user | None | None | None | False | None | Return `User` object with the email_notifications_enabled field updated (other fields are not overwritten by None) | EXISTING_USER |
| TC-10.6 | existing_user | "" | None | None | None | None | Return `User` object with empty username (other fields are not overwritten by None) | EXISTING_USER |
| TC-10.7 | existing_user | None | "" | None | None | None | Return `User` object with empty first_name (other fields are not overwritten by None) | EXISTING_USER |
| TC-10.8 | existing_user | None | None | "" | None | None | Return `User` object with empty last_name (other fields are not overwritten by None) | EXISTING_USER |
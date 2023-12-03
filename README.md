# Task Manager API

Task Manager API for any web app project. Built using FastAPI.

## Basic functionality

- User creation
- Authorization
- Task creation

### Extra features

- User groups: Allows different users share their tasks. [IN PROGRESS]
- Task groups: Allows users categorize and share their tasks. [IN PROGRESS]

## Routes

The following routes have been defined and are up and running.

| **Route category** | **Route** | **Request method** | **Description** | **Scope** |
|---|:---:|:---:|:---:|---|
| Default | / | GET |  | Public |
| Users | /users/ | POST | Create a user | Public |
|  | /users/ | DELETE | Delete a user | Private |
|  | /users/me/ | GET | Request user information | Private |
| Login | /login/ | POST | Authorize a user (Request Bearer token). | Private |
| Tasks | /tasks/ | POST | Create a task group | Private |
|  | /tasks/ | GET | Request tasks | Private |
|  | /tasks/{task_id}/ | GET | Request task | Private |
|  | /tasks/{task_id}/ | DELETE | Delete a task | Private |
|  | /tasks/{task_id}/task_groups/ | POST | Assign task to a task group | Private |
|  | /tasks/{task_id}/task_groups/{group_id}/ | DELETE | Remove task from a task group | Private |
| User Groups | /user_groups/ | GET | Request user groups | Private |
|  | /user_groups/ | POST | Create a user group | Private |
|  | /user_groups/{group_id}/ | GET | Request a user group | Private |
|  | /user_groups/{group_id}/ | DELETE | Delete a user group | Private |
|  | /user_groups/{group_id}/members/ | POST | Assign user to a user group | Private |
|  | /user_groups/{group_id}/members/{member_id} | DELETE | Remove user from a user group | Private |
| Task Groups | /task_groups/ | GET | Request task groups | Private |
|  | /task_groups/ | POST | Create a task group | Private |
|  | /task_groups/{group_id} | DELETE | Delete a task group | Private |
|  | /task_groups/{group_id} | GET | Request a task group | Private |

**Note:** A private route requires an authorization token. An authorization token can be requested via user login in the /login/ route.

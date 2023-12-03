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

| **Route category** | **Route** | **Request method** | **Description** |
|---|:---:|:---:|:---:|
| Default | / | GET |  |
| Users | /users/ | POST | Create a user |
|  | /users/ | DELETE | Delete a user |
|  | /users/me/ | GET | Request user information |
| Login | /login/ | POST | Authorize a user (Request Bearer token). |
| Tasks | /tasks/ | POST | Create a task group |
|  | /tasks/ | GET | Request tasks |
|  | /tasks/{task_id}/ | GET | Request task |
|  | /tasks/{task_id}/ | DELETE | Delete a task |
|  | /tasks/{task_id}/task_groups/ | POST | Assign task to a task group |
|  | /tasks/{task_id}/task_groups/{group_id}/ | DELETE | Remove task from a task group |
| User Groups | /user_groups/ | GET | Request user groups |
|  | /user_groups/ | POST | Create a user group |
|  | /user_groups/{group_id}/ | GET | Request a user group |
|  | /user_groups/{group_id}/ | DELETE | Delete a user group |
|  | /user_groups/{group_id}/members/ | POST | Assign user to a user group |
|  | /user_groups/{group_id}/members/{member_id} | DELETE | Remove user from a user group |
| Task Groups | /task_groups/ | GET | Request task groups |
|  | /task_groups/ | POST | Create a task group |
|  | /task_groups/{group_id} | DELETE | Delete a task group |
|  | /task_groups/{group_id} | GET | Request a task group |

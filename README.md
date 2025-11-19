# Custom Authentication and Authorization System

## Overview
This project implements a custom authentication and authorization system using Django and Django Rest Framework. It avoids using Django's built-in `Groups` and `Permissions` in favor of a custom Role-Based Access Control (RBAC) schema stored in the database.

## Permission Schema

The system is built around the following concepts:

1.  **User**: The entity requesting access. A user can have multiple **Roles**.
2.  **Role**: A named collection of **Permissions**. (e.g., "Admin", "Editor", "Viewer").
3.  **Permission**: A granular rule allowing a specific **Action** on a specific **Resource**.
4.  **Resource**: A system entity that needs protection (e.g., "Document", "Report", "User").
5.  **Action**: An operation that can be performed on a resource (e.g., "read", "create", "update", "delete").

### Database Models

#### 1. Resource
- `name`: Human-readable name (e.g., "Document").
- `code`: Unique identifier used in code checks (e.g., "document").

#### 2. Action
- `name`: Human-readable name (e.g., "Read").
- `code`: Unique identifier used in code checks (e.g., "read").

#### 3. Permission
- `resource`: FK to Resource.
- `action`: FK to Action.
- *Constraint*: Unique together (resource, action).
- *Representation*: often denoted as `resource.action` (e.g., "document.read").

#### 4. Role
- `name`: Unique name of the role.
- `permissions`: ManyToMany field to Permission.

#### 5. User (Custom)
- `roles`: ManyToMany field to Role.

### Access Control Logic

When a user requests access to an endpoint:
1.  The endpoint defines the required permission (e.g., `document.read`).
2.  The system checks the user's assigned roles.
3.  It collects all permissions associated with those roles.
4.  If the required permission is present in the user's permission set, access is **granted**.
5.  Otherwise, access is **denied** (403 Forbidden).
6.  If the user is not authenticated, access is **denied** (401 Unauthorized).

## API Usage

### Authentication
- **Register**: `POST /api/auth/register/`
- **Login**: `POST /api/auth/login/`
- **Logout**: `POST /api/auth/logout/`

### User Management
- **Profile**: `GET /api/users/me/`
- **Update**: `PATCH /api/users/me/`
- **Delete**: `DELETE /api/users/me/` (Soft delete)

### Permission Management (Admin)
- **Roles**: `GET/POST /api/permissions/roles/`
- **Resources**: `GET/POST /api/permissions/resources/`
- **Assign Role**: `POST /api/permissions/assign/`

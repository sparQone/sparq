# User and Group System

## Overview
The user-group system manages user memberships in groups, with specific rules for system groups and admin protection.

## Schema & Associations
- Users and Groups have a many-to-many relationship through user_group table
- Each user can belong to multiple groups
- Each group can have multiple users
- Groups have properties: name, description, and is_system flag

## System Groups

### ALL Group
- System group (is_system=True)
- Every user must belong to this group
- Cannot be removed from any user
- Created during system initialization

### ADMIN Group
- System group (is_system=True)
- Must always have at least one member
- Grants administrative privileges
- Created during system initialization

## Admin Protection Mechanisms

### Database Level
- Before removing a user from ADMIN group, system checks admin count
- If count would drop to zero, operation is blocked

### Application Level
- UI disables admin checkbox for last admin
- Warning message shown to last admin
- API endpoints validate admin count before group changes
- Group management routes check for admin status

### Model Level
- User model has is_admin property checking ADMIN group membership
- is_sole_admin property to check if user is last admin
- Group removal methods validate admin count

## Enforcement Points
1. **Creation**: All users automatically added to ALL group
2. **Modification**: Cannot remove last admin (checked at multiple levels)
3. **Deletion**: Prevents deletion of system groups
4. **UI**: Prevents UI actions that would violate these rules
5. **API**: Validates all group membership changes

This design ensures system integrity by maintaining required group memberships while preventing accidental removal of administrative access.
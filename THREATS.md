
# TrustVault – Threat Model

## 1. Purpose
This document describes the security threats, risks and protection mechanisms considered in TrustVault.

## 2. Assets to Protect
- User accounts and credentials
- Uploaded documents
- Document permissions
- Audit events
- User and document metadata

## 3. Potential Threat Actors
- Unauthenticated attackers
- Malicious authenticated users
- Users attempting to access documents without permission
- Users attempting to bypass role restrictions

## 4. Main Threats and Mitigations

### Unauthorized Document Access
Threat: A user attempts to access a document that was not shared with them.

Mitigation: Server-side permission validation is performed before document viewing and downloading.

### Permission Revocation Bypass
Threat: A user attempts to download a document after their access has been revoked.

Mitigation: Current permissions are checked on every protected download request.

### Unauthorized Upload
Threat: A Viewer attempts to upload documents through the API.

Mitigation: The API allows document uploads only for users with the OWNER role.

### Unauthorized Document Modification
Threat: A user attempts to edit a document without EDIT permission.

Mitigation: Document edit requests require server-side EDIT permission validation.

### Unauthorized Deletion
Threat: A shared user attempts to delete another user's document.

Mitigation: Only the document owner can delete the document.

### Audit Log Manipulation
Threat: An attacker attempts to modify audit records.

Mitigation: Audit events use a SHA-256 hash-chain mechanism to make unauthorized changes detectable when the chain is verified.

## 5. Known Limitations
- A database administrator or attacker with full database control may rewrite the audit records and hash chain.
- Independent immutable audit backups are not yet implemented.
- A document already downloaded by an authorized user cannot be remotely recalled.
- Production deployment requires HTTPS, secure secret management, private file storage and additional hardening.
- This project has not undergone an independent security audit.

## 6. Security Testing
The following checks were performed:
- Revoked Viewer download attempt returned HTTP 403.
- Viewer API upload attempt returned HTTP 403.
- Django system checks completed without issues.

## 7. Conclusion
TrustVault implements basic role-based access control, protected document operations and audit logging. Additional security controls are required before production use.

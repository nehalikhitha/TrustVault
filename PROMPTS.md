
# TrustVault – AI Prompts and Assistance Log

This document records AI assistance used during the development of TrustVault.

## Entry 1 – 2026-11-08
**Topic:** Django Project Architecture

**Prompt:** Help me design a secure document-sharing application using Python, Django and Django REST Framework with ADMIN, OWNER and VIEWER roles.

**Outcome:** Received guidance on project structure, Django apps, models and role-based access control.

## Entry 2 – 2026-11-08
**Topic:** Document Permissions

**Prompt:** Help implement document-level READ and EDIT permissions, including granting and revoking access.

**Outcome:** Developed permission models, service functions and sharing/revocation workflows.

## Entry 3 – 2026-11-08
**Topic:** Authorization Security

**Prompt:** Help prevent unauthorized users from viewing or downloading documents after permission revocation.

**Outcome:** Implemented server-side permission checks and verified that a revoked Viewer receives HTTP 403 on document download.

## Entry 4 – 2026-11-08
**Topic:** Audit Logging

**Prompt:** Help implement audit events for document uploads, views, downloads, edits and permission changes.

**Outcome:** Implemented audit event recording and a SHA-256 hash-chain mechanism.

## Entry 5 – 2026-11-08
**Topic:** API Security Testing

**Prompt:** Help prevent VIEWER users from uploading documents directly through the Django REST API.

**Outcome:** Added an OWNER-only upload restriction and tested that a Viewer upload attempt returns HTTP 403.

## AI Usage Disclosure
AI assistance was used for learning, code guidance, debugging and documentation. The project code was reviewed and tested during development by the developer.

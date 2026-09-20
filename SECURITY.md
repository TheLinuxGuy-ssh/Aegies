# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Aegies, please report it responsibly:

1. **Do not** create a public issue for the vulnerability
2. **Email** the maintainer at: [your-email@domain.com]
3. Include:
   - A description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggested fixes (optional)

We will acknowledge receipt within 48 hours and provide a timeline for a fix.

## Security Considerations

Aegies is a local-only CLI tool that:

- Stores data in a local SQLite database (`~/.aegies/tracker.db`)
- Does not make any network requests
- Does not transmit any data externally
- Does not execute user-provided code
- Uses parameterized SQL queries to prevent injection

The main security consideration is local file system access. The database file is created with default permissions in the user's home directory.
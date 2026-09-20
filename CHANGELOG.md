# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-20

### Added
- Initial release of Aegies DSA Tracker
- Leitner-system spaced-repetition scheduling (5 boxes, up to 30-day intervals)
- CLI commands:
  - `aegies add` — Add new DSA problems with difficulty (Easy/Medium/Hard)
  - `aegies list p` — List all tracked problems
  - `aegies list d` — List problems due for review today
  - `aegies list r` — List full review history
  - `aegies review` — Record review result (correct/wrong)
  - `aegies stats` — Show overall success rate
- SQLite database with automatic schema creation at `~/.aegies/tracker.db`
- Raw parameterized SQL (no ORM)
- Context manager for database connections with automatic commit/rollback
- Custom exceptions for error handling
- Test suite with pytest (database layer + scheduler logic)
- MIT License

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A
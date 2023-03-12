# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!-- Template

## [0.0.1] - 1970-01-01
### Added

- X
- Y

### Changed
### Deprecated
### Removed
### Fixed
### Security
-->

## [Unreleased]

## [0.4.1] - 2023-03-12

### Fixed

- Fix type annotation for `Faker.add_provider` (it takes a BaseProvider instance or class) https://github.com/youtux/types-factory-boy/pull/17

## [0.4.0] - 2023-02-28

### Fixed

- Fix type annotation for `FactoryMetaClass.__new__`. Now it returns a `Self` https://github.com/youtux/types-factory-boy/pull/15
- Use `Self` now that mypy 1.0 supports it https://github.com/youtux/types-factory-boy/pull/15

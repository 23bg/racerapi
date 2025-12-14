## [0.0.4] – 2025-12-14

### Added

* Decorator-based controller routing (`@Controller`, `@Get`, `@Post`, `@Put`, `@Delete`)
* Automatic controller discovery and registration from `app/modules`
* Middleware registration via framework settings
* Minimal middleware abstraction for request lifecycle hooks
* Resource generator for module scaffolding (controller, service, schemas, tests)

### Fixed

* Controller loading failures during module discovery
* Incorrect middleware instantiation causing runtime errors
* CLI command registration inconsistencies
* Generator template resolution issues on Windows paths

### Changed

* Standardized module structure (`controller`, `service`, `schemas`, `tests`)
* Simplified middleware configuration to accept middleware classes only
* Improved `racerapi dev` startup reliability and reload behavior

---

### Notes

* This release focuses on **stability and architectural foundations**
* No breaking changes are introduced
* API surface is still considered **pre-stable**


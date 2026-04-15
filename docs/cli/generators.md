# Generators and Templates

Generators write files from templates and perform a basic validation step by trying to import the generated module. Templates are stored in the framework package so they are available when the package is installed in editable mode or as a distribution.

Location of templates:

- `src/racerapi/templates/module` — templates for `api.py`, `service.py`, `repo.py`, `models.py`, `schemas.py`, `deps.py`, and a basic test.

What the generator guarantees:

- Files are written into `src/<pkg>/modules/<name>` (or `src/racerapi/modules/<name>` when not inside a user project).
- After writing files the generator attempts to import `<pkg>.modules.<name>.api` and checks that a `router` attribute exists. If import fails the generator exits with a non-zero status and prints the exception.

This approach prevents common generator pitfalls (broken imports, missing dependencies) and ensures a newly-generated module is importable by the framework.

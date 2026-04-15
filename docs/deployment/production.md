# Production deployment and Docs CI/CD

This page covers two topics: deploying the application to production and deploying the documentation site.

Docs deployment (recommended)

We use MkDocs and GitHub Actions to build and publish the documentation to GitHub Pages. The repository includes a workflow file at `.github/workflows/docs.yml`.

To deploy docs manually from your machine:

```bash
pip install mkdocs-material mkdocs-mermaid2-plugin
mkdocs build
mkdocs gh-deploy --force
```

Notes on GitHub Actions

- The workflow installs MkDocs and required plugins, runs `mkdocs build`, and then runs `mkdocs gh-deploy --force` using the repository's `GITHUB_TOKEN` to push to the `gh-pages` branch.
- Ensure `GITHUB_TOKEN` or an appropriate deploy token is available in secrets for the repository (GitHub automatically provides `GITHUB_TOKEN` in Actions).

Application deployment

Production deployment is out of scope for this document, but the general recommendations:

- Use a process manager (systemd, supervisor, or container orchestrator) to run `uvicorn` with sensible worker/process counts.
- Manage configuration through environment variables; the settings loader validates production safety and requires an explicit database URL in `RACERAPI_DATABASE_URL`.
- Ensure logs are collected centrally — in `prod` environment the logger emits JSON for structured logging.

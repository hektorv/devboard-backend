# Contributing

Thanks for contributing! This file documents the process and conventions for making changes in `devboard-backend`.

Branching and PRs

- Create a feature branch from `main`: `git checkout -b feat/<short-description>`
- Open a PR against `main` with a clear description, motivation, and testing notes.

What we expect in a PR

- All new functionality must include unit tests (services + edge cases) and integration tests for API behavior.
- Any change to API routes/payloads/enums must include an update to `docs/oas.yml` before implementation and a contract test.
- Follow the repository’s code style (Python: PEP8). Use typing where it helps clarity.
- Update docs when behavior or public API changes (including this README or `docs/` files).

Testing & CI

- Run `pytest` locally and ensure coverage does not drop for the affected modules.
- If your change requires DB migrations or new environment variables, document them in `docs/developer-setup.md`.

PR checklist (add to PR description):

- [ ] Tests added/updated
- [ ] `docs/oas.yml` updated (if API changed)
- [ ] `docs/backend-architecture-spec.md` or `docs/*` updated (if behavior changed)
- [ ] All checks passing (CI / tests)

If you have any doubts about the architecture or business rules, open an issue and discuss before starting a large implementation.

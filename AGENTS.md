# aetpi — AGENTS.md

## Package identity

- Repo `aetpi` → PyPI package **`aetpiref`** (import as `import aetpiref`).
- Single package under `src/aetpiref/`, PEP 561 typed with `py.typed`.
- Provides an ASGI-like protocol interface (`AETPIApplication` callable signature) for processing external BPMN tasks.
- Design principle: keep few, non-heavy runtime dependencies (`prek`, `typing-extensions` only).

## Commands

```shell
uv sync                           # install all deps (dev included)
uv sync --group lint              # install only lint group
uv sync --group test              # install only test group
uv build                          # build dist/
uv run pytest                     # run tests (no real tests exist yet)
uv run pytest --cov=src --cov-report=term-missing tests
ruff check src                    # lint
ruff format --check src           # formatter check
ty check src                      # type check (ty, not mypy/pyright)
tox -e ruff                       # lint via tox
tox -e ty                         # type check via tox
tox -e py311                      # tests via tox
git cliff --bump > CHANGELOG.md   # regenerate changelog from conventional commits
uv version <new-version>          # bump version in pyproject.toml
```

## CI/Release flow

- `verify.yaml` runs on PR/push to main: **lint + build only** (test is disabled).
- Release is a two-step manual process:
  1. Run `prepare_release.yaml` workflow (dispatch) — bumps version via `git cliff --bump`, updates `CHANGELOG.md`, commits, tags, pushes.
  2. Tag push `v*.*.*` triggers `release.yaml` — builds, publishes to PyPI, creates GitHub release.
- `uv version` is used for bumping in CI (not `bump-my-version`).

## Conventions

- Feature branches use `feature/<name>` prefix (not `feat/`).
- Conventional commits required for changelog generation (`git-cliff`).
- `ruff` handles both linting and formatting — always run both.
- `ty` for static type analysis (not mypy/pyright).
- Pre-commit hooks include `uv-lock` (lock must be in sync) and `sync-with-uv`.
- Build backend: `uv_build`.
- `PYTHONPATH` must include `{project_root}/src` (set automatically in tox).

## Task plans

- Task plans live in `.opencode/tasks/`, gitignored.
- Name convention: `NNN-descriptive-name.md` (3-digit incrementing number, kebab-case, Markdown).

## Quirks

- No real tests exist yet (`tests/__init__.py` is empty).
- The `ty` pre-commit hook runs `ty check .` with `language: system`.
- `keyring-provider = "subprocess"` in `[tool.uv]`.

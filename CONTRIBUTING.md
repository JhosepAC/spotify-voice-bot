# Contributing — Standards (Phase 0, enforced)

> Language: all code, comments, docstrings, identifiers, commit messages → **English only**.
> Spanish is allowed only in: user-facing TTS strings, `config/responses.json` values, `tests/test_nlp.py` input phrases.

## 1. Conventional Commits (enforced)

Format: `<type>(<scope>): <short imperative summary>`

Types: `feat|fix|refactor|perf|docs|test|chore|ci|build`

- `feat(nlu): ...` new intent or capability
- `fix(nlu): ...` comprehension bug (e.g. shortcut stealing LLM)
- `perf(stt): ...` latency improvement (e.g. whisper medium→small)
- `refactor(config): ...` centralization, no behavior change
- `docs: ...`, `test(nlp): ...`, `chore: ...`

Rules:

- Lowercase type/scope, imperative mood (`add`, not `added`).
- One logical change per commit. No `fix stuff`.
- Branch work is squashed/merged with `--no-ff` into `develop`.

## 2. GitFlow (enforced)

- `master` = production. `develop` = integration. No direct commits to either.
- Branches:
  - `feature/<topic>` → off `develop`, into `develop`
  - `docs/<topic>` → off `develop`, into `develop`
  - `fix/<topic>` → off `develop`, into `develop`
  - `release/*`, `hotfix/*` only when cutting a release.
- This Phase 0 uses one branch per concern (no single mega-branch):
  - `docs/phase0-standards-workflow` (this file)
  - `feature/phase0-nlu-hotfix`
  - `feature/phase0-config-centralization`
  - `feature/phase0-whisper-latency`
  - `feature/phase0-vad-ducking`
  - `feature/phase0-responses-robustness`
- Verify with: `git branch --show-current`, `git status --short`.

## 3. Architecture rules

- Single source of truth: `config/settings.py` (+ `.env`). No hardcoded URLs, model names, thresholds elsewhere. `voice/audio_config.py` keeps backward-compat re-exports only.
- Layering: `voice/` (capture/STT/TTS) → `nlp/` (intent+entities) → `commands/` (router/handlers) → `spotify/` (API). No upward imports (e.g. `nlp` never imports `voice.tts`).
- New audio side-effects (ducking) live in their own module (`voice/ducking.py`), used by `assistant/pipeline.py`. No inline volume hacks in the loop.
- All user-facing strings via `config/responses.json` or handler return values (Spanish OK). All logs/comments in English.
- Tests: `tests/test_nlp.py` uses asserts. New intents require 10+ paraphrases.

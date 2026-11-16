# Annotated replay verification — 17 November 2026

Presentation-only upgrade from the accepted v0.1 foundation. Windows/Python
3.12.10 and Node 24.21.0 were used locally. No changes were made to scenario,
geometry, validation, simulation, controller or monitor logic.

From the replay feature checkout, commands select its source explicitly while
using the already installed sibling development environment:

```powershell
$env:PYTHONPATH = (Join-Path $PWD 'src')
node --test tests/replay.test.cjs
..\openyield\.venv\Scripts\python -m pytest -q
..\openyield\.venv\Scripts\python -m openyield --output outputs/annotated --seed 7
..\openyield\.venv\Scripts\python -m mkdocs build --strict
git diff --check
```

Observed: **7 Node tests and 32 Python tests passed**. Default demonstration
success remained **73 accepted steps / 18.25 s**, with 74 recorded frames. Strict
documentation build passed; no whitespace errors. Node checks cover paused start,
elapsed catch-up, fractional progress, speed changes, pause/resume, scrub/restart,
terminal behavior, captions/fallback, custom IDs and mobile label font sizing.

Before changing the exporter, generated `outputs/before-replay/` with seed 7.
Compared the resulting `trace.json` and `summary.json` to `outputs/annotated/`:
both were exactly byte-identical. Python regression tests retain these baseline
digests while normalizing platform line endings. Output escaping tests cover
IDs containing closing script tags.

Built a wheel using:

```powershell
..\openyield\.venv\Scripts\python -m pip wheel . --no-deps -w dist
python -m venv .venv-wheel
.\.venv-wheel\Scripts\python -m pip install --no-index --force-reinstall dist/openyield-0.1.0-py3-none-any.whl
```

Then ran the installed package from the parent directory:

```powershell
.\openyield-revert\.venv-wheel\Scripts\python -m openyield --output openyield-revert/outputs/wheel-smoke --seed 7
```

Installed-wheel demo succeeded. The HTML embeds the packaged CSS/JavaScript;
trace and summary were byte-identical to the pre-upgrade outputs. No runtime
dependencies were added. Node is used only for development tests and CI.

Independent source review found mobile label sizing, custom-ID captions and
screen-reader status churn issues; these were corrected and re-reviewed. The
reviewer found no remaining blocking source defect. A final generic canvas
accessibility label also removes the assumption that IDs are always A/B.

## Outstanding visual verification

**This upgraded replay has not been visually inspected, and no video was recorded.**
An earlier local-file browser preview was rejected by browser security policy,
with an explicit prohibition on workarounds through localhost or other browser
surfaces. No workaround was attempted for this upgrade. Automated and source
checks do not establish that the final layout is free of clipping or overlap.

Owner-operated inspection is needed before treating the recording view as ready
for public use: open `outputs/annotated/replay.html`, check desktop and mobile
layouts, play/pause/restart/scrub/speed, wait/pass/lateral/final stages and the
full 16:9 composition. Ensure the caveat stays visible throughout. Capture a
short recording with an existing recorder only after that check. Nothing has
been deployed, published or release-tagged, and later research work is separate.

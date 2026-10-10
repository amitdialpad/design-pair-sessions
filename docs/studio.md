# Studio controls and releases

Reference for the current Studio template, checked 10 October 2026. Existing prototypes may retain an earlier shell and pinned dependencies. For the build workflow, use [Build a prototype](/prototyping).

## The current Studio shell

The shared shell merged in [Design PR #190](https://github.com/dialpad/design/pull/190). It keeps the prototype visible while you inspect or adjust it:

- A centered toolbar opens **About** on the left or **Settings** on the right.
- The inspectors use Dialtone's resizable panels and bring the canvas inward. Closing the inspector restores the full-width canvas.
- Only one inspector is open at a time. `Shift+S` toggles Settings outside editable controls; Escape closes the active inspector. `?settings=open` opens Settings when sharing a URL.
- Appearance controls include light, dark, and system mode, text size, density, material, color theme, and high contrast. Use these to stress-test the idea.
- About reads the prototype's title, description, status, purpose, author, Dialtone version, and tags.

Josh's earlier preview described a toolbar that hides or minimizes with pointer position. The merged shell is the reference for current behavior. Existing prototypes do not all acquire it automatically.

**Versioning:** [Design PR #189](https://github.com/dialpad/design/pull/189) added versioned studio-kit releases. New Vue prototypes choose an exact released version, using the latest approved registry release by default. Existing prototypes stay on their pinned version until explicitly upgraded. The shared-shell package still has release and migration checkpoints, so a merged template change does not by itself prove the latest shell is available in every prototype.

## Announced work to watch

These are Josh's announced directions, **not a promise that they are ready to use**:

| Item | Status checked 10 October |
|---|---|
| `design-spec` for evidence-based build plans | Announced; no skill under this name in the current repository inventory |
| Settings in picture-in-picture | The shell has an optional hook, hidden unless a working callback is supplied; general availability is not established |
| A Prompt area for copying a prototype's starting prompt | Announced; not verified in the merged shell |
| Commenting package inspired by Amit's review workflow | Callout API foundations have merged; a usable Studio commenting experience is not established by those changes |
| Reusable settings template library | Announced; not verified as available |

About, resizable inspectors, appearance controls, and versioning have moved beyond that earlier announcement. Use the current repository and `skill-search` to check availability before planning around the remaining items.

Josh credits Josh Everhart's groundwork for enabling these additions. Bring questions and suggestions back to the team with a concrete example of what you wanted to test and what got in the way.


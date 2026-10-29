# Dependencies · skill-pack-marketplace

Prefer **zero runtime deps**. Site is static HTML/CSS/JS.

| name | role | license | notes |
| --- | --- | --- | --- |
| *(none)* | browser runtime | — | No npm packages shipped under `build/` |
| Python 3 | test runner | PSF License | stdlib only (`json`, `re`, `pathlib`, …) |
| Node.js *(optional)* | local static server | MIT | Not required for tests; `python3 -m http.server` also fine |

## Pack licenses (catalog contents, not site deps)

| pack id | upstream license | source |
| --- | --- | --- |
| impeccable | Apache-2.0 | GitHub API / repo |
| taste-skill | MIT | GitHub API / repo |
| hallmark | MIT | GitHub API / repo |
| motionsites-web-builder | MIT (skill text; examples/media excluded per LICENSE) | repo LICENSE |
| ai-design-skills | MIT | GitHub API / repo |
| ui-ux-pro-max | MIT | repo LICENSE |
| design-taste | MIT | GitHub API / repo |
| agent-design-taste | MIT | GitHub API / repo |

No proprietary libraries. Original site code only under `build/`.

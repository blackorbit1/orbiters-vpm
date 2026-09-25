# Orbiters VPM

The package listing and creator management are moving to **[Orbiters VPM](https://orbiters.cc/vpm/orbiters)**. Creators manage their repositories, release webhooks, package versions and GitHub builds in [Creator → VPM](https://orbiters.cc/creator?tab=vpm).

The GitHub repository URL cannot issue an external HTTP redirect. This page points to its replacement; the GitHub Pages landing page redirects automatically once the hosted catalog passes the migration safety gate.

## Existing Creator Companion installations

The existing `https://blackorbit1.github.io/orbiters-vpm/index.json` address remains a working JSON catalog. Once Orbiters is ready, it mirrors `https://orbiters.cc/vpm/orbiters/index.json`. New installations should use the Orbiters address after the handover. Release ZIP download addresses and SHA-256 hashes are preserved.

## Safe handover

The **Build Repo Listing** action checks the Orbiters feed on manual runs, source changes, and hourly. Before the first handover it requires every currently published package version, URL and checksum to match. If Orbiters is unavailable or not ready, the existing GitHub-based listing build continues. After handover, creator visibility/removal settings are mirrored as well.

To complete the handover, deploy the Orbiters VPM feature, import the reviewed `source.json` and published `index.json` into the owner's listing, verify `/vpm/orbiters/index.json`, then run **Build Repo Listing**. No empty or partial catalog is deployed by the migration step.

`source.json`, the original website templates, and existing release artifacts are kept for the staged migration. The migration workflow never deletes release ZIPs or changes their checksums.

## Validation

```sh
python -m unittest discover -s scripts -p 'test_*.py'
```

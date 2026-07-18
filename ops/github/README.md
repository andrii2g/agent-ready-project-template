# GitHub Settings as Code

`main-ruleset.json` is an example repository ruleset and `labels.yml` is the
label catalog used by `scripts/configure_github.py`. The script performs a
read-only preview unless `--apply` is provided.

Review plan availability, status-check names, bypass actors, merge methods, and
default-branch behavior before applying these settings. Repository settings are
not assumed to be copied automatically when a GitHub template is used.

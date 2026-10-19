# ClockOff for Hermes

One standard Agent Plugin with eight shared skills and the ClockOff MCP address.
No Python executable, custom hook, keyword router or separate runtime is installed.

## Install and connect

Use Plugins → Install from Git in the intended gym profile:
https://github.com/vjbuildsnz/clockoff-hermes-plugin

Or use `hermes -p <gym> plugins install vjbuildsnz/clockoff-hermes-plugin --enable`.
The host loads root plugin.json, skills and mcp.json through its normal portable
plugin support. A hosted provider needs to expose supported Git installation.

Enable Hermes's built-in Skills support for that profile. This is how Hermes
finds and reads plugin instructions. A restricted profile that disables all
skill tools also disables its normal skill discovery and configured preloads.
ClockOff does not bypass that restriction or enable terminal/browser tools.
The built-in Skills toolset includes local skill management; plugin-provided
skills themselves are read-only. ClockOff staff verify the intended host policy.

Then complete ClockOff gym sign-in through the profile's connector. Installation
never signs you in or starts updates. An existing configured `clockoff` connector
wins over the package entry; reuse its grant rather than creating a duplicate.
Never put a key in this repository, an installation link or chat.

Ask **Who am I connected as in ClockOff?**, **What needs my attention today?**,
and **Show my full morning brief**. Check the gym, dates, coverage and full report.
The shared skills guide finished-report presentation; no Python code replaces
the model's answer. Proactive updates need separate host support and opt-in.

## Upgrade a previously customized setup

Staff retain a private rollback copy and update this same Git plugin. Confirm
old plugin.yaml, __init__.py, delivery.py and OWNER_RULES.md are absent from the
installed package; otherwise an older native manifest can take precedence.
Remove the former clockoff-hermes-runtime through plugin management if present.
Enable normal Skills support and preload the registered core ClockOff skill
using its actual qualified name where the managed profile requires it.
Preserve credentials, model, personality and schedules. Start a fresh session
or use the host's supported reload, then run identity and report acceptance.

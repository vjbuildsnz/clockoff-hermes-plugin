# ClockOff for Hermes

One plugin for your gym's ClockOff workflows. It contains eight shared skills and
the report-handling code previously installed as a separate runtime plugin.
It adds no tools, provider credentials, model provider, schedules or permissions.

## Install

In Hermes Desktop, use **Plugins → Install from Git** with this repository's URL,
then enable **ClockOff** in the intended gym profile. On a hosted Hermes instance,
use its plugin manager or `hermes -p <gym-profile> plugins install <repository> --enable`.
Git installation and update are supported Hermes features; a particular cloud
service may restrict plugin installation. Check its actual controls.

## Connect your gym

Plugin installation does not sign in to ClockOff. In the same profile's
**Connectors**, add a Streamable HTTP server named `clockoff` at
`https://clockoff-preview.appwrite.network/mcp`, then complete ClockOff sign-in.
Use the dedicated client configuration supplied for that gym/host where required.
For a managed setup, staff place that installation's scoped key directly in secure
connector settings. Never put a key in this repository, an installation link or chat.

Already connected? Reuse the existing `clockoff` connector, credentials and schedules.
Do not add a second server. Ask **Who am I connected as in ClockOff?**, then
**What needs my attention today?** Confirm the gym and dated evidence.

## Update an existing two-component installation

Staff back up the existing plugin folders, replace `clockoff` with this package,
and disable the old `clockoff-hermes-runtime` using the profile's plugin manager.
Keep that old folder for rollback. Enable ClockOff, run Plugin Doctor, and start
a fresh session or use the supported gateway reload. Do not change authentication,
personality files, schedules or model settings. Confirm one ClockOff entry is enabled.

## What the small Hermes-specific part does

It loads a relevant shared workflow for restricted gym profiles and preserves
successfully returned ClockOff briefings/attendance reports. An interrupted turn
cannot overwrite the owner's new question with an older report. Business rules,
gym access and data definitions remain on the ClockOff server.

These callbacks are Hermes hooks, not MCP Events subscriptions. Installing the
plugin does not enable alerts. Test updates separately in the intended host.

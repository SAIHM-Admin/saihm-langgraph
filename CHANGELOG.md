# Changelog

## 0.1.4

- Require `saihm-adapters` 0.1.3 or later. With `mcp` 2.x installed, 0.1.2 passed a call the
  service refused off as a success; 0.1.3 raises it. 0.1.3 also reports an unfinished
  free-join at start-up with `SaihmNoIdentityError`, raises `SaihmStartupError` for every
  start-up failure, and bundles sidecar dependencies with no known vulnerabilities.
- The README follows the `@saihm/mcp-server-pro` README: start free, add SAIHM to your app,
  what it costs (with the [pricing page](https://saihm.net/pricing)) and support. It now
  shows a runnable LangGraph graph (`graph.compile(store=SaihmStore())`).
- Package links add Issues and Changelog.

## 0.1.3

- Require `saihm-adapters` 0.1.2 or later, which raises a clear `SaihmNoIdentityError` when
  live mode has no identity and bundles the current SAIHM client.
- Links point to https://saihm.net, this repository, the saihm-adapters repository and
  https://saihm-admin.github.io/saihm-demos/. The README says how to go live.
- This repository now holds the forwarding package itself. The earlier adapter code stays in
  its history and lives on in saihm-adapters.

## 0.1.2

`saihm-langgraph` moved into the consolidated `saihm-adapters` package. Installing it pulls
`saihm-adapters[langgraph]`; import from `saihm_adapters` (was `saihm_memory`).

## 0.1.1

- `SaihmStore` imports LangGraph's private filter helpers when they are available and falls back
  to vendored copies from langgraph-checkpoint 4.2.0 when they are not, with a `RuntimeWarning`
  when the fallback is used.
- Tests for the fallback path and for parity with `InMemoryStore` (16 to 62 tests).
- Added `THIRD-PARTY-NOTICES.md` for the vendored helpers (MIT, LangChain, Inc.).

## 0.1.0

First release. `SaihmStore`, a `langgraph.store.base.BaseStore` whose items live in SAIHM: sealed
client-side, portable across models, and provably erasable — `delete()` crypto-shreds the cell
(GDPR Art. 17). Cryptography runs in a bundled Node MCP sidecar.

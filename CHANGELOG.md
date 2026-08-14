# Changelog

## 0.1.1

Hardening only — no API change, no behaviour change on a normal install.

- **Removed a hard dependency on three private LangGraph symbols.** `SaihmStore` reuses LangGraph's
  own `_compare_values` / `_does_match` (and, transitively, `_apply_operator`) so `filter=` and
  `list_namespaces(prefix=/suffix=)` behave exactly as the reference `InMemoryStore` does. Those
  symbols are private and live in `langgraph.store.memory`, shipped by the **langgraph-checkpoint**
  distribution — which this package pins nowhere. `langgraph>=1.2,<2` transitively admits
  `langgraph-checkpoint>=4.1.0,<5.0.0`, so any 4.x release could rename or drop an underscore symbol
  with no semver signal and break `import saihm_memory` outright.

  The import now lives in `saihm_memory/_lg_filter.py` behind a `try` / `except ImportError`, with a
  verbatim vendored copy as the fallback. Upstream is still preferred whenever it is importable, so
  parity is exact by construction on every install where it exists.

  Not a fix for a live break: all five live langgraph-checkpoint 4.x releases (4.0.0, 4.0.3, 4.1.0,
  4.1.1, 4.2.0) define all three symbols, and both ends of the `langgraph>=1.2,<2` band import
  cleanly. This closes the exposure before it can land on a user.

- **The fallback warns when it engages.** A silent fallback would be the wrong trade: the copies match
  4.2.0 exactly, so a *removed* symbol is handled correctly, but a symbol whose *semantics changed*
  would leave `SaihmStore` on 4.2.0 behaviour while `InMemoryStore` moved on. That divergence is now
  a `RuntimeWarning` rather than something you discover from wrong query results.

- **Tests: 16 → 62.** The new cases force the fallback branch to execute (the upstream import is made
  to raise, not stubbed) and then assert the vendored copies agree with upstream across a filter
  matrix (`$eq/$ne/$gt/$gte/$lt/$lte`, multi-operator, nested dicts, lists, type mismatches, unknown
  operator) and a namespace matrix (prefix/suffix, wildcards, over-long paths, unknown match type),
  plus a full `SaihmStore` ⇄ `InMemoryStore` parity check while the fallback is live. Filter
  assertions straddle an actual stored value (`$gt: 10` where a score *is* 10), because a filter that
  returns the same set under `>` and `>=` cannot detect an off-by-one comparator.

  Verified by mutation, not just by passing: breaking the vendored comparator, breaking wildcard
  matching, letting the fallback fail to bind, removing the warning, and restoring the patched
  modules in the wrong order each fail the suite.

- The equivalence tests skip rather than error if a future langgraph really has dropped these
  symbols — otherwise the fallback's own test file would fail to collect in exactly the scenario the
  fallback exists for.

- Added `THIRD-PARTY-NOTICES.md` (the vendored helpers are MIT, © LangChain, Inc.).

## 0.1.0

First release. `SaihmStore`, a `langgraph.store.base.BaseStore` whose items live in SAIHM: sealed
client-side, portable across models, and provably erasable — `delete()` crypto-shreds the cell
(GDPR Art. 17). Cryptography runs in a bundled Node MCP sidecar; Python holds no key.

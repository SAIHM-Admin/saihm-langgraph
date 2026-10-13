# saihm-langgraph

**`saihm-langgraph` has moved. It is now the LangGraph adapter inside the consolidated [`saihm-adapters`](https://pypi.org/project/saihm-adapters/) package** — the same `BaseStore` that gives a LangGraph app long-term memory the user owns: portable across models *and* frameworks, sealed client-side (with the key file, Python never reads your key), and provably erasable (GDPR Art. 17).

Installing `saihm-langgraph` now pulls `saihm-adapters[langgraph]`. This package ships no code of its own.

## Migration — one line

The import root changed from `saihm_memory` to `saihm_adapters`:

```python
from saihm_adapters import SaihmStore          # was: from saihm_memory import SaihmStore
```

`SaihmMemoryClient`, `Memory`, `SaihmTimeout`, and the start-up errors `SaihmStartupError` / `SaihmNoIdentityError` come from `saihm_adapters`:

```python
from saihm_adapters import SaihmMemoryClient, Memory, SaihmTimeout, SaihmNoIdentityError
```

To keep memories beyond one process, create an identity once with `npx -y @saihm/mcp-server-pro free-join` and set `SAIHM_ENDPOINT_URL=https://saihm.net/mcp`; the [saihm-adapters README](https://github.com/SAIHM-Admin/saihm-adapters#go-live) has the details. Without it, the client uses a local sandbox whose memory ends with the process.

This is a clean break: after upgrading, `import saihm_memory` will fail with `ModuleNotFoundError`. That is intentional: the old import root is gone, so the one change to make is obvious.

## Install

```bash
pip install saihm-langgraph        # -> installs saihm-adapters[langgraph]; also needs Node.js >= 20 on PATH
```

or depend on the consolidated package directly:

```bash
pip install "saihm-adapters[langgraph]"
```

`SaihmStore` remains a drop-in `langgraph.store.base.BaseStore` — `get` / `put` / `search` / `delete` / `list_namespaces`, sync and async. Everything else about the adapter is unchanged; only the package that carries it and its import root have consolidated.

## Related

- **Consolidated package:** <https://pypi.org/project/saihm-adapters/>
- **Source and getting started (including how to go live):** <https://github.com/SAIHM-Admin/saihm-adapters>
- **Demos:** <https://saihm-admin.github.io/saihm-demos/>
- **What SAIHM is:** <https://saihm.net>

## License

Apache-2.0.

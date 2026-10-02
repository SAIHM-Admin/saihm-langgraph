# saihm-langgraph

**SAIHM long-term memory for LangGraph — a `BaseStore` your graph owns. Portable, encrypted, provably erasable.**

<a href="https://saihm.net/overview"><img src="https://saihm.net/media/saihm-short-overview-play.jpg" alt="Watch: SAIHM in 6 minutes" width="480"></a>

**New to SAIHM?** [Watch the 6-minute overview](https://saihm.net/overview) (captions and transcript), or [read the SAIHM manual (PDF)](https://saihm.net/manual).

`SaihmStore` is a drop-in [`langgraph.store.base.BaseStore`](https://langchain-ai.github.io/langgraph/) — the interface LangGraph uses for long-term, cross-thread memory. Compile a graph with it and that graph gets memory the user actually owns: portable across models *and* frameworks, non-custodial (sealed client-side; Python never holds a key), and **provably erasable** (GDPR Art. 17 — `delete` crypto-shreds the cell, it does not merely hide it).

```bash
pip install saihm-langgraph      # also needs Node.js >= 20 on PATH (see "How it works")
```

```python
from typing import TypedDict
from langgraph.graph import StateGraph
from langgraph.store.base import BaseStore
from saihm_memory import SaihmStore

class State(TypedDict):
    user: str
    profile: dict

def node(state, *, store: BaseStore):        # LangGraph injects the compiled store
    store.put(("users", state["user"]), "profile", {"name": "Dana"})
    return {"profile": store.get(("users", state["user"]), "profile").value}

builder = StateGraph(State)
builder.add_node("remember", node)
builder.set_entry_point("remember")

graph = builder.compile(store=SaihmStore())  # sandbox by default — no account, offline
print(graph.invoke({"user": "u1"})["profile"])   # -> {'name': 'Dana'}
```

`SaihmStore` implements the full `BaseStore` surface — `get` / `put` / `search` / `delete` /
`list_namespaces`, sync **and** async — on top of `batch` / `abatch`. Each `(namespace, key)` is
one encrypted SAIHM cell.

## Why not just the built-in store?

An in-process store is only as portable as the process it runs in, and only as private as
whoever holds it. SAIHM changes the ownership model — same three lines of `BaseStore`, a
fundamentally different guarantee about *who owns the memory*:

- **Yours across every model.** The same memory opens under Claude, GPT, DeepSeek, Qwen, Kimi,
  or GLM — and under the LangChain, CrewAI, and AutoGen adapters. Switch models or frameworks and
  the agent's memory follows it. No migration, no re-embedding, no vendor lock-in.
- **The store is blind.** Every cell is sealed client-side with post-quantum cryptography
  (ML-DSA-65 / ML-KEM-768 / AES-256-GCM) before it ever leaves your process. The endpoint holds
  ciphertext it cannot read; Python never holds a key.
- **Erasure you can prove.** `delete` destroys the cell's key, so its ciphertext becomes
  unrecoverable noise — a cryptographic shred, not a soft-delete. That is GDPR Art. 17 built into
  `store.delete(...)`. On the hosted tier each shred is recorded in SAIHM's audit chain; in the
  offline sandbox the identical code path runs locally, with no external record.
- **Free to start, offline in seconds.** Runs against a local blind sandbox with no account and
  no network; point it at the hosted free tier when you're ready to persist.

Give your graph long-term memory your users actually own — portable, private, and provably
forgettable — without leaving the `BaseStore` interface you already use.

## How it works

All cryptography runs in a small **Node sidecar** (built on [`@saihm/mcp-server-pro`](https://www.npmjs.com/package/@saihm/mcp-server-pro), ML-DSA-65 / ML-KEM-768 / AES-256-GCM); Python drives it over [MCP](https://modelcontextprotocol.io) stdio and holds no keys — one audited crypto implementation, not a second one ported to Python. That is why **Node.js ≥ 20 is required**. The sidecar ships inside the wheel as source only; its Node dependencies are installed once into a per-user cache (`~/.cache/saihm-langgraph`) on first use, then reused offline.

- **Sandbox (default):** no configuration → a local, in-process *blind* endpoint (ciphertext only). Great for trying it with zero signup; memory lasts for the client's life.
- **Live:** set `SAIHM_ENDPOINT_URL` + `SAIHM_MASTER_SECRET_HEX` and either `SAIHM_TIER=FREE` (free tier — run `npx -y @saihm/mcp-server-pro free-join` once) or `SAIHM_AUTH_HEADER` (Pro; join at <https://saihm.coti.global/join>) → durable, hosted, blind memory.

Always `close()` the store (or use the client as a context manager); a dropped client is reaped on GC, but explicit close is cleaner.

## Parity with `InMemoryStore`

Filter (`$`-operators) and namespace matching reuse LangGraph's own helpers, so results match the reference `InMemoryStore` exactly. Two documented differences, both from SAIHM being a *blind* store (the endpoint holds ciphertext only and cannot run a server-side vector index):

- `search` returns matches **newest-first** with `score=None` (no semantic ranking), where `InMemoryStore` returns insertion order.
- `supports_ttl` is `False`.

A cell written outside this adapter (e.g. by the LangChain, CrewAI, or AutoGen SAIHM adapters, or a raw `remember`) is left untouched — one owned store can hold facts from several adapters without collision.

## Related

- **Try it in your browser (offline, no signup):** <https://citw2.github.io/saihm-demos/>
- **Runnable end-to-end demo:** <https://github.com/citw2/saihm-langgraph>
- **Other adapters:** [LangChain/LlamaIndex](https://github.com/citw2/saihm-langchain) · [CrewAI](https://github.com/citw2/saihm-crewai) · [AutoGen](https://github.com/citw2/saihm-autogen)
- **What SAIHM is:** <https://saihm.coti.global>

## License

Apache-2.0.

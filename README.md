# saihm-langgraph — memory for LangGraph agents

**Portable memory for LangGraph agents.** A LangGraph `BaseStore` whose memories are
encrypted on your machine, follow your user across models and frameworks, and can be
erased for good.

**`saihm-langgraph` is now the LangGraph adapter inside the consolidated
[`saihm-adapters`](https://pypi.org/project/saihm-adapters/) package.** Installing it pulls
`saihm-adapters[langgraph]`. This package ships no code of its own.

**New to SAIHM?** [Watch the 6-minute overview](https://saihm.net/overview) (captions and transcript).
**Prefer to read?** [The SAIHM manual](https://saihm.net/manual) (PDF) is a decision-maker's guide to SAIHM.

**Encrypted at rest, by default.** Every memory is encrypted on your own machine before it
goes anywhere, and SAIHM stores only that ciphertext. Nobody else can read your memories —
not the storage, not SAIHM. With your key in a key file, Python never reads the key.

## Start free — one command

```sh
npx -y @saihm/mcp-server-pro free-join
```

No card and no wallet. The command creates your key on this machine and shows a link and a
short code. Open the link, sign in to GitHub, enter the code and approve; the command then
finishes by itself and shows where your key is saved. If a join is interrupted, join again
on the same machine: it reuses the key it already created. The
[saihm-adapters README](https://github.com/SAIHM-Admin/saihm-adapters#start-free--one-command)
has the details, including how to start without a GitHub account.

## Add SAIHM to your graph

```bash
pip install saihm-langgraph        # -> installs saihm-adapters[langgraph]; also needs Node.js >= 20 on PATH
```

Compile your graph with the store; every node that takes `store` reads and writes SAIHM:

```python
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.store.base import BaseStore

from saihm_adapters import SaihmStore


class State(TypedDict):
    user: str
    answer: str


def remember(state: State, *, store: BaseStore):
    store.put(("users", state["user"]), "drink", {"text": "likes tea"})
    return {}


def recall(state: State, *, store: BaseStore):
    item = store.get(("users", state["user"]), "drink")
    return {"answer": item.value["text"] if item else ""}


graph = StateGraph(State)
graph.add_node("remember", remember)
graph.add_node("recall", recall)
graph.add_edge(START, "remember")
graph.add_edge("remember", "recall")
graph.add_edge("recall", END)

app = graph.compile(store=SaihmStore())
print(app.invoke({"user": "ada", "answer": ""}))  # {'user': 'ada', 'answer': 'likes tea'}
```

With no `SAIHM_ENDPOINT_URL` set, the store uses a local sandbox whose memory ends with the
process, so you can try it with no sign-up. To go live once free-join has finished:

```bash
export SAIHM_ENDPOINT_URL=https://saihm.net/mcp
```

`SaihmStore` is a drop-in `langgraph.store.base.BaseStore` — `get` / `put` / `search` /
`delete` / `list_namespaces`, sync and async. In live mode, `SaihmStore()` raises
`SaihmNoIdentityError` when this machine has no active identity, with the command that
fixes it, and a call the service refuses raises `RuntimeError` with the service's reason.

## Migration — one line

The import root changed from `saihm_memory` to `saihm_adapters`:

```python
from saihm_adapters import SaihmStore          # was: from saihm_memory import SaihmStore
```

`SaihmMemoryClient`, `Memory`, `SaihmTimeout`, and the start-up errors `SaihmStartupError` / `SaihmNoIdentityError` come from `saihm_adapters`:

```python
from saihm_adapters import SaihmMemoryClient, Memory, SaihmTimeout, SaihmNoIdentityError
```

This is a clean break: after upgrading, `import saihm_memory` will fail with `ModuleNotFoundError`. That is intentional: the old import root is gone, so the one change to make is obvious.

## What it costs

Start free. The free tier is a fixed, one-time allowance for trying SAIHM on real
infrastructure — it doesn't reset or refill. **No card, and nothing to cancel.** Paid
plans are monthly; prices are on the [pricing page](https://saihm.net/pricing).
[Upgrading](https://github.com/SAIHM-Admin/saihm-adapters#what-it-costs) keeps the same key
and every memory you already have.

## Support SAIHM

- **Star it on [GitHub](https://github.com/SAIHM-Admin/saihm-adapters).** Stars help other
  developers find SAIHM.
- **Share it** with a colleague, your team, or anyone whose agents keep forgetting.
- **Questions or problems?** See [contact and support](https://saihm.net/contact).

More: the [consolidated package](https://pypi.org/project/saihm-adapters/), its
[source and full guide](https://github.com/SAIHM-Admin/saihm-adapters), the
[demos](https://saihm-admin.github.io/saihm-demos/), and [what SAIHM is](https://saihm.net).

## License

Apache-2.0 © SAIHM

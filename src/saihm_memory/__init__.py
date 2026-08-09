"""SAIHM memory for Python — LangGraph BaseStore (long-term, cross-thread memory).

Long-term memory a LangGraph app owns: portable across models, non-custodial (sealed by a
bundled Node sidecar — Python holds no key), and provably erasable (GDPR Art. 17).

    from saihm_memory import SaihmStore         # langgraph BaseStore, SAIHM-backed
    from saihm_memory import SaihmMemoryClient   # the core client (any Python app)
"""
from .client import Memory, SaihmMemoryClient, SaihmTimeout

__all__ = ["SaihmMemoryClient", "Memory", "SaihmTimeout", "SaihmStore"]


def __getattr__(name: str):
    # Import the adapter lazily so the core client works without langgraph installed.
    if name == "SaihmStore":
        from .langgraph_store import SaihmStore

        return SaihmStore
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

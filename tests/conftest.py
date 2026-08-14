"""Test fixtures. Everything runs against the OFFLINE blind sandbox (no account, no live
endpoint): a fresh SaihmMemoryClient with no SAIHM_ENDPOINT_URL spins up a local in-process
blind endpoint via the bundled Node sidecar.

One sandbox client is shared for the whole session (a Node subprocess spawn is not free); each
test starts from a clean slate via the autouse ``_wipe`` fixture.
"""
from __future__ import annotations

import pytest

from saihm_memory import SaihmMemoryClient, SaihmStore


@pytest.fixture(scope="session")
def client():
    c = SaihmMemoryClient()  # sandbox mode (no env) -> local blind endpoint
    try:
        yield c
    finally:
        c.close()


@pytest.fixture(autouse=True)
def _wipe(client):
    """Erase every cell before each test so the shared sandbox is isolated per-test."""
    for m in client.recall():
        client._forget_raw(m.cell_id)
    yield


@pytest.fixture(autouse=True)
def _no_vendored_leak():
    """No test may leave ``SaihmStore`` bound to the vendored fallback instead of upstream.

    ``test_vendored_filter_fallback`` reloads modules to force the fallback branch. Getting the
    restore order wrong re-binds ``langgraph_store`` to the vendored copies and leaves it there, so
    every later test silently exercises the fallback — which passes, because the copies agree, while
    quietly voiding what the parity suite claims to check. That leak was real; this fails on it.
    """
    yield
    import saihm_memory._lg_filter as f
    import saihm_memory.langgraph_store as s

    if not f.USING_VENDORED:  # normal install: the store must point at LangGraph's own helpers
        assert s._compare_values is f.compare_values, (
            "test leaked a vendored binding into langgraph_store._compare_values "
            f"({s._compare_values.__module__})"
        )
        assert s._does_match is f.does_match, (
            "test leaked a vendored binding into langgraph_store._does_match "
            f"({s._does_match.__module__})"
        )


@pytest.fixture
def saihm(client):
    # client passed in => the store does not own/close it (session fixture handles that).
    return SaihmStore(client=client)


@pytest.fixture
def mem():
    from langgraph.store.memory import InMemoryStore
    return InMemoryStore()

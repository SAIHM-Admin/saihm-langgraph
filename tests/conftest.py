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


@pytest.fixture
def saihm(client):
    # client passed in => the store does not own/close it (session fixture handles that).
    return SaihmStore(client=client)


@pytest.fixture
def mem():
    from langgraph.store.memory import InMemoryStore
    return InMemoryStore()

import asyncio
from typing import Any, Dict
from opal.client.enforcer.schemas import AuthorizationQuery
from opal.common.schemas.policy import PolicyBundle

from .base_policy_store_client import  BasePolicyStoreClient

class MockPolicyStoreClient(BasePolicyStoreClient):
    """
    A naive mock policy and policy-data store for tests
    """

    def __init__(self) -> None:
        super().__init__()
        self._has_data_event:asyncio.Event() = None
        self._data = {}

    @property
    def has_data_event(self):
        if self._has_data_event is None:
            self._has_data_event = asyncio.Event() 
        return self._has_data_event

    async def is_allowed(self, query: AuthorizationQuery):
        return True

    async def set_policy(self, policy_id: str, policy_code: str):
        pass

    async def set_policies(self, bundle: PolicyBundle):
        pass

    async def set_policy_data(self, policy_data: Dict[str, Any], path=""):
        self._data[path] = policy_data
        self.has_data_event.set()
        
    async def get_data(self, path: str=None):
        if path is None:
            return self._data
        else: 
            return self._data[path]

    async def wait_for_data(self):
        """
        Wait until the store has data set in it
        """
        await self.has_data_event.wait()
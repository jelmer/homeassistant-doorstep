"""DataUpdateCoordinator for doorstep."""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import DoorstepAuthError, DoorstepClient, DoorstepError, Parcels, Stats
from .const import DOMAIN, UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

type DoorstepConfigEntry = ConfigEntry[DoorstepCoordinator]


@dataclass(frozen=True)
class DoorstepData:
    """One poll's worth of doorstep state."""

    parcels: Parcels
    stats: Stats


class DoorstepCoordinator(DataUpdateCoordinator[DoorstepData]):
    """Coordinator to fetch parcels and statistics from doorstep."""

    def __init__(
        self, hass: HomeAssistant, entry: DoorstepConfigEntry, client: DoorstepClient
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )
        self.client = client

    async def _async_update_data(self) -> DoorstepData:
        try:
            parcels, stats = await asyncio.gather(
                self.client.parcels(), self.client.stats()
            )
        except DoorstepAuthError as err:
            raise ConfigEntryAuthFailed(str(err)) from err
        except DoorstepError as err:
            raise UpdateFailed(str(err)) from err
        return DoorstepData(parcels=parcels, stats=stats)

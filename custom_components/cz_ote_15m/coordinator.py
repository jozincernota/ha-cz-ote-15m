import aiohttp
import async_timeout
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import API_URL, UPDATE_INTERVAL

class CZOTE15MCoordinator(DataUpdateCoordinator):
    def __init__(self, hass):
        super().__init__(
            hass,
            logger=None,
            name="CZ OTE 15min Spot",
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self):
        try:
            async with aiohttp.ClientSession() as session:
                with async_timeout.timeout(10):
                    async with session.get(API_URL) as response:
                        return await response.json()
        except Exception as err:
            raise UpdateFailed(f"Error fetching OTE data: {err}")
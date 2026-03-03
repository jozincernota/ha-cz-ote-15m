from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util
from .coordinator import CZOTE15MCoordinator
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = CZOTE15MCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([CZOTE15MSensor(coordinator, entry.data)])

class CZOTE15MSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, config):
        super().__init__(coordinator)
        self._config = config
        self._attr_name = "CZ OTE Aktuální 15min Cena"
        self._attr_unique_id = "cz_ote_15m_current_price"
        self._attr_unit_of_measurement = self._config.get("unit", "CZK/MWh")

    @property
    def state(self):
        data = self.coordinator.data
        now = dt_util.utcnow()
        price = None

        for item in data.get("today", []):
            start = dt_util.parse_datetime(item["valid_from"])
            end = dt_util.parse_datetime(item["valid_to"])
            if start <= now < end:
                price = item["priceCZK"]
                break

        if price is None:
            return None

        if self._attr_unit_of_measurement == "CZK/kWh":
            price /= 1000

        return round(price, 2)

    @property
    def extra_state_attributes(self):
        attributes = {}
        data = self.coordinator.data
        today = data.get("today", [])
        tomorrow = data.get("tomorrow", [])

        attributes["today"] = today
        if self._config.get("show_tomorrow", True):
            attributes["tomorrow"] = tomorrow

        if self._config.get("show_statistics", True):
            prices = [x["priceCZK"] for x in today]
            if self._attr_unit_of_measurement == "CZK/kWh":
                prices = [p / 1000 for p in prices]

            attributes["min_today"] = round(min(prices), 2) if prices else None
            attributes["max_today"] = round(max(prices), 2) if prices else None
            attributes["avg_today"] = round(sum(prices)/len(prices), 2) if prices else None

            # Nejlevnější 2 hodiny (8 intervalů)
            min_block = None
            min_sum = float("inf")
            for i in range(len(prices) - 7):
                block_sum = sum(prices[i:i+8])
                if block_sum < min_sum:
                    min_sum = block_sum
                    min_block = {"start_index": i, "end_index": i+7, "avg_price": round(block_sum/8,2)}
            attributes["cheapest_2h_block"] = min_block

        return attributes
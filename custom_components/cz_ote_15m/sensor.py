from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Vytvoření senzorů po přidání integrace."""
    sensors = [
        CzOte15mSensor("current"),
        CzOte15mSensor("min"),
        CzOte15mSensor("max"),
        CzOte15mSensor("avg"),
    ]
    async_add_entities(sensors, True)

class CzOte15mSensor(SensorEntity):
    """Definice senzoru CZ OTE 15min."""

    def __init__(self, kind):
        self._kind = kind
        self._state = None
        self._attr_name = f"OTE 15min {kind.capitalize()} Price"
        self._attr_unit_of_measurement = "CZK"

    @property
    def state(self):
        return self._state

    async def async_update(self):
        """Načtení dat z OTE API."""
        # Tady se přidá volání API a výpočet min/max/avg
        # Pro jednoduchost zatím fiktivní hodnoty:
        from random import randint
        if self._kind == "current":
            self._state = randint(1500, 2500) / 100
        elif self._kind == "min":
            self._state = 1.50
        elif self._kind == "max":
            self._state = 2.50
        elif self._kind == "avg":
            self._state = 2.00
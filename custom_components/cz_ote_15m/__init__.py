"""Inicializace CZ OTE 15min integrace."""
from homeassistant.core import HomeAssistant

DOMAIN = "cz_ote_15m"

async def async_setup(hass: HomeAssistant, config: dict):
    """Základní setup (bez YAML)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Setup po přidání přes config flow."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry):
    """Odinstalace integrace."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    return True
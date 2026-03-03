from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class CZOTE15MFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="CZ OTE 15min Spot", data=user_input)

        schema = vol.Schema({
            vol.Optional("unit", default="CZK/MWh"): vol.In(["CZK/MWh", "CZK/kWh"]),
            vol.Optional("show_tomorrow", default=True): bool,
            vol.Optional("show_statistics", default=True): bool
        })
        return self.async_show_form(step_id="user", data_schema=schema)
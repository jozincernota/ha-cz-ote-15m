import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, DEFAULT_CURRENCY

class CzOte15mFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow pro CZ OTE 15min."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="CZ OTE 15min", data=user_input)

        schema = vol.Schema({
            vol.Optional("currency", default=DEFAULT_CURRENCY): vol.In(["CZK", "EUR"]),
            vol.Optional("include_future_prices", default=True): bool,
            vol.Optional("round_digits", default=2): int,
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
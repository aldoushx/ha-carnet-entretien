"""Config flow : demande une clé Gemini optionnelle, comme ha-millesime."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import CONF_GEMINI_API_KEY, DOMAIN


class CarnetEntretienConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None):
        if user_input is not None:
            return self.async_create_entry(title="Carnet d'entretien", data=user_input)

        schema = vol.Schema({vol.Optional(CONF_GEMINI_API_KEY, default=""): str})
        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            description_placeholders={
                "info": "Clé gratuite sur aistudio.google.com. Laissez vide pour "
                        "utiliser l'intégration en mode manuel (sans génération IA)."
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return CarnetEntretienOptionsFlow(config_entry)


class CarnetEntretienOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict | None = None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_key = self.config_entry.options.get(
            CONF_GEMINI_API_KEY, self.config_entry.data.get(CONF_GEMINI_API_KEY, "")
        )
        schema = vol.Schema({vol.Optional(CONF_GEMINI_API_KEY, default=current_key): str})
        return self.async_show_form(step_id="init", data_schema=schema)

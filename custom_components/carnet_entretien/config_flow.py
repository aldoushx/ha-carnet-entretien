"""Config flow : clé Gemini optionnelle + langue de l'intégration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import CONF_GEMINI_API_KEY, CONF_LANGUAGE, DOMAIN

# Choix proposé pour la langue de contenu de l'intégration (carte, noms
# d'opérations du catalogue, texte généré par Gemini, notifications — voir
# catalog_i18n.py). Décidée une fois à l'installation, au même endroit que
# la clé API : contrairement à un thème visuel, il n'y a pas de raison de
# changer de langue au jour le jour, donc ce n'est plus un réglage de la
# carte (v1.4.0) mais un réglage d'installation de l'intégration (v1.4.1),
# modifiable ensuite via Options si besoin (au même titre que la clé API).
LANGUAGE_OPTIONS = [
    selector.SelectOptionDict(value="fr", label="Français 🇫🇷"),
    selector.SelectOptionDict(value="en", label="English 🇬🇧"),
    selector.SelectOptionDict(value="de", label="Deutsch 🇩🇪"),
    selector.SelectOptionDict(value="es", label="Español 🇪🇸"),
    selector.SelectOptionDict(value="it", label="Italiano 🇮🇹"),
]


def _language_field() -> selector.SelectSelector:
    return selector.SelectSelector(
        selector.SelectSelectorConfig(options=LANGUAGE_OPTIONS, mode=selector.SelectSelectorMode.DROPDOWN)
    )


class CarnetEntretienConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict | None = None):
        # Intégration conçue comme un singleton : le stockage
        # (STORAGE_KEY dans const.py) est une clé globale unique, partagée
        # par tout HA, pas par config entry — comme le réglage "language"
        # (voir CONF_LANGUAGE). Une deuxième entrée créerait une deuxième
        # instance CarnetStore chargeant/réécrivant le MÊME fichier
        # .storage/carnet_entretien_data de façon indépendante, avec un
        # risque réel d'écrasement complet des véhicules de la première
        # entrée au premier `async_save()` de la seconde (vécu en
        # production : ajout d'un véhicule depuis une 2e entrée -> perte
        # de tous les véhicules de la 1re). "single_config_entry" dans
        # manifest.json bloque déjà le bouton "Ajouter une entrée" dans
        # l'UI sur les versions de HA qui le supportent ; cet abort est une
        # deuxième barrière explicite, y compris si ce flow est déclenché
        # autrement (ex. import, ancienne version de HA).
        self._async_abort_entries_match()
        if user_input is not None:
            return self.async_create_entry(title="Carnet d'entretien", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional(CONF_GEMINI_API_KEY, default=""): str,
                vol.Optional(CONF_LANGUAGE, default="fr"): _language_field(),
            }
        )
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
        return CarnetEntretienOptionsFlow()


class CarnetEntretienOptionsFlow(config_entries.OptionsFlow):
    """Depuis une version récente de Home Assistant, `config_entry` est une
    propriété en lecture seule sur `OptionsFlow`, assignée automatiquement
    par le framework — un `__init__` qui l'assigne manuellement (pattern
    historiquement standard, utilisé par de très nombreuses intégrations)
    lève désormais AttributeError. On ne définit donc plus `__init__` du
    tout ; `self.config_entry` reste accessible normalement, hérité."""

    async def async_step_init(self, user_input: dict | None = None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_key = self.config_entry.options.get(
            CONF_GEMINI_API_KEY, self.config_entry.data.get(CONF_GEMINI_API_KEY, "")
        )
        current_language = self.config_entry.options.get(
            CONF_LANGUAGE, self.config_entry.data.get(CONF_LANGUAGE, "fr")
        )
        schema = vol.Schema(
            {
                vol.Optional(CONF_GEMINI_API_KEY, default=current_key): str,
                vol.Optional(CONF_LANGUAGE, default=current_language): _language_field(),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)

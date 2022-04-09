"""Support for the Rainforest Automation Energy Monitoring Unit."""

import asyncio
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import (DOMAIN, PLATFORMS)



async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Set up Rainforest EMU-2 entry."""
    hass.config_entries.async_setup_platforms(config_entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload the config entry and platform"""
    hass.data.pop(DOMAIN)

    tasks = {}
    for platform in PLATFORMS:
        tasks.append(
                hass.config_entries.async_forward_entry_unload(config_entry, platform)
        )

    return all(await asyncio.gather(*tasks))

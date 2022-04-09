"""Config flow for Rainforest EMU-2 integration."""
from __future__ import annotations

from typing import Any, Union

import serial.tools.list_ports
from serial.tools.list_ports_common import ListPortInfo
import voluptuous as vol
import os

from homeassistant import config_entries
from homeassistant.components import usb
from homeassistant.const import CONF_PORT, CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import DEFAULT_NAME, DOMAIN

DATA_SCHEMA = vol.Schema({"name": str, "device": str})


def _generate_unique_id(port: Union[ListPortInfo, usb.UsbServiceInfo]) -> str:
    """Generate unique id from usb attributes."""
    return f"{port.vid}:{port.pid}_{port.serial_number}_{port.manufacturer}_{port.description}"


@config_entries.HANDLERS.register(DOMAIN)
class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config Flow."""
    VERSION = 1

    def __init__(self):
        """Initialize flow instance."""
        self._device: str | None = None

    async def async_step_usb(self, discovery_info: usb.UsbServiceInfo) -> FlowResult:
        """Handle usb discovery."""
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")
        if self._async_in_progress():
            return self.async_abort(reason="already_in_progress")

        dev_path = await self.hass.async_executor_job(
            usb.get_serial_by_id, discovery_info.device
        )
        unique_id = self._generate_unique_id(discovery_info)
        if (
                await self.validate_device_errors(
                    dev_path=dev_path, unique_id=unique_id
                )
                is None
        ):
            self._device = dev_path
            return await self.async_step_usb_confirm()
        return await self.async_abort(reason="cannot_connect")

    async def async_step_usb_confirm(
            self,
            user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm usb discovery."""
        if user_input is not None:
            return self.async_create_entry(
                    title=user_input.get(CONF_NAME, DEFAULT_NAME),
                    data={CONF_PORT: self._device},
            )
        self._set_confirm_only()
        return self.async_show_form(step_id="usb_confirm")

    async def async_step_user(
            self,
            user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle config initiated by the user."""
        errors: dict[str, str] | None = {}
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")
        if self._async_in_progress():
            return self.async_abort(reason="already_in_progress")
        ports = await self.hass.async_add_executor_job(
            serial.tools.list_ports.comports
        )
        existing_devices = [
            entry.data[CONF_PORT] for entry in self._async_current_entries()
        ]
        unused_ports = [
            usb.human_readable_device_name(
                port.device,
                port.serial_number,
                port.manufacturer,
                port.description,
                port.vid,
                port.pid,
            )
            for port in ports
            if port.device not in existing_devices
        ]
        if not unused_ports:
            return self.async_abort(reason="no_devices_found")

        if user_input is not None:
            port = ports[unused_ports.index(str(user_input.get(CONF_PORT)))]
            dev_path = await self.hass.async_add_executor_job(
                usb.get_serial_by_id, port.device
            )
            errors = await self.validate_device_errors(
                dev_path=dev_path, unique_id=_generate_unique_id(port)
            )
            if errors is None:
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, DEFAULT_NAME),
                    data={CONF_PORT: dev_path},
                )
        user_input = user_input or {}
        schema = vol.Schema({vol.Required(CONF_PORT): vol.In(unused_ports)})
        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )

    async def validate_device_errors(
            self, dev_path: str, unique_id: str
    ) -> dict[str, str] | None:
        """Handle common flow input validation."""
        self._async_abort_entries_match({CONF_PORT: dev_path})
        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured(updates={CONF_PORT: dev_path})

        try:
            serial.Serial(dev_path, 115200, timeout=1)
        except Exception:
            return {"base": "cannot_connect"}
        else:
            return None


def get_serial_by_id(dev_path: str) -> str:
    """Return a /dev/serial/by-id match for given device if available."""
    by_id = "/dev/serial/by-id"
    if not os.path.isdir(by_id):
        return dev_path

    for path in (entry.path for entry in os.scandir(by_id) if entry.is_symlink()):
        if os.path.realpath(path) == dev_path:
            return path
    return dev_path

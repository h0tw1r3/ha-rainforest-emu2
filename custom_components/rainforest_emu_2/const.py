"""rainforest emu-2 component"""

from __future__ import annotations

import logging

#from typing import Final
#
#from homeassistant.components.sensor import (
#    SensorDeviceClass,
#    SensorEntityDescription,
#    SensorStateClass,
#)
#from homeassistant.helpers.entity import EntityCategory

from homeassistant.const import (
    Platform,
#    POWER_KILO_WATT,
)

DOMAIN = "rainforest_emu_2"
LOGGER = logging.getLogger(__package__)

DEFAULT_NAME = "Rainforest EMU-2"

PLATFORMS = [Platform.SENSOR]

#SENSOR_TYPES: tuple[SensorEntityDescription, ...] = (
#    SensorEntityDescription(
#        key="device_mac_id",
#        name="Device MAC ID",
#        icon="mdi:information-outline"
#    ),
#    SensorEntityDescription(
#        key="meter_mac_id",
#        name="Meter MAC ID",
#        icon="mdi:information-outline",
#    ),
#    SensorEntityDescription(
#        key="tier",
#        name="Tier",
#        icon="mdi:information-outline",
#    ),
#    SensorEntityDescription(
#        key="price",
#        name="Price",
#        icon="mdi:cash",
#    ),
#    SensorEntityDescription(
#        key="summation",
#        name="Summation",
#        icon="mdi:information-outline",
#        native_unit_of_measurement=POWER_KILO_WATT,
#        device_class=SensorDeviceClass.POWER,
#        state_class=SensorStateClass.MEASUREMENT,
#    ),
#    SensorEntityDescription(
#        key="delivered",
#        name="Delivered",
#        icon="mdi:lightning-bolt",
#        native_unit_of_measurement=POWER_KILO_WATT,
#        device_class=SensorDeviceClass.POWER,
#        state_class=SensorStateClass.MEASUREMENT,
#    ),
#    SensorEntityDescription(
#        key="received",
#        name="Received",
#        icon="mdi:lightning-bolt-outline",
#        native_unit_of_measurement=POWER_KILO_WATT,
#        device_class=SensorDeviceClass.POWER,
#        state_class=SensorStateClass.MEASUREMENT,
#    ),
#    SensorEntityDescription(
#        key="custom_price",
#        name="Custom Price",
#        icon="mdi:cash",
#    ),
#)

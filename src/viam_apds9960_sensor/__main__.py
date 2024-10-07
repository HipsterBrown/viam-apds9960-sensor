import asyncio
from typing import (
    Any,
    ClassVar,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
)

from typing_extensions import Self, Tuple
from viam.components.sensor import Sensor
from viam.module.module import Module
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import SensorReading, struct_to_dict

from pydantic import BaseModel, Field

import board
from busio import I2C
from adafruit_apds9960.apds9960 import APDS9960

MAX_COLOR_DATA = 65535
MAX_COLOR_RGB = 255


class SensorConfig(BaseModel):
    color: bool = False
    gesture: bool = False
    proximity: bool = True
    interrupt: bool = False
    interrupt_low_threshold: int = Field(ge=0, le=255, default=0)
    interrupt_high_threshold: int = Field(ge=0, le=255, default=255)
    interrupt_persistence_ms: int = Field(ge=0, le=15, default=1)


class Apds9960(Sensor, EasyResource):
    MODEL: ClassVar[Model] = Model(ModelFamily("hipsterbrown", "sensor"), "apds9960")

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        """This method creates a new instance of this sensor component.
        The default implementation sets the name from the `config` parameter and then calls `reconfigure`.

        Args:
            config (ComponentConfig): The configuration for this resource
            dependencies (Mapping[ResourceName, ResourceBase]): The dependencies (both implicit and explicit)

        Returns:
            Self: The resource
        """
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        """This method allows you to validate the configuration object received from the machine,
        as well as to return any implicit dependencies based on that `config`.

        Args:
            config (ComponentConfig): The configuration for this resource

        Returns:
            Sequence[str]: A list of implicit dependencies
        """
        attrs = struct_to_dict(config.attributes)

        SensorConfig(**attrs)

        return []

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        """This method allows you to dynamically update your service when it receives a new `config` object.

        Args:
            config (ComponentConfig): The new configuration
            dependencies (Mapping[ResourceName, ResourceBase]): Any dependencies (both implicit and explicit)
        """
        self.config = SensorConfig(**struct_to_dict(config.attributes))
        self.sensor = APDS9960(I2C(board.SCL, board.SDA))

        self.sensor.enable_proximity = self.config.proximity
        self.sensor.enable_color = self.config.color
        self.sensor.enable_gesture = self.config.gesture
        self.sensor.enable_proximity_interrupt = self.config.interrupt

        if self.sensor.enable_proximity_interrupt:
            self.sensor.proximity_interrupt_threshold = tuple(
                [
                    self.config.interrupt_low_threshold,
                    self.config.interrupt_high_threshold,
                    self.config.interrupt_persistence_ms,
                ]
            )

    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Mapping[
        str,
        SensorReading,
    ]:
        return {
            "proximity": (
                self.sensor.proximity if self.sensor.enable_proximity else None
            ),
            "color": (
                self._format_color(self.sensor.color_data)
                if self.sensor.enable_color
                else None
            ),
            "gesture": (
                self._format_gesture(self.sensor.gesture())
                if self.sensor.enable_gesture
                else None
            ),
        }

    def _format_color(self, data: Tuple[int, int, int, int]) -> List[int]:
        """Clamp the sensor color data values within a familiar 0-255 RGBA range."""
        return [int((color / MAX_COLOR_DATA) * MAX_COLOR_RGB) for color in data]

    def _format_gesture(
        self, gesture: int
    ) -> Literal["up", "down", "left", "right", "none"]:
        """Evaluate the integer data from the sensor as the string literal direction."""
        if gesture == 0x01:
            return "up"
        if gesture == 0x02:
            return "down"
        if gesture == 0x03:
            return "left"
        if gesture == 0x04:
            return "right"
        return "none"


if __name__ == "__main__":
    asyncio.run(Module.run_from_registry())

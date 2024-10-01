# [`apds9960-sensor` module](https://app.viam.com/module/hipsterbrown/apds9960-sensor)

This [module](https://docs.viam.com/registry/#modular-resources) implements the [`rdk:component:sensor` API](https://docs.viam.com/appendix/apis/components/sensor/) in an `apds9960` model.
With this model, you can read proximity, gesture, and color values from the [APDS9960 sensor](https://learn.adafruit.com/adafruit-apds9960-breakout).

## Requirements

Ensure that [I<sup>2</sup>C communication is enabled](https://docs.viam.com/installation/prepare/rpi-setup/#enable-communication-protocols) on the device connected to the sensor.


## Configure your `apds9960` sensor

Navigate to the [**CONFIGURE** tab](https://docs.viam.com/configure/) of your [machine](https://docs.viam.com/fleet/machines/) in [the Viam app](https://app.viam.com/).
[Add `sensor` / `apds9960` to your machine](https://docs.viam.com/configure/#components).

On the new component panel, copy and paste the following attribute template into your <INSERT API NAME>’s attributes field:

```json
{
    "color": <true|false>,
    "gesture": <true|false>,
    "proximity": <true|false>,
    "interrupt": <true|false>,
    "interrupt_low_threshold": <0-255>,
    "interrupt_high_threshold": <0-255>,
    "interrupt_persistence_ms": <0-15>,
}
```

### Attributes

The following attributes are available for `hipsterbrown:apds9960-sensor:apds9960` sensor:

| Name    | Type   | Required?    | Default | Description |
| ------- | ------ | ------------ | ------- | ----------- |
| `color` | boolean | Optional    | false        | Enable color detection |
| `gesture` | boolean | Optional     | false        | Enable gesture detection  |
| `proximity` | boolean | Optional     | true        | Enable proximity detection  |
| `interrupt` | boolean | Optional     | false        | Enable proximity interrupt  |
| `interrupt_low_threshold` | integer | Optional     | 0        | Configure value to trigger interrupt if proximity drops below  |
| `interrupt_high_threshold` | integer | Optional     | 255        | Configure value to trigger interrupt if proximity rises above  |
| `interrupt_persistence_ms` | integer | Optional     | false        | Configure number of cycles (2.78ms per cycle) to wait before triggering interrupt when threshold is met. Used to prevent false positives.  |

### Example configuration

Default values:

```json
{
    "color": false,
    "gesture": false,
    "proximity": true,
    "interrupt": false,
    "interrupt_low_threshold": 0,
    "interrupt_high_threshold": 255,
    "interrupt_persistence_ms": 1
}
```

Configure a proximity interrupt to trigger when value goes above 175:

```json
{
    "interrupt": true,
    "interrupt_high_threshold": 175
}
```


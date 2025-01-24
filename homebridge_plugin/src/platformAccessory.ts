import type { CharacteristicValue, PlatformAccessory, Service } from 'homebridge';

import type { ChookHutchPlatform } from './platform.js';

import { createRequire } from 'module';
import { Gpio } from 'onoff';
const require = createRequire(import.meta.url);

var GPIO = require('onoff').Gpio;
// GPIO mappings on RPi4: https://github.com/fivdi/onoff/issues/200#issuecomment-2088761700
//gpio-517 (GPIO5 )
//gpio-518 (GPIO6 )
//gpio-519 (GPIO7 )
var doorReedSwitchPin = new GPIO(519, 'in');

var linearActuatorAPin = new GPIO(517, 'out');
var linearActuatorBPin = new GPIO(518, 'out');

/**
 * Platform Accessory
 * An instance of this class is created for each accessory your platform registers
 * Each accessory may expose multiple services of different service types.
 */
export class ChookHutchDoorAccessory {
  private service: Service;
  private isDoorClosed: boolean;
  private targetState: number;

  /**
   * These are just used to create a working example
   * You should implement your own code to track the state of your accessory
   */
  private exampleStates = {
    On: false,
    Brightness: 100,
  };

  constructor(
    private readonly platform: ChookHutchPlatform,
    private readonly accessory: PlatformAccessory,
  ) {
    // set accessory information
    this.accessory.getService(this.platform.Service.AccessoryInformation)!
      .setCharacteristic(this.platform.Characteristic.Manufacturer, 'Default-Manufacturer')
      .setCharacteristic(this.platform.Characteristic.Model, 'Default-Model')
      .setCharacteristic(this.platform.Characteristic.SerialNumber, 'Default-Serial');

    // get the LightBulb service if it exists, otherwise create a new LightBulb service
    // you can create multiple services for each accessory

    if (accessory.context.device.CustomService) {
      // This is only required when using Custom Services and Characteristics not support by HomeKit
      this.service = this.accessory.getService(this.platform.CustomServices[accessory.context.device.CustomService]) ||
        this.accessory.addService(this.platform.CustomServices[accessory.context.device.CustomService]);
    } else {
      this.service = this.accessory.getService(this.platform.Service.Door) || this.accessory.addService(this.platform.Service.Door);
    }

    // set the service name, this is what is displayed as the default name on the Home app
    // in this example we are using the name we stored in the `accessory.context` in the `discoverDevices` method.
    this.service.setCharacteristic(this.platform.Characteristic.Name, accessory.context.device.exampleDisplayName);

    // each service must implement at-minimum the "required characteristics" for the given service type
    // see https://developers.homebridge.io/#/service/Lightbulb

    /*
    // register handlers for the On/Off Characteristic
    this.service.getCharacteristic(this.platform.Characteristic.TargetPosition)
      .onSet(this.setOn.bind(this)) // SET - bind to the `setOn` method below
      .onGet(this.getOn.bind(this)); // GET - bind to the `getOn` method below

    // register handlers for the Brightness Characteristic
    this.service.getCharacteristic(this.platform.Characteristic.Brightness)
      .onSet(this.setBrightness.bind(this)); // SET - bind to the `setBrightness` method below
*/

    this.service.getCharacteristic(this.platform.Characteristic.CurrentPosition)
      .onGet(this.handleCurrentPositionGet.bind(this));

    this.service.getCharacteristic(this.platform.Characteristic.PositionState)
      .onGet(this.handlePositionStateGet.bind(this));

    this.service.getCharacteristic(this.platform.Characteristic.TargetPosition)
      .onGet(this.handleTargetPositionGet.bind(this))
      .onSet(this.handleTargetPositionSet.bind(this));

    this.service.getCharacteristic(this.platform.Characteristic.TargetDoorState)
      .onSet(this.handleTargetPositionSet.bind(this));


    /**
     * Creating multiple services of the same type.
     *
     * To avoid "Cannot add a Service with the same UUID another Service without also defining a unique 'subtype' property." error,
     * when creating multiple services of the same type, you need to use the following syntax to specify a name and subtype id:
     * this.accessory.getService('NAME') || this.accessory.addService(this.platform.Service.Lightbulb, 'NAME', 'USER_DEFINED_SUBTYPE_ID');
     *
     * The USER_DEFINED_SUBTYPE must be unique to the platform accessory (if you platform exposes multiple accessories, each accessory
     * can use the same subtype id.)
     */

    // Example: add two "motion sensor" services to the accessory
    const doorService = this.accessory.getService('Hutch Door Service')
      || this.accessory.addService(this.platform.Service.Door, 'Hutch Door Service', 'Door-Service-1');

    //const motionSensorTwoService = this.accessory.getService('Motion Sensor Two Name')
    //  || this.accessory.addService(this.platform.Service.MotionSensor, 'Motion Sensor Two Name', 'YourUniqueIdentifier-2');

    /**
     * Updating characteristics values asynchronously.
     *
     * Example showing how to update the state of a Characteristic asynchronously instead
     * of using the `on('get')` handlers.
     * Here we change update the motion sensor trigger states on and off every 10 seconds
     * the `updateCharacteristic` method.
     *
     */
    /*
    let motionDetected = false;
    setInterval(() => {
      // EXAMPLE - inverse the trigger
      motionDetected = !motionDetected;

      // push the new value to HomeKit
      motionSensorOneService.updateCharacteristic(this.platform.Characteristic.MotionDetected, motionDetected);
      motionSensorTwoService.updateCharacteristic(this.platform.Characteristic.MotionDetected, !motionDetected);

      this.platform.log.debug('Triggering motionSensorOneService:', motionDetected);
      this.platform.log.debug('Triggering motionSensorTwoService:', !motionDetected);
    }, 10000);
    */
    this.isDoorClosed = false;
    this.targetState = this.platform.Characteristic.TargetDoorState.CLOSED;
    this.updateCurrentState();
  }
  updateCurrentState() {
    this.isDoorClosed = doorReedSwitchPin.readSync() == 0;
    this.platform.log.debug('isDoorClosed:', this.isDoorClosed);

  }

  async openDoor(){
    linearActuatorAPin.writeSync(Gpio.HIGH);
    linearActuatorBPin.writeSync(Gpio.LOW);
    this.service.updateCharacteristic(this.platform.Characteristic.CurrentDoorState,
                                      this.platform.Characteristic.CurrentDoorState.OPEN
    )
    //await asyncWait(5000);
    this.service.updateCharacteristic(this.platform.Characteristic.CurrentPosition,
      100);
  }

  async closeDoor(){
    linearActuatorAPin.writeSync(Gpio.LOW);
    linearActuatorBPin.writeSync(Gpio.HIGH);
    this.service.updateCharacteristic(this.platform.Characteristic.CurrentDoorState,
      this.platform.Characteristic.CurrentDoorState.CLOSED);
      this.service.updateCharacteristic(this.platform.Characteristic.CurrentPosition,
        0);
}

  

  /**
   * Handle requests to get the current value of the "Current Position" characteristic
   */
  handleCurrentPositionGet() {
    /*
    from https://developer.apple.com/documentation/homekit/hmcharacteristictypecurrentposition :
    The corresponding value is an integer percentage. A value of 0 indicates a door or window is fully closed, 
    or that awnings or shades permit the least possible light. A value of 100 indicates the opposite.
    */
    this.platform.log.debug('Triggered GET CurrentPosition');
    let value: number = 100;
    this.updateCurrentState();
    if (this.isDoorClosed) {
      value = 0;
    }
    this.platform.log.debug('CurrentPosition:', value);
    return value;
  }
  /**
   * Handle requests to get the current value of the "Position State" characteristic
   */
  handlePositionStateGet() {
    this.platform.log.debug('Triggered GET PositionState');
    this.updateCurrentState();
    let value: number = this.platform.Characteristic.CurrentDoorState.OPEN;
    if (this.isDoorClosed) {
      value = this.platform.Characteristic.CurrentDoorState.CLOSED;
    }
    this.platform.log.debug('PositionState:', value);
    return value;
  }


  /**
   * Handle requests to get the current value of the "Target Position" characteristic
   */
  handleTargetPositionGet() {
    this.platform.log.debug('Triggered GET TargetPosition');
    let value = this.targetState == this.platform.Characteristic.TargetDoorState.CLOSED ? 0 : 100;
    // set this to a valid value for TargetPosition
    this.platform.log.debug('TargetPosition:', value);

    return value;
  }

  /**
   * Handle requests to set the "Target Position" characteristic
   */
  handleTargetPositionSet(value: CharacteristicValue) {
    this.targetState = value as number;
    this.platform.log.debug('Triggered SET TargetPosition:', value);
    if (Number(value) > 0){
      this.openDoor();
    }
    else{
      this.closeDoor();
    }
  }
}

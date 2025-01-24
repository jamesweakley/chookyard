import type { API } from 'homebridge';

//import { ExampleHomebridgePlatform } from './platform.js';
import { PLATFORM_NAME } from './settings.js';

import { ChookHutchPlatform } from './platform.js';
/**
 * This method registers the platform with Homebridge
 */
export default (api: API) => {
  api.registerPlatform(PLATFORM_NAME, ChookHutchPlatform);
};

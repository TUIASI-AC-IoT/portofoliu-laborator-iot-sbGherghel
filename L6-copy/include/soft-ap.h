#ifndef _SOFT_AP_H_
#define _SOFT_AP_H_

#define EXAMPLE_ESP_WIFI_SSID      "ESP32-prov-<nume-familie>"
#define EXAMPLE_ESP_WIFI_PASS      "password"
#define EXAMPLE_ESP_WIFI_CHANNEL   6
#define EXAMPLE_MAX_STA_CONN       4

void wifi_init_softap(void);

#endif
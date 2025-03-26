/*  WiFi softAP Example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "freertos/event_groups.h"
#include "esp_http_server.h"


#include "lwip/err.h"
#include "lwip/sys.h"

#include "soft-ap.h"
#include "http-server.h"
#include "scan.h"

#include "../mdns/include/mdns.h"

static const char *TAG = "wifi softAP";


void app_main(void)
{
    //Initialize NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
      ESP_ERROR_CHECK(nvs_flash_erase());
      ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    static httpd_handle_t server = NULL;

    // TODO: 3. SSID scanning in STA mode 

    wifi_scan();

    // TODO: 1. Start the softAP mode

    //ESP_LOGI(SOFTAP_TAG, "ESP_WIFI_MODE_AP");
    wifi_init_softap();


     // TODO: 4. mDNS init (if there is time left)   

    // TODO: 2. Start the web server 
    server = start_webserver();

    // Open
    printf("\n");
    printf("Opening Non-Volatile Storage (NVS) handle... ");
    nvs_handle_t my_handle;
    ret = nvs_open("storage", NVS_READWRITE, &my_handle);
    if (ret != ESP_OK) {
        printf("Error (%s) opening NVS handle!\n", esp_err_to_name(ret));
    } else {
        printf("Done\n");

        // Read
        printf("Reading restart counter from NVS ... ");
        int32_t restart_counter = 0; // value will default to 0, if not set yet in NVS
        ret = nvs_get_i32(my_handle, "restart_counter", &restart_counter);
        switch (ret) {
            case ESP_OK:
                printf("Done\n");
                printf("Restart counter = %li\n", restart_counter);
                break;
            case ESP_ERR_NVS_NOT_FOUND:
                printf("The value is not initialized yet!\n");
                break;
            default :
                printf("Error (%s) reading!\n", esp_err_to_name(ret));
        }

        // Write
        printf("Updating restart counter in NVS ... ");
        restart_counter++;
        ret = nvs_set_i32(my_handle, "restart_counter", restart_counter);
        printf((ret != ESP_OK) ? "Failed!\n" : "Done\n");

        // Commit written value.
        // After setting any values, nvs_commit() must be called to ensure changes are written
        // to flash storage. Implementations may write to storage at other times,
        // but this is not guaranteed.
        printf("Committing updates in NVS ... ");
        ret = nvs_commit(my_handle);
        printf((ret != ESP_OK) ? "Failed!\n" : "Done\n");

        // Close
        nvs_close(my_handle);
    }

    printf("\n");

    // Restart module
    for (int i = 10; i >= 0; i--) {
        printf("Restarting in %d seconds...\n", i);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
    printf("Restarting now.\n");
    fflush(stdout);
    esp_restart();
       

}
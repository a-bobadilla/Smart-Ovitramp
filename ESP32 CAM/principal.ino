#include <stdio.h>
#include <string.h>
#include <time.h>
#include "esp_log.h"
#include "esp_camera.h"
#include "mqtt_client.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "protocol_examples_common.h"

#define CAMERA_PIXEL_FORMAT PIXFORMAT_JPEG
#define CAMERA_FRAME_SIZE FRAMESIZE_640X480
#define MQTT_BROKER_URI "mqtt://192.168.100.125"
#define MQTT_TOPIC_IMAGE "smartovi/ovitramp1/imagen"
#define MQTT_TOPIC_STATUS "smartovi/ovitramp1/status"

// Configuración de la cámara
void camera_config(){
    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = 5;
    config.pin_d1 = 18;
    config.pin_d2 = 19;
    config.pin_d3 = 21;
    config.pin_d4 = 36;
    config.pin_d5 = 39;
    config.pin_d6 = 34;
    config.pin_d7 = 35;
    config.pin_xclk = 0;
    config.pin_pclk = 22;
    config.pin_vsync = 25;
    config.pin_href = 23;
    config.pin_sccb_sda = 26;
    config.pin_sccb_scl = 27;
    config.pin_reset = -1;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = CAMERA_PIXEL_FORMAT;
    config.frame_size = CAMERA_FRAME_SIZE;
    config.jpeg_quality = 12;
    config.fb_count = 1;

    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        ESP_LOGE("CAMERA", "Error inicializando la cámara: %s", esp_err_to_name(err));
        return;
    }
}

// Callback de eventos MQTT
static esp_err_t mqtt_event_handler(esp_mqtt_event_handle_t event) {
    switch (event->event_id) {
        case MQTT_EVENT_CONNECTED:
            ESP_LOGI("MQTT", "Conectado al servidor MQTT");
            break;
        case MQTT_EVENT_DISCONNECTED:
            ESP_LOGI("MQTT", "Desconectado del servidor MQTT");
            break;
        default:
            break;
    }
    return ESP_OK;
}

// Función para capturar y publicar la imagen
void send_image_mqtt(esp_mqtt_client_handle_t client) {
    camera_fb_t *fb = esp_camera_fb_get();
    if (!fb) {
        ESP_LOGE("CAMERA", "No se pudo capturar la imagen");
        return;
    }

    // Publicar imagen en el tema MQTT
    int msg_id = esp_mqtt_client_publish(client, MQTT_TOPIC_IMAGE, (const char *)fb->buf, fb->len, 1, 0);
    if (msg_id != -1) {
        ESP_LOGI("MQTT", "Imagen publicada en MQTT, msg_id=%d", msg_id);
    }
    esp_camera_fb_return(fb);
}

// Función para publicar el estado
void send_status_mqtt(esp_mqtt_client_handle_t client) {
    time_t now;
    time(&now);
    struct tm *timeinfo = localtime(&now);
    char status_msg[64];
    strftime(status_msg, sizeof(status_msg), "ok %Y-%m-%d %H:%M:%S", timeinfo);
    esp_mqtt_client_publish(client, MQTT_TOPIC_STATUS, status_msg, 0, 1, 0);
}

void app_main() {
    // Inicialización de NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
      ESP_ERROR_CHECK(nvs_flash_erase());
      ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // Conectar a la red Wi-Fi
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    ESP_ERROR_CHECK(example_connect());

    // Inicializar la cámara
    camera_config();

    // Configuración y conexión al broker MQTT
    esp_mqtt_client_config_t mqtt_cfg = {
        .uri = MQTT_BROKER_URI,
        .event_handle = mqtt_event_handler,
    };
    esp_mqtt_client_handle_t client = esp_mqtt_client_init(&mqtt_cfg);
    esp_mqtt_client_start(client);

    // Capturar y enviar imagen
    send_image_mqtt(client);
    
    // Publicar estado
    send_status_mqtt(client);
}

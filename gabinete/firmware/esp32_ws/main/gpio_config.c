#include "include/gpio_config.h"
#include "esp_log.h"

static const char *TAG = "GPIO_CONFIG";

esp_err_t setup_gpios() {

    esp_err_t ret = ESP_OK;

    /* ---------- CONFIGURAR GENERAL INPUTS ---------- */
    for (size_t i = 0; i < sizeof(general_inputs)/sizeof(general_inputs[0]); i++) {

        const GeneralInput *in = &general_inputs[i];

        if (!in->habilitado) {
            ESP_LOGI(TAG, "Saltando %s (deshabilitado)", in->identificador);
            continue;
        }

        if (in->pin == GPIO_NUM_NC || in->pin == -1) {
            ESP_LOGW(TAG, "%s tiene pin no conectado", in->identificador);
            continue;
        }

        gpio_config_t cfg = {
            .pin_bit_mask = 1ULL << in->pin,
            .mode = GPIO_MODE_INPUT,
            .pull_up_en = GPIO_PULLUP_DISABLE,
            .pull_down_en = GPIO_PULLDOWN_DISABLE,
            .intr_type = GPIO_INTR_DISABLE
        };

        ret |= gpio_config(&cfg);
        ESP_LOGI(TAG, "Configurado INPUT %s en GPIO %d", in->identificador, in->pin);
    }


    /* ---------- CONFIGURAR GENERAL OUTPUTS ---------- */
    for (size_t i = 0; i < sizeof(general_outputs)/sizeof(general_outputs[0]); i++) {

        const GeneralOutput *out = &general_outputs[i];

        if (!out->habilitado) {
            ESP_LOGI(TAG, "Saltando %s (deshabilitado)", out->identificador);
            continue;
        }

        if (out->pin == GPIO_NUM_NC || out->pin == -1) {
            ESP_LOGW(TAG, "%s tiene pin no conectado", out->identificador);
            continue;
        }

        gpio_config_t cfg = {
            .pin_bit_mask = 1ULL << out->pin,
            .mode = GPIO_MODE_OUTPUT,
            .pull_up_en = GPIO_PULLUP_DISABLE,
            .pull_down_en = GPIO_PULLDOWN_DISABLE,
            .intr_type = GPIO_INTR_DISABLE
        };

        ret |= gpio_config(&cfg);
        gpio_set_level(out->pin, 0);
        ESP_LOGI(TAG, "Configurado OUTPUT %s en GPIO %d", out->identificador, out->pin);
    }


    /* ---------- CONFIG INPUTS ---------- */
    for (size_t i = 0; i < sizeof(config_inputs)/sizeof(config_inputs[0]); i++) {

        const ConfigInput *in = &config_inputs[i];

        if (!in->habilitado) {
            ESP_LOGI(TAG, "Saltando %s (deshabilitado)", in->identificador);
            continue;
        }

        if (in->pin == GPIO_NUM_NC || in->pin == -1) {
            ESP_LOGW(TAG, "%s tiene pin no conectado", in->identificador);
            continue;
        }

        gpio_config_t cfg = {
            .pin_bit_mask = 1ULL << in->pin,
            .mode = GPIO_MODE_INPUT,
            .pull_up_en = GPIO_PULLUP_DISABLE,
            .pull_down_en = GPIO_PULLDOWN_DISABLE,
            .intr_type = GPIO_INTR_DISABLE
        };

        ret |= gpio_config(&cfg);
        ESP_LOGI(TAG, "Configurado CONFIG INPUT %s en GPIO %d", in->identificador, in->pin);
    }


    /* ---------- CONFIG OUTPUTS ---------- */
    for (size_t i = 0; i < sizeof(config_outputs)/sizeof(config_outputs[0]); i++) {

        const ConfigOutput *out = &config_outputs[i];

        if (!out->habilitado) {
            ESP_LOGI(TAG, "Saltando %s (deshabilitado)", out->identificador);
            continue;
        }

        if (out->pin == GPIO_NUM_NC || out->pin == -1) {
            ESP_LOGW(TAG, "%s tiene pin no conectado", out->identificador);
            continue;
        }

        gpio_config_t cfg = {
            .pin_bit_mask = 1ULL << out->pin,
            .mode = GPIO_MODE_OUTPUT,
            .pull_up_en = GPIO_PULLUP_DISABLE,
            .pull_down_en = GPIO_PULLDOWN_DISABLE,
            .intr_type = GPIO_INTR_DISABLE
        };

        ret |= gpio_config(&cfg);
        gpio_set_level(out->pin, 0);
        ESP_LOGI(TAG, "Configurado CONFIG OUTPUT %s en GPIO %d", out->identificador, out->pin);
    }

    return ret;
}

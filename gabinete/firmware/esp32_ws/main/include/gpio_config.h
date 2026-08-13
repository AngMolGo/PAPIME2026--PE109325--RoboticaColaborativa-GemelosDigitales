#ifndef GPIO_CONFIG_H
#define GPIO_CONFIG_H

    #include "esp_err.h"
    #include "driver/gpio.h"

    // COMUNICACIÓN UART0
    #define UART0_TX GPIO_NUM_1              // 22. Transmisión  (no van a conectarse)
    #define UART0_RX GPIO_NUM_3              // 23. Recepción    (no van a conectarse)
    // COMUNICACIÓN UART1
    #define UART1_TX GPIO_NUM_17             // 22. Transmisión  (no van a conectarse, solo para debuguear)
    #define UART1_RX GPIO_NUM_16             // 23. Recepción    (no van a conectarse, solo para debuguear)

/* # # # # # # # # # # # #   CONFIGURACIÓN DE PINES  # # # # # # # # # # # # # */

    /* Entradas generales */

    typedef struct {
        gpio_num_t pin;
        bool habilitado;
        const char *identificador;
    } GeneralInput;
    
    static const GeneralInput general_inputs[] = {
        { GPIO_NUM_21,      true,       "GENERAL_INPUT_00" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_23,      true,       "GENERAL_INPUT_01" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_5,       true,       "GENERAL_INPUT_02" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "GENERAL_INPUT_03" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "GENERAL_INPUT_04" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "GENERAL_INPUT_05" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "GENERAL_INPUT_06" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "GENERAL_INPUT_07" },   // 00. INPUT_00 -> GPIO_00
    };



    /* Salidas generales */

    typedef struct {
        gpio_num_t pin;
        bool habilitado;
        const char *identificador;
    } GeneralOutput;

    static const GeneralOutput general_outputs[] = {
        { GPIO_NUM_15,      true,       "GENERAL_OUTPUT_00" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_2,       true,       "GENERAL_OUTPUT_01" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_0,       true,       "GENERAL_OUTPUT_02" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_4,       true,       "GENERAL_OUTPUT_03" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "GENERAL_OUTPUT_04" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "GENERAL_OUTPUT_05" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "GENERAL_OUTPUT_06" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "GENERAL_OUTPUT_07" },   // 00. INPUT_00 -> GPIO_00
    };

    

    /* Entradas dedicadas (botones, entrada safety, selector, etc) */

    typedef struct {
        gpio_num_t pin;
        bool habilitado;
        const char *identificador;
    } ConfigInput;
    
    static const ConfigInput config_inputs[] = {
        { GPIO_NUM_NC,      false,      "CONFIG_INPUT_00" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "CONFIG_INPUT_01" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "CONFIG_INPUT_02" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_18,      true,       "SAFETY_INPUT"    },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "CONFIG_INPUT_04" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "CONFIG_INPUT_05" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "CONFIG_INPUT_06" },   // SIN CONECTAR
        { GPIO_NUM_NC,      false,      "CONFIG_INPUT_07" },   // SIN CONECTAR
    };



    /* Salidas dedicadas (btones luminosos, torreta luminosa, etc) */

    typedef struct {
        gpio_num_t pin;
        bool habilitado;
        const char *identificador;
    } ConfigOutput;
    
    static const ConfigOutput config_outputs[] = {
        { GPIO_NUM_22,      true,       "TORRETA_LUMOSA_AMBAR"},// 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "CONFIG_OUTPUT_01" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "CONFIG_OUTPUT_02" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "CONFIG_OUTPUT_03" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "CONFIG_OUTPUT_04" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "CONFIG_OUTPUT_05" },   // 00. INPUT_00 -> GPIO_00
        { GPIO_NUM_NC,      false,      "CONFIG_OUTPUT_06" },   // SIN CONECTAR
        { GPIO_NUM_NC,      false,      "CONFIG_OUTPUT_07" },   // SIN CONECTAR
    };



/* # # # # # # # # # # # #   DECLARACIÓN DE FUNCIONES   # # # # # # # # # # # # # */

    esp_err_t setup_gpios();

#endif //GPIO_CONFIG_H

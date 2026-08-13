#include "gpio_manager_task.h"
#include "micro_ros_task.h"

#include "gpio_config.h"
#include "driver/gpio.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"

#include "esp_log.h"

static const char *TAG_GPIO_MANAGER_TASK = "GPIO_MANAGER_TASK_C"; // El 'TAG' es una etiqueta que se utiliza para identificar la fuente del mensaje de registro.

void gpio_manager_task(void * arg){

    pkg_pe26_gabinete_custom_interfaces__msg__Outputs msg;
    pkg_pe26_gabinete_custom_interfaces__msg__Outputs msg_2;

    while (true)
    {

        // Outputs_standard_desired
        if (xQueueReceive(xQueueExample, &msg, 0))
        {
            for (size_t i = 0; i < 8; i++)
            {
                GeneralOutput * general_outputs_i = &general_outputs[i];
                if (general_outputs_i->habilitado && general_outputs_i->pin!=GPIO_NUM_NC){
                    gpio_set_level(general_outputs_i->pin, msg.output[i]);
                }
            }
        }

        // Outputs_config_desired
        if (xQueueReceive(xQueueExample_2, &msg_2, 0))
        {
            for (size_t i = 0; i < 8; i++)
            {
                ConfigOutput * config_output_i = &config_outputs[i];
                if (config_output_i->habilitado && config_output_i->pin!=GPIO_NUM_NC){
                    gpio_set_level(config_output_i->pin, msg_2.output[i]);
                }
            }
        }
        
        
        // Actualización de Inputs
        pkg_pe26_gabinete_custom_interfaces__msg__Inputs msg_inputs_general = {0};
        for (size_t i = 0; i < 8; i++)
        {
            ConfigInput * general_input_i = &general_inputs[i];
            
            if (general_input_i->habilitado && general_input_i->pin!=GPIO_NUM_NC){
                msg_inputs_general.input[i] = gpio_get_level(general_input_i->pin);
                //printf("%d: %d\n",i,msg_inputs_general.input[i]);    
            }
            
        }
        //printf("\n");
        xQueueOverwrite(xQueueExample_3, &msg_inputs_general);
        

        // Actualización de Inputs
        pkg_pe26_gabinete_custom_interfaces__msg__Inputs msg_inputs_config = {0};
        for (size_t i = 0; i < 8; i++)
        {
            ConfigInput * config_input_i = &config_inputs[i];
            
            if (config_input_i->habilitado && config_input_i->pin!=GPIO_NUM_NC){
                msg_inputs_config.input[i] = gpio_get_level(config_input_i->pin);
                //printf("%d: %d\n",i,msg_inputs_general.input[i]);    
            }
            
        }
        //printf("\n");
        xQueueOverwrite(xQueueExample_4, &msg_inputs_config);

        
        //ESP_LOGI(TAG_GPIO_MANAGER_TASK, "Loop de prueba...");
        //vTaskDelay(pdMS_TO_TICKS(1));
    }   
    vTaskDelete(NULL);
}
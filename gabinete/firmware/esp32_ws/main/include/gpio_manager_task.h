#ifndef GPIO_MANAGER_TASK_H
#define GPIO_MANAGER_TASK_H

#include "gpio_config.h"
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"

#include "pkg_pe26_gabinete_custom_interfaces/msg/inputs.h"
#include "pkg_pe26_gabinete_custom_interfaces/msg/outputs.h"

extern QueueHandle_t xQueueExample_4;
extern QueueHandle_t xQueueExample_3;

void gpio_manager_task(void * arg);

#endif //GPIO_MANAGER_TASK_H
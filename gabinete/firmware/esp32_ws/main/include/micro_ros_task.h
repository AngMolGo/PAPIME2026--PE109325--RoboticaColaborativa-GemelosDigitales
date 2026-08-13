#ifndef MICRO_ROS_TASK_H
#define MICRO_ROS_TASK_H



#include <string.h>
#include <stdio.h>
#include <unistd.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_system.h"
#include "driver/uart.h"

#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <std_msgs/msg/int32.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

#include <rmw_microxrcedds_c/config.h>
#include <rmw_microros/rmw_microros.h>
#include "esp32_serial_transport.h"

#include "pkg_pe26_gabinete_custom_interfaces/msg/inputs.h"
#include "pkg_pe26_gabinete_custom_interfaces/msg/outputs.h"

#include "freertos/queue.h"


#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Aborting.\n",__LINE__,(int)temp_rc);vTaskDelete(NULL);}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Continuing.\n",__LINE__,(int)temp_rc);}}

// Queue1
extern QueueHandle_t xQueueExample;
extern QueueHandle_t xQueueExample_2;



// # # # # # #   PUBS, SUS, INTERFACES Y FUNCIONES CALLBACKS		   # # # # # #



// 1.- Definición de publicadres y suscriptores.
extern rcl_subscription_t general_outputs_subscriber;
extern rcl_subscription_t dedicated_outputs_subscriber;
extern rcl_publisher_t general_inputs_publisher;
extern  rcl_publisher_t dedicated_inputs_publisher;


// 2.- Definición de interfaces (msg, srv y personalizados)
extern pkg_pe26_gabinete_custom_interfaces__msg__Inputs msg_in;
extern pkg_pe26_gabinete_custom_interfaces__msg__Outputs msg_out;


// # # # # # Funciones

void timer_callback(rcl_timer_t * timer, int64_t last_call_time);
void subscription_callback(const void * msgin);

void micro_ros_task(void * arg);





#endif //MICRO_ROS_TASK_H
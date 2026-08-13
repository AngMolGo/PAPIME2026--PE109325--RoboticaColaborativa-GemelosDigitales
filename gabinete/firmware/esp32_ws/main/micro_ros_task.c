#include "micro_ros_task.h"
#include "esp_log.h"
#include "gpio_manager_task.h"

static const char *TAG_MICRO_ROS_TASK = "MICRO_ROS_TASK_C"; // El 'TAG' es una etiqueta que se utiliza para identificar la fuente del mensaje de registro.


// 1.- Definición de publicadres y suscriptores.
rcl_subscription_t general_outputs_subscriber;
rcl_subscription_t config_outputs_subscriber;
rcl_publisher_t general_inputs_publisher;
rcl_publisher_t config_inputs_publisher;

// 2.- Definición de interfaces (msg, srv y personalizados)
pkg_pe26_gabinete_custom_interfaces__msg__Inputs msg_in = {0};
pkg_pe26_gabinete_custom_interfaces__msg__Inputs msg_in_2 = {0};
pkg_pe26_gabinete_custom_interfaces__msg__Outputs msg_out;
pkg_pe26_gabinete_custom_interfaces__msg__Outputs msg_out_2;


// 3.- Definción de funciones callback.
void timer_callback(rcl_timer_t * timer, int64_t last_call_time)
{
	RCLC_UNUSED(last_call_time);
	if (timer != NULL) {

		xQueueReceive(xQueueExample_3, &msg_in, 0);

		// 2.- Publicar mensaje en el tópico
		RCSOFTCHECK(rcl_publish(&general_inputs_publisher, &msg_in, NULL));
	}
}


void timer_callback_2(rcl_timer_t * timer, int64_t last_call_time)
{
	RCLC_UNUSED(last_call_time);
	if (timer != NULL) {

		// 1. Leer mensaje desde Queue
        xQueueReceive(xQueueExample_4, &msg_in_2, 0);

		// 2.- Publicar mensaje en el tópico
		RCSOFTCHECK(rcl_publish(&config_inputs_publisher, &msg_in_2, NULL));
	}
}



void subscription_callback(const void * msgin)
{
	const pkg_pe26_gabinete_custom_interfaces__msg__Outputs * msg = (const pkg_pe26_gabinete_custom_interfaces__msg__Outputs *)msgin;
	//ESP_LOGI(TAG_MICRO_ROS_TASK, "%d", msg->output[0]);
	// Mandar mensaje a Queue
	pkg_pe26_gabinete_custom_interfaces__msg__Outputs tmp = *msg;
	xQueueOverwrite(xQueueExample, &tmp);

}

void subscription_callback_2(const void * msgin)
{
	const pkg_pe26_gabinete_custom_interfaces__msg__Outputs * msg = (const pkg_pe26_gabinete_custom_interfaces__msg__Outputs *)msgin;
	//ESP_LOGI(TAG_MICRO_ROS_TASK, "%d", msg->output[0]);
	// Mandar mensaje a Queue
	pkg_pe26_gabinete_custom_interfaces__msg__Outputs tmp = *msg;
	xQueueOverwrite(xQueueExample_2, &tmp);
}




// # # # # # #   FUNCIÓN PRINCIPAL DE MICROROS   # # # # # #

void micro_ros_task(void * arg)
{
	rcl_allocator_t allocator = rcl_get_default_allocator();
	rclc_support_t support;

	// create init_options
	RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));
    ESP_LOGI(TAG_MICRO_ROS_TASK, "No sé qué es esto, pero ya esta creado");

	// create node
	rcl_node_t node;
	RCCHECK(rclc_node_init_default(&node, "pe115326_gabinete_esp32", "", &support));


	// create publisher
	RCCHECK(rclc_publisher_init_default(
		&general_inputs_publisher,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(pkg_pe26_gabinete_custom_interfaces, msg, Inputs),
		"/gabinete/inputs/standard"));

	RCCHECK(rclc_publisher_init_default(
    	&config_inputs_publisher,
    	&node,
    	ROSIDL_GET_MSG_TYPE_SUPPORT(pkg_pe26_gabinete_custom_interfaces, msg, Inputs),
    	"/gabinete/inputs/config"));


	// Create subscriber.
	RCCHECK(rclc_subscription_init_default(
		&general_outputs_subscriber,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(pkg_pe26_gabinete_custom_interfaces, msg, Outputs),
		"/gabinete/outputs/standard"));
    ESP_LOGI(TAG_MICRO_ROS_TASK, "Suscriptor creado...");

	// Create subscriber.
	RCCHECK(rclc_subscription_init_default(
		&config_outputs_subscriber,
		&node,
		ROSIDL_GET_MSG_TYPE_SUPPORT(pkg_pe26_gabinete_custom_interfaces, msg, Outputs),
		"/gabinete/outputs/config"));
    ESP_LOGI(TAG_MICRO_ROS_TASK, "Suscriptor creado...");

	// create timer,
	rcl_timer_t timer;
	const unsigned int timer_timeout = 5;
	RCCHECK(rclc_timer_init_default2(
		&timer,
		&support,
		RCL_MS_TO_NS(timer_timeout),
		timer_callback,
		true));
    ESP_LOGI(TAG_MICRO_ROS_TASK, "Timer creado...");

	// create timer,
	rcl_timer_t timer_2;
	const unsigned int timer_timeout_2 = 5;
	RCCHECK(rclc_timer_init_default2(
		&timer_2,
		&support,
		RCL_MS_TO_NS(timer_timeout_2),
		timer_callback_2,
		true));
    ESP_LOGI(TAG_MICRO_ROS_TASK, "Timer creado...");

	// create executor
	rclc_executor_t executor;
	RCCHECK(rclc_executor_init(&executor, &support.context, 4, &allocator));
	RCCHECK(rclc_executor_add_timer(&executor, &timer));
	RCCHECK(rclc_executor_add_timer(&executor, &timer_2));
	RCCHECK(rclc_executor_add_subscription(&executor, &general_outputs_subscriber, &msg_out, &subscription_callback, ON_NEW_DATA));
	RCCHECK(rclc_executor_add_subscription(&executor, &config_outputs_subscriber, &msg_out_2, &subscription_callback_2, ON_NEW_DATA));
    ESP_LOGI(TAG_MICRO_ROS_TASK, "Ejecutor creado...");

	msg_in.input[0] = 0;

	while(1){
		rclc_executor_spin_some(&executor, RCL_MS_TO_NS(4));
		//usleep(10000);
		vTaskDelay(pdMS_TO_TICKS(10));
	}

    ESP_LOGI(TAG_MICRO_ROS_TASK, "Liberando memoria...");
	// free resources
	RCCHECK(rcl_subscription_fini(&general_outputs_subscriber, &node));
	RCCHECK(rcl_publisher_fini(&general_inputs_publisher, &node));
	RCCHECK(rcl_node_fini(&node));

  	vTaskDelete(NULL);
}
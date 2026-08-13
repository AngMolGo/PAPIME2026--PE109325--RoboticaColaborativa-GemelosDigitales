#include "micro_ros_task.h"
#include "gpio_manager_task.h"

static const char *TAG_MAIN = "MAIN_C"; // El 'TAG' es una etiqueta que se utiliza para identificar la fuente del mensaje de registro.

/* # # # # # # # # # #   FUNCIÓN PRINCIPAL (MAIN)   # # # # # # # # # # # */

static size_t uart_port = UART_NUM_0;
// Aquí sí va la DEFINICIÓN real
QueueHandle_t xQueueExample;
QueueHandle_t xQueueExample_2;
QueueHandle_t xQueueExample_3;
QueueHandle_t xQueueExample_4;

void app_main(void)
{

	/* # # # # # # # # # # # # # # # # # #   FASE 1: Configuraciones   # # # # # # # # # # # # # */
	
	// 1.- Inicialización de GPIOs
	setup_gpios();

	
	// Crear Queue ANTES de lanzar tareas
    xQueueExample = xQueueCreate(1, sizeof(pkg_pe26_gabinete_custom_interfaces__msg__Outputs));
    assert(xQueueExample != NULL);
	// Crear Queue ANTES de lanzar tareas
    xQueueExample_2 = xQueueCreate(1, sizeof(pkg_pe26_gabinete_custom_interfaces__msg__Outputs));
    assert(xQueueExample_2 != NULL);
	// Crear Queue ANTES de lanzar tareas
    xQueueExample_3 = xQueueCreate(1, sizeof(pkg_pe26_gabinete_custom_interfaces__msg__Inputs));
    assert(xQueueExample_3 != NULL);
	// Crear Queue ANTES de lanzar tareas
    xQueueExample_4 = xQueueCreate(1, sizeof(pkg_pe26_gabinete_custom_interfaces__msg__Inputs));
    assert(xQueueExample_4 != NULL);
	

	// 2.- Configuración de transporte personalizado por UART-USB
	#if defined(RMW_UXRCE_TRANSPORT_CUSTOM)
		rmw_uros_set_custom_transport(
			true,
			(void *) &uart_port,
			esp32_serial_open,
			esp32_serial_close,
			esp32_serial_write,
			esp32_serial_read
		);
		ESP_LOGI(TAG_MAIN, "Se configuró correctamente el transporte personalizado.");
	#else
	#error micro-ROS transports misconfigured
	#endif  // RMW_UXRCE_TRANSPORT_CUSTOM

	


	/* # # # # # # # # # # # # # # # #   FASE 2: Lanzamiento de tareas   # # # # # # # # # # # # */

    xTaskCreatePinnedToCore(micro_ros_task,
            "uros_task",
            CONFIG_MICRO_ROS_APP_STACK,
            NULL,
            16,
            NULL,
			0);

	xTaskCreatePinnedToCore(gpio_manager_task,
			"gpio_manager_task",
			2048,
			NULL,
			12,
			NULL,
			1);
}

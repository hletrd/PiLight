#include <pigpio.h>
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
	if (gpioInitialise() < 0) return 0;
	gpioSetMode(16, PI_OUTPUT);
	gpioSetMode(20, PI_OUTPUT);
	gpioSetMode(21, PI_OUTPUT);
	gpioSetPWMrange(16, 1000);
	gpioSetPWMrange(20, 1000);
	gpioSetPWMrange(21, 1000);

	while(1) {
		gpioPWM(16, atoi(argv[0]));
		gpioPWM(20, atoi(argv[1]));
		gpioPWM(21, atoi(argv[2]));
		puts("PWM set OK");
	}
}
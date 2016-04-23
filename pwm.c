#include <pigpio.h>
#include <stdio.h>
int main(int argc, char **argv) {
	gpioInitialise();
	gpioSetMode(16, PI_OUTPUT);
	gpioSetMode(20, PI_OUTPUT);
	gpioSetMode(21, PI_OUTPUT);
	gpioSetPWMrange(16, 1000);
	gpioSetPWMrange(20, 1000);
	gpioSetPWMrange(21, 1000);

	while(1) {
		int r, g, b;
		scanf("%d%d%d", &r, &g, &b);
		gpioPWM(16, r);
		gpioPWM(20, g);
		gpioPWM(21, b);
	}
}
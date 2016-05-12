#include <pigpio.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int main(int argc, char **argv) {
	if (gpioInitialise() < 0) return 0;
	gpioSetMode(16, PI_OUTPUT);
	gpioSetMode(20, PI_OUTPUT);
	gpioSetMode(21, PI_OUTPUT);
	gpioSetPWMrange(16, 1000);
	gpioSetPWMrange(20, 1000);
	gpioSetPWMrange(21, 1000);

	gpioPWM(16, atoi(argv[1]));
	gpioPWM(20, atoi(argv[2]));
	gpioPWM(21, atoi(argv[3]));
	int r, g, b;
	FILE *f;
	while(1) {
		f = fopen("pwm.txt", "r");
		fscanf(f, "%d%d%d", &r, &g, &b);
		gpioPWM(16, r);
		gpioPWM(20, g);
		gpioPWM(21, b);
		fclose(stdin);
		usleep(50000);
	}
}
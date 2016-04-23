Compiler=gcc

pwm: pwm.c
	$(Compiler) pwm.c -Ofast -o pwm -lpigpio -lrt
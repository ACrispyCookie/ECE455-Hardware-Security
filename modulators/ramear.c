// Compile: gcc -msse2 -Wall -std=c99 -O2 ramear.c -o ramear

#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include <stdlib.h>
#include <emmintrin.h>
#include <pthread.h>
#include <stdbool.h>
#include <string.h>

#define BUFFER_SIZE 164096
#define PULSE_WIDTH (CLOCKS_PER_SEC * 0.125)

void transmit_init();
void transmit_free();
void transmit_begin();
void transmit_bytes(uint8_t * bytes, uint8_t len);
void transmit_end();

static volatile __m128i * buffer;
static volatile __m128i reg;
uint8_t begin_string[1] = { 0b10101001 };
uint8_t end_string[1] =   { 0b11111111 };

static inline uint32_t current_time() {
	clock_t now = clock();
	return now;
}

static inline void steroids() {
	__m128i* buffer_ptr = (__m128i*) buffer;

	for (uint32_t i = 0 ; i < BUFFER_SIZE ; i++) {
		_mm_stream_si128(
			&reg,
			*buffer_ptr
		);
		buffer_ptr = buffer_ptr + 1;
	}
}

static inline void transmit_plain_bit(uint8_t bit) {
	clock_t begin = clock();
	if (bit == 1) {
		while(clock() - begin < PULSE_WIDTH) {
			steroids();
		}
	} else {
		while(clock() - begin < PULSE_WIDTH);
	}
}

static inline void dummy_steroids() {
	for (bool flag = 1 ; 1; flag = !flag) {
		transmit_plain_bit((uint8_t) flag);
	}
}

void transmit_begin() {
	for (uint32_t i = 0 ; i < 8 ; i++) {
		uint8_t bit = (begin_string[0] >> (7 - i)) & 0b1;
		transmit_plain_bit(bit);
	}
}

void transmit_bytes(uint8_t * bytes, uint8_t len) {
	for (uint32_t i = 0 ; i < len ; i++) {
		for (uint32_t j = 0 ; j < 8 ; j++) {
			uint8_t bit = (bytes[i] >> (7 - j)) & 0b1;
			transmit_plain_bit(bit);
		}
	}
}

void transmit_end() {
	for (uint32_t i = 0 ; i < 8 ; i++) {
		uint8_t bit = (end_string[0] >> (7 - i)) & 0b1;
		transmit_plain_bit(bit);
	}
}

void transmit_init() {
	buffer = malloc(BUFFER_SIZE * sizeof(__m128i));
	for (uint32_t i = 0 ; i < BUFFER_SIZE ; i++) {
		buffer[i][0] = rand();
		buffer[i][1] = rand();
	}
}

void transmit_free() {
	free(buffer);
	buffer = NULL;
}

int main()
{
	 /*
	uint8_t byte = 0b10101010;
	uint8_t zero = 0;
	*/
	transmit_init();
	while (1) {
		uint8_t * data = NULL;
		size_t len = 0;
		puts("Enter a string to transmit: ...");
		getline(&data, &len, stdin);
		transmit_begin();
		transmit_bytes(data, strlen((const char*) data) - 1);
		transmit_end();
		puts("done!");
		free(data);
	}
	transmit_free();
}

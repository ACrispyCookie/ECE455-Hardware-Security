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

static clock_t pulse_width;

void transmit_init();
void transmit_free();
void transmit_begin();
void transmit_bytes(uint8_t * bytes, uint8_t len);
void transmit_end();
static uint8_t *read_file(const char *path, size_t *out_len);

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
		while (clock() - begin < pulse_width) {
			steroids();
		}
	} else {
		while (clock() - begin < pulse_width);
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

static uint8_t *read_file(const char *path, size_t *out_len) {
	FILE *f = fopen(path, "rb");
	if (!f) {
		perror("fopen");
		return NULL;
	}

	if (fseek(f, 0, SEEK_END) != 0) {
		perror("fseek");
		fclose(f);
		return NULL;
	}

	long size = ftell(f);
	if (size <= 0) {
		fprintf(stderr, "Invalid file size\n");
		fclose(f);
		return NULL;
	}

	rewind(f);

	uint8_t *buf = malloc(size);
	if (!buf) {
		perror("malloc");
		fclose(f);
		return NULL;
	}

	if (fread(buf, 1, size, f) != (size_t)size) {
		perror("fread");
		free(buf);
		fclose(f);
		return NULL;
	}

	fclose(f);
	*out_len = (size_t)size;
	return buf;
}

int main(int argc, char **argv)
{	if (argc != 3) {

		fprintf(stderr, "Usage: %s <symbols_per_second> <keyfile>\n", argv[0]);
		return 1;
	}

	double symbols_per_second = atof(argv[1]);
	if (symbols_per_second <= 0.0) {
		fprintf(stderr, "symbols_per_second must be > 0\n");
		return 1;
	}

	pulse_width = (clock_t)(CLOCKS_PER_SEC / symbols_per_second);
	if (pulse_width == 0)
		pulse_width = 1;

	size_t data_len;
	uint8_t *data = read_file(argv[2], &data_len);
	if (!data)
		return 1;

	printf("Loaded %zu bytes from %s\n", data_len, argv[2]);
	printf("Pulse width: %ld clock ticks\n", (long)pulse_width);

	transmit_init();

	transmit_begin();
	transmit_bytes(data, (uint8_t)data_len);
	transmit_end();

	free(data);
	transmit_free();
}

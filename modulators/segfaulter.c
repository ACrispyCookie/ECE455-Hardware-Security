// Compile: gcc -O2 segfaulter.c -o segfaulter -pthread
// Run as root or normal user; only on hardware you own.

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
#include <pthread.h>
#include <unistd.h>

#define BUF_MB 64            // buffer size (MB); increase to stress memory bus
#define BURST_MS 2000        // duration of "1" in ms
#define IDLE_MS 2000         // duration of "0" in ms
#define PREAMBLE_BITS 8

volatile int stop_flag = 0;
uint8_t *buf;
size_t buf_size;

static inline uint64_t now_ms() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec*1000ULL + ts.tv_nsec/1000000ULL;
}

// memory-walking worker that continuously reads through buffer
void *mem_worker(void *arg) {
    size_t step = 64; // read stride (cache line)
    while(!stop_flag){
        for(size_t i = 0; i < buf_size; i += step){
            // volatile to prevent optimization
            volatile uint8_t v = buf[i];
            (void)v;
        }
    }
    return NULL;
}

void send_bit(int bit) {
    uint64_t t0;
    if (bit) {
        // start worker thread
        stop_flag = 0;
        pthread_t thr;
        if(pthread_create(&thr,NULL,mem_worker,NULL) != 0){
            perror("pthread_create");
            return;
        }
        t0 = now_ms();
        while(now_ms() - t0 < BURST_MS) { /* busy sleep */ }
        stop_flag = 1;
        pthread_join(thr, NULL);
    } else {
        // idle
        usleep(IDLE_MS * 1000);
    }
}

int main(int argc, char** argv) {
    // build buffer
    buf_size = (size_t) BUF_MB * 1024 * 1024;
    buf = malloc(buf_size);
    if (!buf) {
        perror("malloc");
        return 1;
    }
    // touch memory to allocate pages
    for(size_t i = 0; i < buf_size; i += 4096)
        buf[i] = (uint8_t)(i & 0xFF);

    // Example payload: preamble + payload bits (ASCII 'A' 0x41)
    // Format: PREAMBLE of alternating 1/0 for sync, then 8-bit byte LSB-first
    uint8_t payload[] = {0x41, 0x42}; // two bytes to transmit (change as you like)
    int i;

    // preamble (alternating 1/0) to help sync at receiver
    for(i=0;i<PREAMBLE_BITS;i++){
        send_bit(i%2);
    }

    // send bytes LSB first
    for(size_t b=0; b < sizeof(payload); b++){
        uint8_t byte = payload[b];
        for(i = 0; i < 8; i++){
            int bit = (byte >> i) & 1;
            send_bit(bit);
        }
        // inter-byte gap
        usleep(200000);
    }

    free(buf);
    return 0;
}
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> // for sleep

#define NUM_THREADS 10

void *runner(void *param) {
    int i;
    int upper = *((int *)param);
    printf("Thread %d starting...\n", upper);
    for (i = 0; i < 10; i++) {
        printf("Thread %d working...\n", upper);
        sleep(4); // Simulate work
    }
    printf("Thread %d exiting...\n", upper);
    pthread_exit(0);
}

int main() {
    pthread_t workers[NUM_THREADS];
    pthread_attr_t attr;
    pthread_attr_init(&attr);

    int *args[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++) {
        args[i] = malloc(sizeof(int));
        *args[i] = i + 1;
        sleep(4);
        pthread_create(&workers[i], &attr, runner, args[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(workers[i], NULL);
        free(args[i]); // Clean up memory
    }

    return 0;
}

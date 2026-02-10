#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

#define THREAD_COUNT 4   // change this to more threads if you want

DWORD Sum = 0;           // shared data
HANDLE hMutex;           // mutex for synchronization

typedef struct {
    DWORD start;
    DWORD end;
} THREAD_DATA;

/* Thread function */
DWORD WINAPI Summation(LPVOID Param)
{
    THREAD_DATA* data = (THREAD_DATA*)Param;
    DWORD localSum = 0;

    printf("Thread %lu: summing from %lu to %lu\n",
           GetCurrentThreadId(), data->start, data->end);

    for (DWORD i = data->start; i <= data->end; i++) {
        localSum += i;
        Sleep(50); // slow it down so you can see threads working
    }

    // lock mutex before touching shared Sum
    WaitForSingleObject(hMutex, INFINITE);
    Sum += localSum;
    ReleaseMutex(hMutex);

    printf("Thread %lu finished. Local sum = %lu\n",
           GetCurrentThreadId(), localSum);

    return 0;
}

int main(int argc, char* argv[])
{
    if (argc != 2) {
        printf("Usage: %s <number>\n", argv[0]);
        return 1;
    }

    DWORD upper = atoi(argv[1]);
    HANDLE threads[THREAD_COUNT];
    THREAD_DATA threadData[THREAD_COUNT];

    hMutex = CreateMutex(NULL, FALSE, NULL);
    if (hMutex == NULL) {
        printf("Failed to create mutex\n");
        return 1;
    }

    DWORD range = upper / THREAD_COUNT;
    DWORD start = 1;

    printf("Main: Creating %d threads...\n", THREAD_COUNT);

    for (int i = 0; i < THREAD_COUNT; i++) {
        threadData[i].start = start;
        threadData[i].end = (i == THREAD_COUNT - 1)
                                ? upper
                                : start + range - 1;

        threads[i] = CreateThread(
            NULL,
            0,
            Summation,
            &threadData[i],
            0,
            NULL
        );

        start += range;
    }

    // wait for all threads
    WaitForMultipleObjects(THREAD_COUNT, threads, TRUE, INFINITE);

    // cleanup
    for (int i = 0; i < THREAD_COUNT; i++) {
        CloseHandle(threads[i]);
    }

    CloseHandle(hMutex);

    printf("\nMain: Final sum = %lu\n", Sum);
    printf("Main: Press Enter to exit...\n");
    getchar();

    return 0;
}

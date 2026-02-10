#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <unistd.h>

int main(void)
{
    pid_t pid;

    pid = fork();

    if (pid < 0) {
        perror("fork failed");
        return 1;
    }
    else if (pid == 0) {
        execlp("sleep", "sleep", "30", NULL);
        perror("execlp failed");
        return 1;
    }
    else {
        wait(NULL);
        printf("Child Complete\n");
    }

    return 0;
}

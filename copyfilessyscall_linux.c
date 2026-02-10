#include <unistd.h>   // read, write, close
#include <fcntl.h>    // open
#include <stdio.h>    // perror
#include <stdlib.h>   // exit

#define BUFFER_SIZE 1024

int main() {
    int src_fd, dest_fd;
    ssize_t bytes_read;
    char buffer[BUFFER_SIZE];

    // Open source file (result.txt)
    src_fd = open("result.txt", O_RDONLY);
    if (src_fd < 0) {
        perror("Error opening source file");
        exit(1);
    }

    // Open destination file (copyresult.txt)
    dest_fd = open("copyresult.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (dest_fd < 0) {
        perror("Error opening destination file");
        close(src_fd);
        exit(1);
    }

    // Copy loop
    while ((bytes_read = read(src_fd, buffer, BUFFER_SIZE)) > 0) {
        if (write(dest_fd, buffer, bytes_read) != bytes_read) {
            perror("Write error");
            close(src_fd);
            close(dest_fd);
            exit(1);
        }
    }

    if (bytes_read < 0) {
        perror("Read error");
    }

    // Close files
    close(src_fd);
    close(dest_fd);

    write(STDOUT_FILENO, "File copied successfully\n", 26);

    return 0;
}
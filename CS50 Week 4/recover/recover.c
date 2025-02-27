#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

FILE *current_file;
int file_no = 0;
int block_size = 512;
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Cannot Open file");
        return 1;
    }
    uint8_t buffer[block_size];
    while (fread(buffer, 1, block_size, card) == block_size)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            if (file_no > 0)
            {
                fclose(current_file);
            }
            char *filename = malloc(8 * sizeof(char));
            sprintf(filename, "%03i.jpg", file_no);
            current_file = fopen(filename, "w");
            if (current_file == NULL)
            {
                printf("Cannot create file");
                return 1;
            }
            file_no++;
            free(filename);
        }
        if (file_no > 0)
        {
            fwrite(buffer, sizeof(buffer), 1, current_file);
        }
    }
    if (file_no > 0)
    {
        fclose(current_file);
    }
    fclose(card);
}

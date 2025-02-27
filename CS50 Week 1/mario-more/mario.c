#include <stdio.h>

int main(void)
{
    int a;
    int i;
    int j;
    do
    {
        printf("Height: ");
        scanf("%i", &a);
    }
    while (a < 1 || a > 8);
    for (i = 0; i < a; i++)
    {
        for (j = 0; j < (a * 2 + 2); j++)
        {
            if (j >= a - i - 1 && j < a)
            {
                printf("#");
            }
            else if (j <= a + 2 + i && j >= a + 2)
            {
                printf("#");
            }
            else if (j < a + 2)
            {
                printf(" ");
            }
        }
        printf("\n");
    }
}

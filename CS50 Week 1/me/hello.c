#include <stdio.h>

int main(void)
{
    printf("What's your name? ");
    char a[50] = "";
    scanf("%s", a);
    printf("hello, %s\n", a);
}

#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long cardID;
    int digit[100];
    int sum = 0;
    int length = 0;
    int tempInt;
    int i;
    int j;
    cardID = get_long("Number: ");
    while (cardID)
    {
        digit[length] = cardID % 10;
        length++;
        cardID /= 10;
    }
    int temp[length];
    for (i = 0; i < length; i++)
    {
        temp[i] = digit[i];
    }
    for (i = 1; i < length; i += 2)
    {
        tempInt = temp[i] * 2;
        tempInt = tempInt / 10 + tempInt % 10;
        sum = sum + tempInt;
    }
    for (i = 0; i < length; i += 2)
    {
        sum = sum + temp[i];
    }
    for (i = 0; i < length; i++)
    {
        temp[length - i - 1] = digit[i];
    }
    if (sum % 10 == 0)
    {
        if (temp[0] == 3 && (temp[1] == 4 || temp[1] == 7) && length == 15)
        {
            printf("AMEX\n");
        }
        else if (temp[0] == 5 &&
                 (temp[1] == 1 || temp[1] == 2 || temp[1] == 3 || temp[1] == 4 || temp[1] == 5) &&
                 length == 16)
        {
            printf("MASTERCARD\n");
        }
        else if (temp[0] == 4 && (length == 13 || length == 16))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

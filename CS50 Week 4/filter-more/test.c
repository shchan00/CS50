#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>

#include "helpers.h"

int main (void)
{
    RGBTRIPLE image[3][3];
    image[0][0].rgbtRed = 0;
    image[0][0].rgbtBlue = 10;
    image[0][0].rgbtGreen = 25;
    image[0][1].rgbtRed = 0;
    image[0][1].rgbtBlue = 10;
    image[0][1].rgbtGreen = 30;
    image[0][2].rgbtRed = 40;
    image[0][2].rgbtBlue = 60;
    image[0][2].rgbtGreen = 80;
    image[1][0].rgbtRed = 20;
    image[1][0].rgbtBlue = 30;
    image[1][0].rgbtGreen = 90;
    image[1][1].rgbtRed = 30;
    image[1][1].rgbtBlue = 40;
    image[1][1].rgbtGreen = 100;
    image[1][2].rgbtRed = 80;
    image[1][2].rgbtBlue = 70;
    image[1][2].rgbtGreen = 90;
    image[2][0].rgbtRed = 20;
    image[2][0].rgbtBlue = 20;
    image[2][0].rgbtGreen = 40;
    image[2][1].rgbtRed = 30;
    image[2][1].rgbtBlue = 10;
    image[2][1].rgbtGreen = 30;
    image[2][2].rgbtRed = 50;
    image[2][2].rgbtBlue = 40;
    image[2][2].rgbtGreen = 10;
    edges(3, 3, image);

}

#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int grey =
                round((image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) / 3.0);
            image[i][j].rgbtRed = grey;
            image[i][j].rgbtBlue = grey;
            image[i][j].rgbtGreen = grey;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            int tempred = image[i][width - j - 1].rgbtRed;
            int tempblue = image[i][width - j - 1].rgbtBlue;
            int tempgreen = image[i][width - j - 1].rgbtGreen;
            image[i][width - j - 1].rgbtRed = image[i][j].rgbtRed;
            image[i][width - j - 1].rgbtBlue = image[i][j].rgbtBlue;
            image[i][width - j - 1].rgbtGreen = image[i][j].rgbtGreen;
            image[i][j].rgbtRed = tempred;
            image[i][j].rgbtBlue = tempblue;
            image[i][j].rgbtGreen = tempgreen;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE ogimage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            ogimage[i][j].rgbtRed = image[i][j].rgbtRed;
            ogimage[i][j].rgbtBlue = image[i][j].rgbtBlue;
            ogimage[i][j].rgbtGreen = image[i][j].rgbtGreen;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int tempred = 0;
            int tempblue = 0;
            int tempgreen = 0;
            int count = 0;
            for (int k = fmax(0, i - 1); k < fmin(i + 2, height); k++)
            {
                for (int l = fmax(0, j - 1); l < fmin(j + 2, width); l++)
                {
                    tempred += ogimage[k][l].rgbtRed;
                    tempblue += ogimage[k][l].rgbtBlue;
                    tempgreen += ogimage[k][l].rgbtGreen;
                    count++;
                }
            }
            image[i][j].rgbtRed = round(tempred / (float) count);
            image[i][j].rgbtBlue = round(tempblue / (float) count);
            image[i][j].rgbtGreen = round(tempgreen / (float) count);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE ogimage[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            ogimage[i][j].rgbtRed = image[i][j].rgbtRed;
            ogimage[i][j].rgbtBlue = image[i][j].rgbtBlue;
            ogimage[i][j].rgbtGreen = image[i][j].rgbtGreen;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int gxred = 0;
            int gxblue = 0;
            int gxgreen = 0;
            int gyred = 0;
            int gyblue = 0;
            int gygreen = 0;
            int gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
            int gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};
            for (int k = fmax(0, i - 1); k < fmin(i + 2, height); k++)
            {
                for (int l = fmax(0, j - 1); l < fmin(j + 2, width); l++)
                {
                    gxred += ogimage[k][l].rgbtRed * gx[(k - i + 1)][(l - j + 1)];
                    gxblue += ogimage[k][l].rgbtBlue * gx[(k - i + 1)][(l - j + 1)];
                    gxgreen += ogimage[k][l].rgbtGreen * gx[(k - i + 1)][(l - j + 1)];
                    gyred += ogimage[k][l].rgbtRed * gy[(k - i + 1)][(l - j + 1)];
                    gyblue += ogimage[k][l].rgbtBlue * gy[(k - i + 1)][(l - j + 1)];
                    gygreen += ogimage[k][l].rgbtGreen * gy[(k - i + 1)][(l - j + 1)];
                }
            }
            image[i][j].rgbtRed =
                fmin(round(sqrt(pow((float) gxred, 2) + pow((float) gyred, 2))), 255);
            image[i][j].rgbtBlue =
                fmin(round(sqrt(pow((float) gxblue, 2) + pow((float) gyblue, 2))), 255);
            image[i][j].rgbtGreen =
                fmin(round(sqrt(pow((float) gxgreen, 2) + pow((float) gygreen, 2))), 255);
        }
    }
    return;
}

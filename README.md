How to run the code:

Command: python3 main.py <image-name>.jpg 16 S

1) Discussion of Approach for averaging algorithm:
First we do preprocessing for the image we want to process. main() function reads image and converts it to RGB as first stage, so each pixel gets 3 values - 3 channels of color. Then program takes square size from terminal and defines our square. I have used weighted mean for it:
For every pixel in the square, we look at the how far is this pixel from the nearest left or right edge, and how far is it from the nearest top or bottom edge. The distance is counted in pixels, starting at 1 for a pixel that is already on the edge. One step in - is distance 2, the next step is distance 3, and etc. So we calculate distance horizontally and vertically from edges. Then in order to get final weight for a pixel at anywhere of that square, we need to multiply both of those values for that pixel. Here is the example square for 10x10:
1   2   3   4   5   5   4   3   2   1
2   4   6   8  10  10   8   6   4   2
3   6   9  12  15  15  12   9   6   3
4   8  12  16  20  20  16  12   8   4
5  10  15  20  25  25  20  15  10   5
5  10  15  20  25  25  20  15  10   5
4   8  12  16  20  20  16  12   8   4
3   6   9  12  15  15  12   9   6   3
2   4   6   8  10  10   8   6   4   2
1   2   3   4   5   5   4   3   2   1

After that we can use it to average our image's pixels. 


Discussion of Single and Concurrent execution:
The code is able to run both single and multiple core execution. I used python as language to make my code much more cleaner for preprocessing and etc parts. But python also has some drawbacks related to concurrency. Python threads are not giving physical concurrency by nature, so they just run on same physical core no matter how many threads we fire. So, to tackle this problem, I used processes to achieve physical level concurrency. The code first takes the number of cores at the machine and then launches same amount of processes which are binded to separate workers - cores. So, it tries to leverage power of each physical core.


#include "vl_keypoints.h"
#include "vl_linesedges.h"

using namespace bimp;

int main( int argc, char **argv )
{
    if(argc < 5)
    {
        std::cerr << "Usage: testkps <filename> <start> <end> <scale>" << std::endl;
        return -1;
    }

    // Load the input image
    Mat img;
    Mat outimg; 
    img = imread(argv[1],0);

    int width = img.cols;
    int height = img.rows;

    std::cout << "Image width: " << width << std::endl;
    std::cout << "Image height: " << height << std::endl;

    // Select the scales we want to use (logarithmic spacing)
    //Type lambda_start = atof(argv[2]);
    //Type lambda_end = atof(argv[3]);
    int num_scales = atoi(argv[4]);
    //std::vector<Type> lambdas = makeLambdasLog(lambda_start, lambda_end, num_scales);

    // Scale with size of image
    Type dimensions = width * height;
    Type lambda_start = dimensions/pow(2,16);
    std::vector<Type> lambdas = makeLambdasLog(lambda_start, lambda_start*1.2, num_scales);

    // Extract keypoints at selected scales, 8 orientations
    std::vector<KeyPoint> points;
    std::vector<KPData> datas;
    points = keypoints(img,lambdas,datas,16,true);

    std::cout << std::endl << "Found " << points.size() << " points" << std::endl;


    
    // Draw the keypoints and save the image
    drawKeypoints(img, points, outimg, Scalar::all(255), 4);
    imwrite("out.png", outimg);

    return 0;
}



/**
 *
 * Main function to call different algorithms.
 *
 */

#include <cstdio>
#include <iostream>
#include <vector>
#include <sstream>
#include <omp.h>

#include "timer.hpp"
#include "Point.h"
#include "ChanAlgorithm.h"
#include "GrahamScanAlgorithm.h"
#include "JarvisAlgorithm.h"
#include "Quickhull.hpp"


int main(int argc, char const *argv[]) {
    #ifdef WRITE_DEBUG
        std::cout << "Running in DEBUG mode - writing ALL output files." << std::endl;
    #endif

    if (argc < 5) {
        std::cout << "Usage: " << " n_cores input_file algorithm iter_idx\n";
        std::cout << "  algorithm := chan_normal | chan_merge_var | graham | jarvis \n";

        return -1;
    }

    int n_cores             = atoi(argv[1]);
    auto numberOfCores      = (size_t)n_cores;
    std::string inputFile   = argv[2];
    std::string algorithm   = argv[3];
    int iterIdx             = atoi(argv[4]);

    std::vector<Point> points = readPointsFromFile(inputFile);

    timer timer;

    std::vector<Point> result;

    if (algorithm == "chan_normal") {
        ChanAlgorithm chan;

        timer.start();
        result = chan.run(points, numberOfCores, numberOfCores /* TODO number of parts*/);
        timer.stop();

    } else if (algorithm == "chan_merge_var") {
        ChanAlgorithm2Merge chan;
        timer.start();
        result = chan.run(points, numberOfCores, numberOfCores /* TODO number of parts*/);
        timer.stop();

    } else  if (algorithm == "graham") {
        GrahamScanAlgorithm graham;
        timer.start();
        result = graham.run(points);
        timer.stop();

    } else  if (algorithm == "jarvis") {
        JarvisAlgorithm jarvis;
        timer.start();
        result = jarvis.run(points);
        timer.stop();

    } else if (algorithm == "quickhull") {
        std::vector<int> result_idxs;
        timer.start();
        Quickhull::run(points, result_idxs);
        for(int idx: result_idxs) {
            result.push_back(points[idx]);
        }
        timer.stop();

    } else {
        std::cout << "No such algorithm!";
        std::exit(EXIT_FAILURE);
    }

    std::cout << "\n\n=========Result=========" << std::endl;
    std::cout << "Algorithm:     " << algorithm << std::endl;
    std::cout << "N hull points: " << result.size() << std::endl;
    std::cout << "Iteration:     " << iterIdx << std::endl;
    std::cout << "Time used:     " << timer.get_timing() << std::endl;

    std::stringstream fileName;
    fileName << "hull_points_" << iterIdx << ".dat";
    FileWriter::writePointsToFile(result, fileName.str(), true);
    timer.write_to_file(iterIdx);

    return 0;
}

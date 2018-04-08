#ifndef __BOX_H
#define __BOX_H

#include <stdint.h>
#include "common.h"

#define BOX_SUCCESS  0
#define BOX_FAILURE -1

#define BOX_SPLIT_X 0
#define BOX_SPLIT_Y 1
#define BOX_SPLIT_Z 2
#define BOX_SPLIT_AUTODIR -1

#include "mkl_vsl.h"


typedef struct Box Box;

struct Box {
    double center[NDIM];    // center of the box
    double ex[NDIM];        // 
    double ey[NDIM];        // basis vectors. Shows directions of box's edges
    double ez[NDIM];        //
    double dims[NDIM];      // Dimensions of the box.
    double lb[NDIM];        // lower bounds
    double ub[NDIM];        // upper bounds
    double corners[NCOR * NDIM];  // corners
    double volume;
    uint64_t subdiv;         // Box location.
    VSLStreamStatePtr rng;
};


int box_init( 
    Box * box,
    const double * center, 
    const double * ex, 
    const double * ey, 
    const double * ez,
    double xdim, 
    double ydim, 
    double zdim
);

void box_dispose(Box * box);

void box_copy(const Box * src, Box * dst);

int box_generate_random_points(
    Box * box, 
    double * points,
    size_t npts
);

void box_test_points(
    const Box * box, 
    const double * points, 
    size_t npts,
    int * result
);

int box_split(
    const Box * box, 
    Box * box1, 
    Box * box2, 
    int dir, 
    double ratio
);

void box_ieqcons(
    unsigned int m,
    double * result,
    unsigned int n,
    const double * x,
    double * grad,
    void * f_data
);

/* Compares two boxes. Returns
 * +1 if in_box lies actually inside the out_box;
 *  0 if in_box equals out_box;
 * -1 if in_box lies outside of the out_box;
 */
int box_is_in(const Box * in_box, uint64_t out_subdiv);

#endif
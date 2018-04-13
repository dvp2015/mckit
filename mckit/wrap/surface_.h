//
// Created by Roma on 08.04.2018.
//

#ifndef WRAP_SURFACE_H
#define WRAP_SURFACE_H

#include "../src/surface.h"

typedef struct {
    PyObject ob_base;
    Surface surf;
} SurfaceObject;

extern PyTypeObject SurfaceType;
extern PyTypeObject PlaneType;
extern PyTypeObject SphereType;
extern PyTypeObject CylinderType;
extern PyTypeObject ConeType;
extern PyTypeObject TorusType;
extern PyTypeObject GQuadraticType;

#endif //WRAP_SURFACE_H

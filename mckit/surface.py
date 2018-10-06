# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

import numpy as np

from .constants import *
from .geometry import Plane      as _Plane,    \
                      Sphere     as _Sphere,   \
                      Cone       as _Cone,     \
                      Cylinder   as _Cylinder, \
                      Torus      as _Torus,    \
                      GQuadratic as _GQuadratic, \
                      GLOBAL_BOX, ORIGIN, EX, EY, EZ
from .printer import print_card
from .transformation import Transformation

__all__ = [
    'create_surface', 'Plane', 'Sphere', 'Cone', 'Torus', 'GQuadratic',
    'Cylinder'
]


def create_surface(kind, *params, **options):
    """Creates new surface.

    Parameters
    ----------
    kind : str
        Surface kind designator. See MCNP manual.
    params : list[float]
        List of surface parameters.
    options : dict
        Dictionary of surface's options. Possible values:
            transform = tr - transformation to be applied to the surface being
                             created. Transformation instance.

    Returns
    -------
    surf : Surface
        New surface.
    """
    kind = kind.upper()
    if kind[-1] == 'X':
        axis = EX
    elif kind[-1] == 'Y':
        axis = EY
    elif kind[-1] == 'Z':
        axis = EZ
    # -------- Plane -------------------
    if kind[0] == 'P':
        if len(kind) == 2:
            return Plane(axis, -params[0], **options)
        else:
            return Plane(params[:3], -params[3], **options)
    # -------- SQ -------------------
    elif kind == 'SQ':
        A, B, C, D, E, F, G, x0, y0, z0 = params
        m = np.diag([A, B, C])
        v = 2 * np.array([D - A*x0, E - B*y0, F - C*z0])
        k = A*x0**2 + B*y0**2 + C*z0**2 - 2 * (D*x0 + E*y0 + F*z0) + G
        return GQuadratic(m, v, k, **options)
    # -------- Sphere ------------------
    elif kind[0] == 'S':
        if kind == 'S':
            r0 = np.array(params[:3])
        elif kind == 'SO':
            r0 = ORIGIN
        else:
            r0 = axis * params[0]
        R = params[-1]
        return Sphere(r0, R, **options)
    # -------- Cylinder ----------------
    elif kind[0] == 'C':
        A = 1 - axis
        if kind[1] == '/':
            Ax, Az = np.dot(A, EX), np.dot(A, EZ)
            r0 = params[0] * (Ax * EX + (1 - Ax) * EY) + \
                 params[1] * ((1 - Az) * EY + Az * EZ)
        else:
            r0 = ORIGIN
        R = params[-1]
        return Cylinder(r0, axis, R, **options)
    # -------- Cone ---------------
    elif kind[0] == 'K':
        if kind[1] == '/':
            r0 = np.array(params[:3])
            ta = np.sqrt(params[3])
        else:
            r0 = params[0] * axis
            ta = np.sqrt(params[1])
        sheet = 0 if len(params) % 2 == 0 else int(params[-1])
        return Cone(r0, axis, ta, sheet, **options)
    # ---------- GQ -----------------
    elif kind == 'GQ':
        A, B, C, D, E, F, G, H, J, k = params
        m = np.array([[A, 0.5*D, 0.5*F], [0.5*D, B, 0.5*E], [0.5*F, 0.5*E, C]])
        v = np.array([G, H, J])
        return GQuadratic(m, v, k, **options)
    # ---------- Torus ---------------------
    elif kind[0] == 'T':
        x0, y0, z0, R, a, b = params
        return Torus([x0, y0, z0], axis, R, a, b, **options)
    # ---------- Axisymmetric surface defined by points ------
    else:
        if len(params) == 2:
            return Plane(axis, -params[0], **options)
        elif len(params) == 4:
            # TODO: Use special classes instead of GQ
            h1, r1, h2, r2 = params
            if abs(h2 - h1) < RESOLUTION * max(abs(h1), abs(h2)):
                return Plane(axis, -0.5 * (h1 + h2), **options)
            elif abs(r2 - r1) < RESOLUTION * max(abs(r2), abs(r1)):
                R = 0.5 * (abs(r1) + abs(r2))
                return Cylinder([0, 0, 0], axis, R, **options)
            else:
                if r1 * r2 < 0:
                    raise ValueError('Points must belong to the one sheet.')
                h0 = (abs(r1) * h2 - abs(r2) * h1) / (abs(r1) - abs(r2))
                ta = abs((r1 - r2) / (h1 - h2))
                s = round((h1 - h0) / abs(h1 - h0))
                return Cone(axis * h0, axis, ta, sheet=s, **options)
        elif len(params) == 6:
            # TODO: Implement creation of surface by 3 points.
            raise NotImplementedError


def create_replace_dictionary(surfaces, unique=None, box=GLOBAL_BOX, tol=1.e-10):
    """Creates surface replace dictionary for equal surfaces removing.

    Parameters
    ----------
    surfaces : set[Surface]
        A set of surfaces to be checked.
    unique: set[Surface]
        A set of surfaces that are assumed to be unique. If not None, than
        'surfaces' are checked for coincidence with one of them.
    box : Box
        A box, which is used for comparison.
    tol : float
        Tolerance

    Returns
    -------
    replace : dict
        A replace dictionary. surface -> (replace_surface, sense). Sense is +1
        if surfaces have the same direction of normals. -1 otherwise.
    """
    replace = {}
    uniq_surfs = set() if unique is None else unique
    for s in surfaces:
        for us in uniq_surfs:
            t = s.equals(us, box=box, tol=tol)
            if t != 0:
                replace[s] = (us, t)
                break
        else:
            uniq_surfs.add(s)
    return replace


class Surface(ABC):
    """Base class for all surface classes.

    Methods
    -------
    equals(other, box, tol)
        Checks if this surface and surf are equal inside the box.
    test_point(p)
        Checks the sense of point p with respect to this surface.
    transform(tr)
        Applies transformation tr to this surface.
    test_box(box)
        Checks whether this surface crosses the box.
    projection(p)
        Gets projection of point p on the surface.
    """
    def __init__(self, **options):
        self.options = options.copy()

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return id(self) == id(other)

    @abstractmethod
    def equals(self, other, box=GLOBAL_BOX, tol=1.e-10):
        """Checks if this surface equals other one inside the box.

        Parameters
        ----------
        other : Surface
            Other surface.
        box : Box
            A box inside which surfaces are considered.
        tol : float
            Relative tolerance with respect to the origin of global coordinate
            system.

        Returns
        -------
        result : int
            The result of comparison. +1, if surfaces are equal, -1, if they
            are equal, but direction of normals is opposite. 0 - if they are
            not equal.
        """

    @abstractmethod
    def transform(self, tr):
        """Applies transformation to this surface.

        Parameters
        ----------
        tr : Transform
            Transformation to be applied.

        Returns
        -------
        surf : Surface
            The result of this surface transformation.
        """


class Plane(Surface, _Plane):
    """Plane surface class.

    Parameters
    ----------
    normal : array_like[float]
        The normal to the plane being created.
    offset : float
        Free term.
    options : dict
        Dictionary of surface's options. Possible values:
            transform = tr - transformation to be applied to this plane.
                             Transformation instance.
    """
    def __init__(self, normal, offset, **options):
        if 'transform' in options.keys():
            tr = options.pop('transform')
            v, k = tr.apply2plane(normal, offset)
        else:
            v = np.array(normal)
            k = offset
        Surface.__init__(self, **options)
        _Plane.__init__(self, v, k)

    def equals(self, other, box=GLOBAL_BOX, tol=1.e-10):
        raise NotImplementedError
        if not isinstance(other, Plane):
            return 0
        corners = box.corners()
        proj_self = self.projection(corners)
        proj_other = other.projection(corners)
        delta = np.linalg.norm(proj_other - proj_self, axis=1)
        abs_norm = np.linalg.norm(proj_self, axis=1)
        check = delta / abs_norm
        if np.nanmax(check) < tol:
            return int(np.sign(np.dot(self._v, other._v)))
        else:
            return 0

    def transform(self, tr):
        return Plane(self._v, self._k, transform=tr, **self.options)

    def __str__(self):
        words = [str(self.options['name']), ' ']
        if np.all(self._v == np.array([1.0, 0.0, 0.0])):
            words.append('PX')
        elif np.all(self._v == np.array([0.0, 1.0, 0.0])):
            words.append('PY')
        elif np.all(self._v == np.array([0.0, 0.0, 1.0])):
            words.append('PZ')
        else:
            words.append('P')
            for v in self._v:
                words.append(' ')
                words.append('{0:.12e}'.format(v))
        words.append(' ')
        words.append('{0:.12e}'.format(-self._k))
        return print_card(words)


class Sphere(Surface, _Sphere):
    """Sphere surface class.
    
    Parameters
    ----------
    center : array_like[float]
        Center of the sphere.
    radius : float
        The radius of the sphere.
    options : dict
        Dictionary of surface's options. Possible values:
            transform = tr - transformation to be applied to the sphere being
                             created. Transformation instance.
    """
    def __init__(self, center, radius, **options):
        if 'transform' in options.keys():
            tr = options.pop('transform')
            center = tr.apply2point(center)
        Surface.__init__(self, **options)
        _Sphere.__init__(self, center, radius)

    def equals(self, other, box=GLOBAL_BOX, tol=1.e-10):
        raise NotImplementedError
        if not isinstance(other, Sphere):
            return 0
        delta_center = np.linalg.norm(self._center - other._center)
        delta_radius = np.linalg.norm(self._radius - other._radius)
        check = (delta_center + delta_radius) / np.linalg.norm(self._center)
        if check < tol:
            return +1
        else:
            return 0

    def transform(self, tr):
        return Sphere(self._center, self._radius, transform=tr, **self.options)

    def __str__(self):
        words = [str(self.options['name']), ' ']
        if np.all(self._center == np.array([0.0, 0.0, 0.0])):
            words.append('SO')
        elif self._center[0] == 0.0 and self._center[1] == 0.0:
            words.append('SZ')
            words.append(' ')
            words.append('{0:.12e}'.format(self._center[2]))
        elif self._center[1] == 0.0 and self._center[2] == 0.0:
            words.append('SX')
            words.append(' ')
            words.append('{0:.12e}'.format(self._center[0]))
        elif self._center[0] == 0.0 and self._center[2] == 0.0:
            words.append('SY')
            words.append(' ')
            words.append('{0:.12e}'.format(self._center[1]))
        else:
            words.append('S')
            for v in self._center:
                words.append(' ')
                words.append('{0:.12e}'.format(v))
        words.append(' ')
        words.append('{0:.12e}'.format(self._radius))
        return print_card(words)


class Cylinder(Surface, _Cylinder):
    """Cylinder surface class.
    
    Parameters
    ----------
    pt : array_like[float]
        Point on the cylinder's axis.
    axis : array_like[float]
        Cylinder's axis direction.
    radius : float
        Cylinder's radius.
    options : dict
        Dictionary of surface's options. Possible values:
            transform = tr - transformation to be applied to the cylinder being
                             created. Transformation instance.
    """
    def __init__(self, pt, axis, radius, **options):
        if 'transform' in options.keys():
            tr = options.pop('transform')
            pt = tr.apply2point(pt)
            axis = tr.apply2vector(axis)
        axis = axis / np.linalg.norm(axis)
        Surface.__init__(self, **options)
        _Cylinder.__init__(self, pt, axis, radius)

    def equals(self, other, box=GLOBAL_BOX, tol=1.e-10):
        # TODO: add comparison
        return 0

    def transform(self, tr):
        return Cylinder(self._pt, self._axis, self._radius, transform=tr,
                        **self.options)

    def __str__(self):
        words = [str(self.options['name']), ' ']
        if np.all(self._axis == np.array([1.0, 0.0, 0.0])):
            if self._pt[1] == 0.0 and self._pt[2] == 0.0:
                words.append('CX')
            else:
                words.append('C/X')
                words.extend([' ', '{0:.12e}'.format(self._pt[1]), ' ',
                              '{0:.12e}'.format(self._pt[2])])
        elif np.all(self._axis == np.array([0.0, 1.0, 0.0])):
            if self._pt[0] == 0.0 and self._pt[2] == 0.0:
                words.append('CY')
            else:
                words.append('C/Y')
                words.extend([' ', '{0:.12e}'.format(self._pt[0]), ' ',
                              '{0:.12e}'.format(self._pt[2])])
        elif np.all(self._axis == np.array([0.0, 0.0, 1.0])):
            if self._pt[0] == 0.0 and self._pt[1] == 0.0:
                words.append('CZ')
            else:
                words.append('C/Z')
                words.extend([' ', '{0:.12e}'.format(self._pt[0]), ' ',
                              '{0:.12e}'.format(self._pt[1])])
        else:
            nx, ny, nz = self._axis
            m = np.array([[1-nx**2, -nx*ny, -nx*nz],
                          [-nx*ny, 1-ny**2, -ny*nz],
                          [-nx*nz, -ny*nz, 1-nz**2]])
            v = np.zeros(3)
            k = -self._radius**2
            m, v, k = Transformation(translation=self._pt).apply2gq(m, v, k)
            return str(GQuadratic(m, v, k, **self.options))
        words.append(' ')
        words.append('{0:.12e}'.format(self._radius))
        return print_card(words)


class Cone(Surface, _Cone):
    """Cone surface class.

    Parameters
    ----------
    apex : array_like[float]
        Cone's apex.
    axis : array_like[float]
        Cone's axis.
    ta : float
        Tangent of angle between axis and generatrix.
    sheet : int
        Cone's sheet.
    options : dict
        Dictionary of surface's options. Possible values:
            transform = tr - transformation to be applied to the cone being
                             created. Transformation instance.
    """
    def __init__(self, apex, axis, ta, sheet=0, **options):
        if 'transform' in options.keys():
            tr = options.pop('transform')
            apex = tr.apply2point(apex)
            axis = tr.apply2vector(axis)
        axis = axis / np.linalg.norm(axis)
        Surface.__init__(self, **options)
        # TODO: Do something with ta! It is confusing. _Cone accept ta, but returns t2.
        _Cone.__init__(self, apex, axis, ta, sheet)

    def equals(self, other, box=GLOBAL_BOX, tol=1.e-10):
        # TODO: add comparison
        return 0

    def transform(self, tr):
        return Cone(self._apex, self._axis, np.sqrt(self._t2),
                    sheet=self._sheet, transform=tr, **self.options)

    def __str__(self):
        words = [str(self.options['name']), ' ']
        if np.all(self._axis == np.array([1.0, 0.0, 0.0])):
            if self._apex[1] == 0.0 and self._apex[2] == 0.0:
                words.append('KX')
                words.append(' ')
                words.append('{0:.12e}'.format(self._apex[0]))
            else:
                words.append('K/X')
                for v in self._apex:
                    words.append(' ')
                    words.append('{0:.12e}'.format(v))
        elif np.all(self._axis == np.array([0.0, 1.0, 0.0])):
            if self._apex[0] == 0.0 and self._apex[2] == 0.0:
                words.append('KY')
                words.append(' ')
                words.append('{0:.12e}'.format(self._apex[1]))
            else:
                words.append('K/Y')
                for v in self._apex:
                    words.append(' ')
                    words.append('{0:.12e}'.format(v))
        elif np.all(self._axis == np.array([0.0, 0.0, 1.0])):
            if self._apex[0] == 0.0 and self._apex[1] == 0.0:
                words.append('KZ')
                words.append(' ')
                words.append('{0:.12e}'.format(self._apex[2]))
            else:
                words.append('K/Z')
                for v in self._apex:
                    words.append(' ')
                    words.append('{0:.12e}'.format(v))
        else:
            nx, ny, nz = self._axis
            a = 1 + self._t2
            m = np.array([[1-a*nx**2, -a*nx*ny, -a*nx*nz],
                          [-a*nx*ny, 1-a*ny**2, -a*ny*nz],
                          [-a*nx*nz, -a*ny*nz, 1-a*nz**2]])
            v = np.zeros(3)
            k = -self._radius**2
            m, v, k = Transformation(translation=self._apex).apply2gq(m, v, k)
            return str(GQuadratic(m, v, k, **self.options))
        words.append(' ')
        words.append('{0:.12e}'.format(self._t2))
        if self._sheet != 0:
            words.append(' ')
            words.append('{0:d}'.format(self._sheet))
        return print_card(words)


class GQuadratic(Surface, _GQuadratic):
    """Generic quadratic surface class.

    Parameters
    ----------
    m : array_like[float]
        Matrix of coefficients of quadratic terms. m.shape=(3,3)
    v : array_like[float]
        Vector of coefficients of linear terms. v.shape=(3,)
    k : float
        Free term.
    options : dict
        Dictionary of surface's options. Possible values:
            transform = tr - transformation to be applied to the surface being
                             created. Transformation instance.
    """
    def __init__(self, m, v, k, **options):
        if 'transform' in options.keys():
            tr = options.pop('transform')
            m, v, k = tr.apply2gq(m, v, k)
        else:
            m = np.array(m)
            v = np.array(v)
            k = k
        Surface.__init__(self, **options)
        _GQuadratic.__init__(self, m, v, k)

    def equals(self, other, box=GLOBAL_BOX, tol=1.e-10):
        # TODO: add comparison
        return 0

    def transform(self, tr):
        return GQuadratic(self._m, self._v, self._k, transform=tr,
                          **self.options)

    def __str__(self):
        words = [str(self.options['name']), ' ', 'GQ']
        a, b, c = np.diag(self._m)
        d = self._m[0, 1] + self._m[1, 0]
        e = self._m[1, 2] + self._m[2, 1]
        f = self._m[0, 2] + self._m[2, 0]
        g, h, j = self._v
        k = self._k
        for v in [a, b, c, d, e, f, g, h, j, k]:
            words.append(' ')
            words.append('{0:.12e}'.format(v))
        return print_card(words)


class Torus(Surface, _Torus):
    """Tori surface class.

    Parameters
    ----------
    center : array_like[float]
        The center of torus.
    axis : array_like[float]
        The axis of torus.
    R : float
        Major radius.
    a : float
        Radius parallel to torus axis.
    b : float
        Radius perpendicular to torus axis.
    options : dict
        Dictionary of surface's options. Possible values:
            transform = tr - transformation to be applied to the torus being
                             created. Transformation instance.
    """
    def __init__(self, center, axis, R, a, b, **options):
        if 'transform' in options.keys():
            tr = options.pop('transform')
            center = tr.apply2point(center)
            axis = tr.apply2vector(axis)
        else:
            center = np.array(center)
            axis = np.array(axis)
        axis = axis / np.linalg.norm(axis)
        Surface.__init__(self, **options)
        _Torus.__init__(self, center, axis, R, a, b)

    def equals(self, other, box=GLOBAL_BOX, tol=1.e-10):
        # TODO: add comparison
        return 0

    def transform(self, tr):
        return Torus(self._center, self._axis, self._R, self._a, self._b,
                     transform=tr, **self.options)

    def __str__(self):
        words = [str(self.options['name']), ' ']
        if np.all(self._axis == np.array([1.0, 0.0, 0.0])):
            words.append('TX')
        elif np.all(self._axis == np.array([0.0, 1.0, 0.0])):
            words.append('TY')
        elif np.all(self._axis == np.array([0.0, 0.0, 1.0])):
            words.append('TZ')
        x, y, z = self._center
        for v in [x, y, z, self._R, self._a, self._b]:
            words.append(' ')
            words.append('{0:.12e}'.format(v))
        return print_card(words)

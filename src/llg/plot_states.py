import vapory
import numpy


def Arrow(center, direction, color):
    center = numpy.array(center)
    direction = numpy.array(direction) * 0.9
    base_point_cylinder = center - 0.5 * direction
    cap_point_cone = center + 0.5 * direction
    cap_point_cylinder = base_point_cone = base_point_cylinder + 0.5 * direction

    radius_cylinder = 1 / 20
    base_radius_cone = 1 / 6

    cylinder = vapory.Cylinder(
        base_point_cylinder,
        cap_point_cylinder,
        radius_cylinder,
        vapory.Texture(vapory.Pigment("color", color)),
    )

    cone = vapory.Cone(
        base_point_cone,
        base_radius_cone,
        cap_point_cone,
        0.0,
        vapory.Texture(vapory.Pigment("color", color)),
    )

    return vapory.Union(cone, cylinder)


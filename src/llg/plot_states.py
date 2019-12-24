import vapory
import numpy
import os
import colorsys
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D


def PovrayArrow(position, direction, color):
    position = numpy.array(position)
    direction = numpy.array(direction) * 0.9
    base_point_cylinder = position - 0.5 * direction
    cap_point_cone = position + 0.7 * direction
    cap_point_cylinder = base_point_cone = base_point_cylinder + 0.7 * direction

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

    sphere = vapory.Sphere(
        position,
        2 * radius_cylinder,
        vapory.Texture(vapory.Pigment("color", [0, 0, 0])),
    )

    return vapory.Union(sphere, vapory.Union(cone, cylinder))


class PlotStates:
    def __init__(self, positions, output, size, mode):
        self.positions = positions
        self.output = output
        self.size = size
        self.mode = mode
        self.index = 1

        self.centroid = numpy.mean(self.positions, axis=0)
        self.location = numpy.array([1, 1, 1]) * [
            1 + 1.5 * numpy.max(numpy.linalg.norm(self.positions - self.centroid, axis=1))
        ]

    @staticmethod
    def get_rgb(direction, mode):
        sx, sy, sz = direction.T
        rho = numpy.sqrt(sx * sx + sy * sy)

        phi = (numpy.arctan2(sy, sx) + 2 * numpy.pi) % (2 * numpy.pi)
        theta = numpy.arctan2(rho, sz)

        if mode == "azimuthal":
            if sx == 0 and sy == 0:
                return (0, 0, 0)
            return colorsys.hls_to_rgb(phi / (2 * numpy.pi), 0.5, 1)
        elif mode == "polar":
            return colorsys.hls_to_rgb(theta / (2 * numpy.pi), 0.5, 1)
        else:
            raise Exception(f"Mode {mode} is not supported.")

    def plot(self, state, iteration, temperature, field, save=False):

        camera = vapory.Camera(
            "location",
            self.location,
            "look_at",
            self.centroid,
            "sky",
            [0, 0, 1],
            "up",
            [0, 0, 1],
            "right",
            [0, 1, 0],
        )
        background = vapory.Background([1, 1, 1])
        light = vapory.LightSource(self.location, "color", [1, 1, 1])

        arrows = []
        for position, direction in zip(self.positions, state):
            color = PlotStates.get_rgb(direction, self.mode)
            arrows.append(PovrayArrow(position, direction, color))

        scene = vapory.Scene(camera, objects=[background, light, *arrows])

        if save:
            try:
                os.mkdir(self.output)
            except FileExistsError:
                pass

            scene.render(
                f"{self.output}/figure_{self.index}.png",
                width=self.size[0],
                height=self.size[1],
                antialiasing=0,
            )

        self.index += 1

        return scene.render(width=self.size[0], height=self.size[1], antialiasing=0)

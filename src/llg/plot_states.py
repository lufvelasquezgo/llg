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
    cap_point_cone = position + 0.5 * direction
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


class PlotStates:
    def __init__(self, positions, output):
        self.positions = positions
        self.output = output

    @staticmethod
    def get_rgb(direction, mode):
        sx, sy, sz = direction.T
        r = numpy.sqrt(sx * sx + sy * sy + sz * sz)
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

    def __enter__(self):
        try:
            os.mkdir(self.output)
        except FileExistsError:
            pass
        return self

    def __exit__(self, *args):
        return


class PlotStatesPovray(PlotStates):
    def plot(self, state, mode="azimuthal", sufix=""):
        centroid = numpy.mean(self.positions, axis=0)
        location = numpy.array([1, 1, 1]) * 2 * numpy.max(self.positions, axis=0)

        camera = vapory.Camera(
            "location",
            location,
            "look_at",
            centroid,
            "sky",
            [0, 0, 1],
            "up",
            [0, 0, 1],
            "right",
            [0, 1, 0],
        )
        background = vapory.Background([1, 1, 1])
        light = vapory.LightSource(location, "color", [1, 1, 1])

        arrows = []
        for position, direction in zip(self.positions, state):
            color = PlotStates.get_rgb(direction, mode)
            arrows.append(PovrayArrow(position, direction, color))

        scene = vapory.Scene(camera, objects=[background, light, *arrows])

        return scene.render(
            f"{self.output}/plot_states{sufix}.png",
            width=500,
            height=500,
            antialiasing=0,
        )


class PlotStatesMatplotlib(PlotStates):
    def plot(self, state, mode="azimuthal", sufix=""):
        fig = pyplot.figure()
        ax = fig.add_subplot(111, projection="3d")

        x, y, z = numpy.array(self.positions).T
        sx, sy, sz = numpy.array(state).T
        colors = numpy.array(
            [PlotStates.get_rgb(direction, mode) for direction in state]
        )

        ax.quiver(x, y, z, sx, sy, sz, pivot="middle", normalize=True)
        pyplot.savefig(f"{self.output}/plot_states{sufix}.png")
        pyplot.close()


# class PlotStatesMayavi(PlotStates):
#     def plot(self, state, mode="azimuthal", sufix=""):
#         x, y, z = numpy.array(self.positions).T
#         sx, sy, sz = numpy.array(state).T
#         colors = numpy.array(
#             [PlotStates.get_rgb(direction, mode) for direction in state]
#         )

#         mlab.quiver3d(x, y, z, sx, sy, sz, line_width=3, mode=arrow, scale_mode="none")
#         mlab.savefig(f"{self.output}/plot_states{sufix}.png")
#         mlab.close()

class PlotStatesVpython(PlotStates):
    def plot(self, state, mode="azimuthal", sufix=""):

import vapory
import numpy
import os
from matplotlib import pyplot
from PIL import Image
import tempfile


def PovrayArrow(position, direction, color):
    position = numpy.array(position)
    direction = numpy.array(direction) * 0.9
    base_point_cylinder = position - 0.5 * direction
    cap_point_cone = position + 0.7 * direction
    cap_point_cylinder = base_point_cone = base_point_cylinder + 0.7 * direction

    radius_cylinder = 1 / 20
    base_radius_cone = 1 / 6

    texture = vapory.Texture(
            vapory.Pigment("color", color),
            vapory.Finish("roughness", 0, "ambient", 0.2),
        )

    cylinder = vapory.Cylinder(
        base_point_cylinder,
        cap_point_cylinder,
        radius_cylinder,
        texture,
    )

    cone = vapory.Cone(
        base_point_cone,
        base_radius_cone,
        cap_point_cone,
        0.0,
        texture
    )

    sphere = vapory.Sphere(
        position,
        2 * radius_cylinder,
        vapory.Texture(vapory.Pigment("color", [0, 0, 0])),
    )

    return vapory.Union(sphere, vapory.Union(cone, cylinder))


class PlotStates:
    def __init__(self, positions, output, size, mode, colormap):
        self.positions = positions
        self.output = output
        self.size = size
        self.mode = mode
        self.colormap = colormap
        self.index = 1

        self.max_angle = {"azimuthal": 2 * numpy.pi, "polar": numpy.pi}[self.mode]

        self.cmap_norm = pyplot.Normalize(vmin=0, vmax=self.max_angle)
        self.cmap = pyplot.get_cmap(colormap)

        self.centroid = numpy.mean(self.positions, axis=0)
        self.location = numpy.array([1, 1, 1]) * [
            1
            + 1.5 * numpy.max(numpy.linalg.norm(self.positions - self.centroid, axis=1))
        ]

        self.colorbar_image = self.create_colorbar()

    def create_colorbar(self):
        colorbar_file = tempfile.NamedTemporaryFile(suffix=".png")

        pyplot.figure(dpi=self.size[0])
        scatter = pyplot.scatter([], [], c=[], norm=self.cmap_norm, cmap=self.cmap)
        cbar = pyplot.colorbar(scatter)
        cbar.set_label(f"{self.mode.capitalize()} angle")
        pyplot.gca().remove()
        pyplot.savefig(colorbar_file.name, bbox_inches="tight")
        pyplot.close()

        image = Image.open(colorbar_file.name)
        colorbar_file.close()
        return numpy.array(image)

    @staticmethod
    def get_angle(direction, mode):
        sx, sy, sz = direction.T
        rho = numpy.sqrt(sx * sx + sy * sy)

        if mode == "azimuthal":
            return (numpy.arctan2(sy, sx) + 2 * numpy.pi) % (2 * numpy.pi)
        elif mode == "polar":
            return numpy.arctan2(rho, sz)
        else:
            raise Exception(f"Mode {mode} is not supported.")

    def get_rgb(self, direction, mode):
        angle = PlotStates.get_angle(direction, mode)
        color = self.cmap(self.cmap_norm(angle))
        return color[:3]  # rgba -> rgb

    @staticmethod
    def join_images(im1_array, im2_array):
        im1 = Image.fromarray(im1_array)
        im2 = Image.fromarray(im2_array)

        im1 = im1.resize((int(im1.width * im2.height / im1.height), im2.height))

        dst = Image.new("RGB", (im1.width + im2.width, im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))

        return dst

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
            color = self.get_rgb(direction, self.mode)
            arrows.append(PovrayArrow(position, direction, color))

        scene = vapory.Scene(camera, objects=[background, light, *arrows])
        scene_image = scene.render(
            width=self.size[0], height=self.size[1], antialiasing=0.1
        )

        image = PlotStates.join_images(self.colorbar_image, scene_image)
        if save:
            try:
                os.mkdir(self.output)
            except FileExistsError:
                pass

            image.save(f"{self.output}/figure_{self.index}.png")

        self.index += 1

        return numpy.array(image)

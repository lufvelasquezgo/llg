import os
import tempfile

import numpy
from matplotlib import font_manager, pyplot
from PIL import Image, ImageDraw, ImageFont

import vapory


def PovrayArrow(position, direction, color):
    """
    This function creates the arrow with the library vapory (https://pypi.org/project/Vapory/). It helps to process the image.

    :param position: It is the position where the object is going to be ubicated.
    :type position: list
    :param direction: It is the course along which the object moves.
    :type direction: list
    :param color: It is representes by the RGB color model. It is an additive color model in which red, green, and blue light are added together in various ways to reproduce a broad array of colors.
    :type color: list

    :return: It returns an ``Union()`` of three 3D figures, that represent the ``PovrayArrow()``.
    :rtype: ``Union()``
    """
    position = numpy.array(position)
    direction = numpy.array(direction) * 0.9
    base_point_cylinder = position - 0.5 * direction
    cap_point_cone = position + 0.7 * direction
    cap_point_cylinder = base_point_cone = base_point_cylinder + 0.7 * direction

    radius_cylinder = 1 / 20
    base_radius_cone = 1 / 6

    texture = vapory.Texture(
        vapory.Pigment("color", color), vapory.Finish("roughness", 0, "ambient", 0.2)
    )

    cylinder = vapory.Cylinder(
        base_point_cylinder, cap_point_cylinder, radius_cylinder, texture
    )

    cone = vapory.Cone(base_point_cone, base_radius_cone, cap_point_cone, 0.0, texture)

    sphere = vapory.Sphere(
        position,
        2 * radius_cylinder,
        vapory.Texture(vapory.Pigment("color", [0, 0, 0])),
    )

    return vapory.Union(sphere, vapory.Union(cone, cylinder))


class PlotStates:
    """This is a class for processing an image that contains the evolution of the state. It can be written to a file with the extesion ``.png``.

    :param positions: It is the position where the object is going to be ubicated. 
    :type positions: list
    :param output: It is the name of the file.
    :type output: str
    :param size: It is the size of the complete image.
    :type size: tuple
    :param mode: It is one of the two possibles modes (azimuthal/polar). 
    :type mode: str
    :param colormap: It is a matplotlib supported colormaps: https://matplotlib.org/examples/color/colormaps_reference.html
    :type colormap: str
    :param index: It is the index of the positions.
    :type index: int
    :param max_angle: It is the maximum angle. It depends on the mode, if it is ``polar`` the range is between 0° to 180°. On the other hand if it is ``azimuthal`` the range is between 0° to 360°. 
    :type max_angle: float
    :param cmap_norm: It is the colormap normalized.
    :type cmap_norm: list
    :param cmap: It is a colormap instance. This colormap used to map normalized data values to RGBA colors.
    :type cmap: str
    :param centroid: It is the geometric center of the plane image. It is the arithmetic mean position of all the points in the image. 
    :type centroid: float
    :param location: It is a ``numpy.array()`` of one looking site.
    :type location: list
    :param colorbar_image: It creates the colorbar. 
    :type colorbar_image:  
    :param font: It is the font default for the text in the image.
    :type font: str
    """

    def __init__(self, positions, output, size, mode, colormap):
        """It is the constructor for PlotStates class.
        
        :param positions: It is the position where the object is going to be ubicated. 
        :type positions: list
        :param output: It is the name of the file.
        :type output: str
        :param size: It is the size of the complete image.
        :type size: tuple
        :param mode: It is one of the two possibles modes (azimuthal/polar). 
        :type mode: str
        :param colormap: It is a matplotlib supported colormaps: https://matplotlib.org/examples/color/colormaps_reference.html
        :type colormap: str
        :param index: It is the index of the positions.
        :type index: int
        :param max_angle: It is the maximum angle. It depends on the mode, if it is ``polar`` the range is between 0° to 180°. On the other hand if it is ``azimuthal`` the range is between 0° to 360°. 
        :type max_angle: float
        :param cmap_norm: It is the colormap normalized.
        :type cmap_norm: list
        :param cmap: It is a colormap instance. This colormap used to map normalized data values to RGBA colors.
        :type cmap: str
        :param centroid: It is the geometric center of the plane image. It is the arithmetic mean position of all the points in the image. 
        :type centroid: float
        :param location: It is a ``numpy.array()`` of one looking site.
        :type location: list
        :param colorbar_image: It creates the colorbar. 
        :type colorbar_image:  
        :param font: It is the font default for the text in the image.
        :type font: str
        """
        self.positions = positions
        self.output = output
        self.size = size
        self.mode = mode
        self.colormap = colormap
        self.index = 1

        self.max_angle = {"azimuthal": 360, "polar": 180}[self.mode]

        self.cmap_norm = pyplot.Normalize(vmin=0, vmax=self.max_angle)
        self.cmap = pyplot.get_cmap(colormap)

        self.centroid = numpy.mean(self.positions, axis=0)
        self.location = numpy.array([1, 1, 1]) * [
            1
            + 1.5 * numpy.max(numpy.linalg.norm(self.positions - self.centroid, axis=1))
        ]

        self.colorbar_image = self.create_colorbar()

        self.font = ImageFont.truetype(font_manager.findfont(None), self.size // 25)

    def create_colorbar(self):
        """It is a function responsible of create the image of the colorbar with the library matplotlib (https://matplotlib.org/). It creates a temporary file with the image due to we do not want to show this images. Finally it returns an array.

        :param size: It is the size of the complete image.
        :type size: tuple
        :param mode: It is one of the two possibles modes (azimuthal/polar). 
        :type mode: str
        :param cmap_norm: It is the colormap normalized.
        :type cmap_norm: list
        :param cmap: It is a colormap instance. This colormap used to map 
        :type cmap: str
        """
        colorbar_file = tempfile.NamedTemporaryFile(suffix=".png")

        pyplot.figure(dpi=self.size)
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
        """It is a function decarator. It is the responsible of get the angle that the arrow is going to be directed. It depends on the mode that the User chose.

        :param direction: It is the course along which the object moves.
        :type direction: list.
        :param mode: It is one of the two possibles modes (azimuthal/polar). 
        :type mode: str.
        """
        sx, sy, sz = direction.T
        rho = numpy.sqrt(sx * sx + sy * sy)

        if mode == "azimuthal":
            phi = (numpy.arctan2(sy, sx) + 2 * numpy.pi) % (2 * numpy.pi)
            return numpy.degrees(phi)
        elif mode == "polar":
            theta = numpy.arctan2(rho, sz)
            return numpy.degrees(theta)
        else:
            raise Exception(f"Mode {mode} is not supported.")

    def get_rgb(self, direction, mode):
        """It is a function responsible to get the rgb colors through the angle.

        :param direction: It is the course along which the object moves.
        :type direction: list
        :param mode: It is one of the two possibles modes (azimuthal/polar). 
        :type mode: str

        :return: It returns the rgb format instead rgba.
        :rtype: array 
        """
        angle = PlotStates.get_angle(direction, mode)
        color = self.cmap(self.cmap_norm(angle))
        return color[:3]  # rgba -> rgb

    @staticmethod
    def join_images(im1_array, im2_array):
        """It is a function decorator. It is responsible of join the two images arrays, the colormap image array and the state image array. It uses the PIL library (https://pillow.readthedocs.io/en/stable/) to create an image memory from two images arrays interface (using the buffer protocol).

        :param im1_array: It is the array of the colormap array.
        :type im1_array: array
        :param im2_array: It is the array of the processing image of the states.
        :type im2_array: array
        
        :return: It returns an image of the colomap and the processing image of the states.
        :rtype: array
        """
        im1 = Image.fromarray(im1_array)
        im2 = Image.fromarray(im2_array)

        im1 = im1.resize((int(im1.width * im2.height / im1.height), im2.height))

        dst = Image.new("RGB", (im1.width + im2.width, im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))

        return dst

    def plot(self, state, iteration, temperature, field, save=False):
        """It is a function that creates the complete scene of the evolve of the states. It join the two array of the images. Also, it allows to put a text on the top of the scene.

        :param state:  It gets the states information from the simulation hdf file.
        :type state: list
        :param iteration:  It gets the number of iterations from the hdf file.
        :type iteration: int
        :param temperature: It gets the temperature information from the hdf file.
        :type temperature: float/list/dict
        :param field: It gets the field information from the hdf file.
        :type field: float/list/dict

        :return: It returns an array of the complete image.
        :rtype: array
        """
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
        scene_image = scene.render(width=self.size, height=self.size, antialiasing=0.1)

        image = PlotStates.join_images(self.colorbar_image, scene_image)

        if self.index == 1:
            title = "Initial state"
        else:
            title = f"T = {temperature:.2f}; H = {field:.2f}; iteration = {iteration}"

        draw = ImageDraw.Draw(image)
        draw.text((0.2 * image.width, 0), title, (0, 0, 0), font=self.font)

        if save:
            try:
                os.mkdir(self.output)
            except FileExistsError:
                pass

            image.save(f"{self.output}/figure_{self.index}.png")

        self.index += 1

        return numpy.array(image)

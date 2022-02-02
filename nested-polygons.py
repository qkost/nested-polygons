"""
==================
nested-polygons.py
==================

Script for creating animations of nested polygons

"""

import argparse
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from pdb import set_trace as bp

RADIUS_MAX = 1
RADIUS_MIN = 0.001
"""
Minimum and maximum radii for vertices of polygons.
"""

ARG_PARSER =  argparse.ArgumentParser(description="Animates nested polygons")

ARG_PARSER.add_argument(
    "nsides",
    type=int,
    help="Number of sides of the polygon"
)

ARG_PARSER.add_argument(
    "filename",
    type=str,
    help="Output filename."
)

ARG_PARSER.add_argument(
    "--frames",
    "-f",
    type=int,
    help="Number of frames for animation. Defaults to 100.",
    default=100
)

ARG_PARSER.add_argument(
    "--colors",
    "-c",
    nargs=2,
    type=str,
    help="Colors for polygon fills. Defaults to matplotlib's C0 and C1",
    default=["C0", "C1"]
)

ARG_PARSER.add_argument(
    "--max_polygons",
    "-m",
    type=int,
    help="Maximum number of polygons to draw. Defaults to 1000",
    default=1000
)

ARG_PARSER.add_argument(
    "--delay",
    "-d",
    type=int,
    help="Delay between frames in ms. Defaults to 20 ms",
    default=20
)

ARG_PARSER.add_argument(
    "--frame_rate",
    "--fps",
    "-r",
    type=int,
    help="Video playback frame rate. Defaults to 30",
    default=30
)

ARG_PARSER.add_argument(
    "--dpi",
    type=int,
    help="Dots per inch. Defaults to 200",
    default=200
)


def polygon(nsides, radius, rotation):
    """
    Compute the points on a polygon

    Parameters
    ----------
    nsides : int
        Number of sides of the polygon
    radius : float
        Radius of polygon
    rotation : float
        Angle to rotate polygon, rad
    
    Returns
    -------
    x, y : float
        Coordinates of polygon vertices, including the first point repeated
        at the end
    """
    # Space out angles of vertices
    thetas = np.arange(0, 2 * np.pi + 1e-6, 2 * np.pi / nsides) + rotation
    x = radius * np.cos(thetas)
    y = radius * np.sin(thetas)
    return x, y


def get_radius(rotation, radius_big, nsides):
    """
    Compute the radius of a rotated polygon with corners touching the edges of
    a larger polygon

    Parameters
    ----------
    rotation : float
        Angle to rotate polygon, rad
    radius_big : float
        Radius of larger polygon which this radius will touch
    nsides : int
        Number of sides of the polygon

    Returns
    -------
    radius : float
        Radius of smaller polygon that touches the larger one
    """
    # Angle of each of the n sides of the polygon
    alpha = 2 * np.pi / nsides

    # Compute the intersection of the corner of the smaller polygon and
    # the edge of the larger polygon
    tan = np.tan((np.pi - alpha)/2)
    radius = (tan * radius_big) / (np.sin(rotation) + tan * np.cos(rotation))

    return radius


class NestedPolygons:
    """
    Animation of nested polygons

    Create animation of polygons that are nested and rotated such that inner
    polygons' vertices just touch the sides of the larger polygons.

    Attributes
    ----------
    fig : matplotlib.Figure
        Figure
    ax : matplotlib.Axis
        Axis of plot
    nsides : int
        Number of sides of the polygon
    nframes : int
         Number of frames for animation.
    colors : list
        Two element list of colors to use for polygons.
    max_polygons : int
        "Maximum number of polygons to draw.
    polygons : list
        List of all polygon options drawn
    """

    def __init__(
        self,
        nsides,
        nframes=100,
        colors=["C0", "C1"],
        max_polygons=1000,
        figsize=(8,8)
    ):
        """
        Initialize nested polygons animation

        Parameters
        ----------
        nsides : int
            Number of sides of the polygon
        nframes : int, optional
            Number of frames for animation. Defaults to 100.
        colors : list, optional
            Two element list of colors to use for polygons. Defaults to 
            matplotlib's C0 and C1"
        max_polygons : int
            "Maximum number of polygons to draw. Defaults to 1000
        figsize : tuple, optional
            Figure size. Defaults to (8, 8)
        """
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.nsides = nsides
        self.nframes = nframes
        self.colors = colors
        self.max_polygons = max_polygons
        # self.polygons = [
        #     self.ax.fill(
        #         [],
        #         [],
        #         edgecolor="black",
        #         linestyle="-",
        #         linewidth=1
        #     )[0] 
        #     for ii in range(max_polygons)
        # ]
        self.polygons = self.create_polygons()

        # Some formatting
        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.fig.tight_layout()
    
    def create_polygons(self):
        """
        Creates template polygons

        Returns
        -------
        polygon_artists : list
            List of all polygon options drawn
        """
        polygon_artists = []
        for ii in range(self.max_polygons):
            # Get color for this polygon
            if ii < (self.max_polygons - 1):
                color = self.colors[ii % len(self.colors)]
            else:
                color = "black"

            # Create polygon
            poly = self.ax.fill(
                [],
                [],
                facecolor=color,
                edgecolor="black",
                linestyle="-",
                linewidth=1
            )[0]
            polygon_artists.append(poly)
        return polygon_artists

    
    def frame_to_rotation(self, frame):
        """
        Computes rotation of a given frame

        Parameters
        ----------
        frame : int
            Frame number
        
        Returns
        -------
        rotation : float
            Rotation of each nested polygon, float
        """
        return (frame / self.nframes) * (2 * np.pi / self.nsides)

    def draw_frame(self, frame):
        """
        Draws frame

        Parameters
        ----------
        frame : int
            Frame number
        """

        # Compute rotation for this frame
        drotation = self.frame_to_rotation(frame)
        # print(drotation / (2 * np.pi / self.nsides))

        # Initialize outer radius
        radius_outer = RADIUS_MAX

        last = self.max_polygons
        for ipoly in range(self.max_polygons):
            # Update rotation
            rotation = drotation * ipoly

            # Compute radius
            radius = get_radius(drotation, radius_outer, self.nsides)

            # Get a polygon
            poly = polygon(self.nsides, radius, rotation)

            # Update plot
            self.polygons[ipoly].set_xy(np.array(poly).T)

            # Update previous radius
            radius_outer = radius

            # Exit if radius is too small
            if radius < RADIUS_MIN or drotation == 0:
                last = ipoly
                break

            
        
        for poly in self.polygons[last::]:
            poly.set_xy(np.nan * np.zeros((1, 2)))

        return self.polygons


def create_polygon_animation(
    nsides,
    filename,
    nframes,
    colors,
    max_polygons,
    delay,
    frame_rate,
    dpi
):
    """
    Creates and saves polygon animation

    Parameters
    ----------
    nsides : int
        Number of sides of the polygon
    filename : str
        Filename to save video at. Must be a valid file extension supported
        by ffmpeg
    nframes : int
        Number of frames for animation.
    colors : list
        Two element list of colors to use for polygons.
    max_polygons : int
        "Maximum number of polygons to draw.
    delay : int
        Delay between frames
    frame_rate : int
        Number of frames per second for playback
    dpi : int
        Number of dots per inch
    """
    poly = NestedPolygons(
        nsides,
        nframes=nframes,
        colors=colors,
        max_polygons=max_polygons
    )

    
    # calling the animation function    
    anim = animation.FuncAnimation(
        poly.fig,
        poly.draw_frame,
        frames = nframes,
        interval=delay,
        # blit=True
    )
    
    # Save animation
    anim.save(filename, writer="ffmpeg", fps=frame_rate, dpi=dpi)

if __name__ == "__main__":
    ARGS = ARG_PARSER.parse_args()
    create_polygon_animation(
        ARGS.nsides,
        ARGS.filename,
        ARGS.frames,
        ARGS.colors,
        ARGS.max_polygons,
        ARGS.delay,
        ARGS.frame_rate,
        ARGS.dpi
    )

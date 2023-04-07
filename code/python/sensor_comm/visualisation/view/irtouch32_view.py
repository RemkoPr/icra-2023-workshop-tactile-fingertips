import tkinter
import numpy as np

from visualisation.view.hex_grid_plot import HexGridPlot


class IRTouch32View(HexGridPlot):
    def __init__(self, devices=None, grid_size=(5, 4, 5, 4, 5, 4, 5), disp_vals=True, c1='#434A52', c2='#7DB5A8'):
        super().__init__(devices=devices, grid_size=grid_size, disp_vals=disp_vals, c1=c1, c2=c2)

        def edge_marker():
            edge_marker = self.canvas.create_oval(
                0 - self.edge_marker_width / 2,
                0 - self.edge_marker_width / 2,
                0 + self.edge_marker_width / 2,
                0 + self.edge_marker_width / 2,
                fill="#D6AE72", state=tkinter.HIDDEN
            )
            return edge_marker

        self.edge_marker_width = 10
        self.num_edge_markers_per_device = 3 * 12 + 3 * 11  # TODO: derive from grid_size
        self.edge_markers = {device: [edge_marker() for _ in range(self.num_edge_markers_per_device)] for device in
                             devices}  # edge marker items are preallocated and made visible/positioned as needed
        self.edge_marker_centrepoints = {device: [] for device in devices}

        def edge(width=1):
            edge = self.canvas.create_line(0, 0, 0, 0, fill="#D6AE72", width=width)
            return edge
        self.edges = {device: edge(width=3) for device in devices}
        self.edge_len = len(self.grid_size) * self.cell_width
        self.edges_params = {device: (0, 0, 0) for device in devices}

        self.corner_edges = {device: [edge() for _ in range(2)] for device in devices}
        self.corner_params = {device: (0, 0, 0, 0) for device in devices}

        self.darkness_centrepoints = {device: (0, 0) for device in devices}
        self.darkness_centrepoint_width = 20
        self.darkness_centrepoint_indicators = {
            device: self.canvas.create_oval(-self.darkness_centrepoint_width / 2, -self.darkness_centrepoint_width / 2,
                                            self.darkness_centrepoint_width, self.darkness_centrepoint_width,
                                            fill="#6595BF") for device in devices}

        self.redraw()

    def redraw(self):
        for device in self.devices:
            # Darkness centrepoint
            darkness_centrepoint = self.darkness_centrepoint_indicators[device]
            if self.darkness_centrepoints[device]:
                self.canvas.moveto(darkness_centrepoint,
                                   x=self.darkness_centrepoints[device][0] - self.darkness_centrepoint_width / 2,
                                   y=self.darkness_centrepoints[device][1] - self.darkness_centrepoint_width / 2)
                self.canvas.itemconfig(darkness_centrepoint, state=tkinter.NORMAL)
            else:
                self.canvas.itemconfig(darkness_centrepoint, state=tkinter.HIDDEN)

            # Edge markers
            for marker in self.edge_markers[device]:
                self.canvas.itemconfig(marker, state=tkinter.HIDDEN)
            for i, edge_marker_coords in enumerate(self.edge_marker_centrepoints[device]):
                edge_marker = self.edge_markers[device][i]
                self.canvas.itemconfig(edge_marker, state=tkinter.NORMAL)
                self.canvas.moveto(edge_marker, edge_marker_coords[0] - self.edge_marker_width / 2,
                                   edge_marker_coords[1] - self.edge_marker_width / 2)

            # Straight edges
            edge = self.edges[device]
            x0, y0, angle = self.edges_params[device]
            self.canvas.coords(edge, x0 - self.edge_len * np.cos(angle * np.pi / 180) / 2,
                               y0 - self.edge_len * np.sin(angle * np.pi / 180) / 2,
                               x0 + self.edge_len * np.cos(angle * np.pi / 180) / 2,
                               y0 + self.edge_len * np.sin(angle * np.pi / 180) / 2)

            # Corner edges
            edge_len = 300
            line1 = self.corner_edges[device][0]
            line2 = self.corner_edges[device][1]
            x0, y0, angle1, angle2 = self.corner_params[device]
            self.canvas.coords(line1, x0, y0, x0 + edge_len * np.cos(angle1 * np.pi / 180),
                               y0 + edge_len * np.sin(angle1 * np.pi / 180))
            self.canvas.coords(line2, x0, y0, x0 + edge_len * np.cos(angle2 * np.pi / 180),
                               y0 + edge_len * np.sin(angle2 * np.pi / 180))

        super(IRTouch32View, self).redraw()

import asyncio

from sensor_comm.utils.data_handler import *
from sensor_comm.utils.general import data_bytes_to_uint16


class SensorGroup:
    """
    Sensor base class
    """

    def __init__(self, devices, viewmodel=None, data_handler=None, comm_handler=None):
        self.devices = devices
        self.viewmodel = viewmodel
        self.data_handler = data_handler
        self.comm_handler = comm_handler
        self.current_data = None  # TODO: make sure that unused, remove

    async def subscribe_to_devices(self, visualiser_delay=0.05):
        """
        subscribes to notifications on the data characteristic published by each sensor and optionally plots the data
        """
        await self.comm_handler.connect_devices()
        await self.comm_handler.subscribe_devices()

        if self.viewmodel:
            while True:
                await asyncio.sleep(visualiser_delay)
                self.viewmodel.update_view()
        else:
            await asyncio.Event().wait()

    async def read_devices(self):
        await self.comm_handler.connect_devices()
        data = await self.comm_handler.read_devices()
        await self.comm_handler.disconnect_devices()
        if self.data_handler:
            for device in self.devices:
                self.data_handler.persist(data, device)
        return data


class IRTouchGroup(SensorGroup):
    def __init__(self, devices, viewmodel=None, data_handler=None, comm_handler=None):
        super().__init__(devices, viewmodel=viewmodel, data_handler=data_handler, comm_handler=comm_handler)

    def get_current_corner_angles(self):
        return self.viewmodel.corner_fit_angles

    def get_current_corner_angle(self, device):
        return self.viewmodel.corner_fit_angles[device]

    def get_current_edge_fit_errors(self):
        return self.viewmodel.edge_fit_errors

    def get_current_edge_fit_error(self, device):
        return self.viewmodel.edge_fit_errors[device]

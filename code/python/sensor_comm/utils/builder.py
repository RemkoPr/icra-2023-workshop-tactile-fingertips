from sensor_comm.communication.bleak_comm import BleakComm
from sensor_comm.utils.sensor_uuids import SensorUuids

from sensor_comm.visualisation.viewmodel.smart_textile_viewmodel import SmartTextileViewModel
from sensor_comm.visualisation.viewmodel.irtouch_viewmodel import IRTouchViewModel
from sensor_comm.visualisation.viewmodel.irtouch32_viewmodel import IRTouch32ViewModel
from sensor_comm.visualisation.view.irtouch32_view import IRTouch32View
from sensor_comm.visualisation.viewmodel.captouch_viewmodel import CapTouchViewmodel
from sensor_comm.visualisation.viewmodel.capsense_viewmodel import CapSenseViewModel
from sensor_comm.visualisation.viewmodel.cap2sense_viewmodel import Cap2SenseViewModel
from sensor_comm.visualisation.viewmodel.poly_piezo_viewmodel import PolyPiezoViewModel
from sensor_comm.sensor_group import *


class Builder:
    @staticmethod
    def get_callbacks(devices, data_handler, viewmodel):
        def handle_data(handle, value, device, data_handler, viewmodel):
            """
            :param handle: integer characteristic read handle the data was received on
            :param value: data returned in the notification as bytearray
            :param device: hardware address (str, e.g. "D3:21:46:1B:B9:A0") of the device to which this callback belongs
            """
            data_bytes = list(value)
            data_converted = data_handler.data_convert(data_bytes)
            data_handler.current_data = data_converted
            logger.debug([device] + data_converted)
            if viewmodel:
                viewmodel.update_device_data(device, data_converted)
            if data_handler:
                data_handler.persist(data_converted, device)

        callbacks = {device: lambda handle, value, device=device:
        handle_data(handle, value, device, data_handler=data_handler, viewmodel=viewmodel) for device in devices}
        return callbacks

    @staticmethod
    def smart_textile(devices, grid_size=(7, 7), disp_vals=True, data_directory='/data/smart_textile', buffer_size=20,
                      comm_mode="BLEAK"):
        data_handler = SmartTexDataHandler(devices=devices, directory=data_directory, buffer_size=buffer_size,
                                           grid_size=grid_size)
        view = SquareGridPlot(devices=devices, grid_size=grid_size, disp_vals=disp_vals)
        viewmodel = SmartTextileViewModel(view)
        if comm_mode == "BLEAK":
            callbacks = Builder.get_callbacks(devices, data_handler, viewmodel)
            comm_handler = BleakComm(devices, callbacks, SensorUuids.DATA_CHAR_SMARTTEX.value)
        else:
            ValueError("Invalid communication mode passed")
        return SmartTextileGroup(devices, viewmodel=viewmodel, data_handler=data_handler, comm_handler=comm_handler)

    @staticmethod
    def capsense(devices, grid_size=(5, 5), disp_vals=True, data_directory='/data/capsense', buffer_size=20,
                 comm_mode="BLEAK"):
        data_handler = CapSenseDataHandler(devices=devices, directory=data_directory, buffer_size=buffer_size,
                                           grid_size=grid_size)
        view = SquareGridPlot(devices=devices, grid_size=grid_size, disp_vals=disp_vals)
        viewmodel = CapSenseViewModel(view)
        if comm_mode == "BLEAK":
            callbacks = Builder.get_callbacks(devices, data_handler, viewmodel)
            comm_handler = BleakComm(devices, callbacks, SensorUuids.DATA_CHAR_IRTOUCH.value)
        else:
            ValueError("Invalid communication mode passed")
        return CapSenseGroup(devices, viewmodel=viewmodel, data_handler=data_handler, comm_handler=comm_handler)

    @staticmethod
    def cap2sense(devices, grid_size=(5, 5), disp_vals=True, data_directory='/data/cap2sense', buffer_size=20,
                  comm_mode="BLEAK"):
        data_handler = Cap2SenseDataHandler(devices=devices, directory=data_directory, buffer_size=buffer_size,
                                            grid_size=grid_size)
        view = SquareGridPlot(devices=devices, grid_size=grid_size, disp_vals=disp_vals)
        viewmodel = Cap2SenseViewModel(view)
        if comm_mode == "BLEAK":
            callbacks = Builder.get_callbacks(devices, data_handler, viewmodel)
            comm_handler = BleakComm(devices, callbacks, SensorUuids.DATA_CHAR_CAPSENSE.value)
        else:
            ValueError("Invalid communication mode passed")
        return Cap2SenseGroup(devices, viewmodel=viewmodel, data_handler=data_handler, comm_handler=comm_handler)

    @staticmethod
    def captouch(devices, cins, grid_size=(3, 2), disp_vals=True, data_directory='/data/captouch', buffer_size=20,
                 comm_mode="BLEAK"):
        data_handler = CapTouchDataHandler(devices=devices, cins=cins, directory=data_directory,
                                           buffer_size=buffer_size, grid_size=grid_size)
        view = SquareGridPlot(devices=devices, grid_size=grid_size, disp_vals=disp_vals)
        viewmodel = CapTouchViewmodel(view)
        if comm_mode == "BLEAK":
            callbacks = Builder.get_callbacks(devices, data_handler, viewmodel)
            comm_handler = BleakComm(devices, callbacks, SensorUuids.DATA_CHAR_IRTOUCH.value)
        else:
            ValueError("Invalid communication mode passed")
        return CapTouchGroup(devices, cins, viewmodel=viewmodel, data_handler=data_handler, comm_handler=comm_handler)

    @staticmethod
    def irtouch(devices, grid_size=(2, 2), disp_vals=True, data_directory='/data/irtouch', buffer_size=20,
                comm_mode="BLEAK"):
        data_handler = IRTouchDataHandler(devices=devices, directory=data_directory, buffer_size=buffer_size,
                                          grid_size=grid_size)
        view = SquareGridPlot(devices=devices, grid_size=grid_size, disp_vals=disp_vals)
        viewmodel = IRTouchViewModel(view)
        if comm_mode == "BLEAK":
            callbacks = Builder.get_callbacks(devices, data_handler, viewmodel)
            comm_handler = BleakComm(devices, callbacks, SensorUuids.DATA_CHAR_CAPSENSE.value)
        else:
            ValueError("Invalid communication mode passed")
        return IRTouchGroup(devices, viewmodel=viewmodel, data_handler=data_handler, comm_handler=comm_handler)

    @staticmethod
    def irtouch32(devices, grid_size=(5, 4, 5, 4, 5, 4, 5), disp_vals=True, data_directory='/data/irtouch', buffer_size=20,
                comm_mode="BLEAK"):
        data_handler = IRTouchDataHandler(devices=devices, directory=data_directory, buffer_size=buffer_size,
                                          grid_size=grid_size)
        view = IRTouch32View(devices=devices, grid_size=grid_size, disp_vals=disp_vals)
        viewmodel = IRTouch32ViewModel(view)
        if comm_mode == "BLEAK":
            callbacks = Builder.get_callbacks(devices, data_handler, viewmodel)
            comm_handler = BleakComm(devices, callbacks, SensorUuids.DATA_CHAR_IRTOUCH.value)
        else:
            ValueError("Invalid communication mode passed")
        return IRTouchGroup(devices, viewmodel=viewmodel, data_handler=data_handler, comm_handler=comm_handler)

    @staticmethod
    def poly_piezo(devices, grid_size=(5, 5), disp_vals=True, data_directory='/data/poly_piezo', buffer_size=20,
                      comm_mode="BLEAK"):
        data_handler = PolyPiezoDataHandler(devices=devices, directory=data_directory, buffer_size=buffer_size,
                                           grid_size=grid_size)
        view = SquareGridPlot(devices=devices, grid_size=grid_size, disp_vals=disp_vals)
        viewmodel = PolyPiezoViewModel(view)
        if comm_mode == "BLEAK":
            callbacks = Builder.get_callbacks(devices, data_handler, viewmodel)
            comm_handler = BleakComm(devices, callbacks, SensorUuids.DATA_CHAR_POLYPIEZO.value)
        else:
            ValueError("Invalid communication mode passed")
        return PolyPiezoGroup(devices, viewmodel=viewmodel, data_handler=data_handler, comm_handler=comm_handler)

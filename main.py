from calib3d import Calibration

calib = Calibration()
calib.read_measurements()
calib.fix_steps()
calib.show_steps()

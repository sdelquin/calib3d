from calib3d import Calibration

calib = Calibration()
calib.read_measurements()
calib.calculate_errors()
calib.fix_steps()
calib.show_steps()

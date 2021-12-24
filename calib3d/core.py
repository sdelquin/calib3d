import datetime
from pathlib import Path

import yaml

import settings
from calib3d import display


class Calibration:
    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        config_file: Path = settings.CONFIG_FILE,
        history_file: Path = settings.HISTORY_FILE,
    ):
        self.measurements = {'X': x, 'Y': y, 'Z': z}
        self.config_file = config_file
        self.history_file = history_file
        self.config = yaml.load(config_file.read_text(), Loader=yaml.FullLoader)

    def calculate_errors(self):
        calcube_side = self.config['calcube']['side']
        self.errors, self.valid_errors = {}, {}
        for axis, measurement in self.measurements.items():
            self.errors[axis] = measurement - calcube_side
            self.valid_errors[axis] = (
                abs(self.errors[axis]) <= self.config['calcube']['valid-error']
            )

    def fix_steps(self):
        self.steps = {}
        for axis, measurement in self.measurements.items():
            if self.valid_errors[axis]:
                result = self.config['steps'][axis]
            else:
                result = (
                    self.config['calcube']['side']
                    * self.config['steps'][axis]
                    / measurement
                )
            self.steps[axis] = result

    def update_steps(self):
        self.config['steps'] = self.steps
        # Fix floating point issues
        for axis in self.config['steps']:
            self.config['steps'][axis] = round(self.config['steps'][axis], 2)
        output = yaml.dump(self.config, Dumper=yaml.Dumper)
        self.config_file.write_text(output)

    def dump_history(self):
        if not self.history_file.exists():
            self.history_file.write_text('at,X_steps,Y_steps,Z_steps,X_dim,Y_dim,Z_dim\n')
        with self.history_file.open('a') as f:
            buffer = [datetime.datetime.now().isoformat(timespec='minutes')]
            buffer += (str(v) for v in self.config['steps'].values())
            buffer += (str(v) for v in self.measurements.values())
            f.write(','.join(buffer) + '\n')

    def show_results(self, show_gcode=False, show_details=False):
        display.Display(self, show_gcode, show_details).print()

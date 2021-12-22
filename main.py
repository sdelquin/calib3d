import typer

from calib3d import Calibration

app = typer.Typer(add_completion=False)


@app.command()
def run(
    x: float = typer.Option(
        ..., '-X', help='Current measure (mm) for X axis from calibration cube'
    ),
    y: float = typer.Option(
        ..., '-Y', help='Current measure (mm) for Y axis from calibration cube'
    ),
    z: float = typer.Option(
        ..., '-Z', help='Current measure (mm) for Z axis from calibration cube'
    ),
):
    calib = Calibration(x, y, z)
    calib.calculate_errors()
    calib.fix_steps()
    calib.show_results()


if __name__ == "__main__":
    app()
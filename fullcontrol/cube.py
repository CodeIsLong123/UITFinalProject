import fullcontrol as fc
from mpmath import ellipfun
from math import sqrt, asin, sin, cos, tau, pi
import numpy as np

    
steps = []
side = 18
offset = 3

hover_height=10

cube = fc.squarewaveXY(fc.Point(x=-side/2, y=0, z=0), fc.Vector(x=1, y=0), side, offset, int(side/offset)//2, True)
cube.extend(fc.squarewaveXY(fc.Point(x=side/2, y=side, z=offset), fc.Vector(x=0, y=-1), -side, offset, int(side/offset)//2, True))
cube = fc.move(cube, fc.Vector(z=offset*2), copy=True, copy_quantity=side//offset//2)
cube = fc.move(cube, fc.Vector(z=hover_height), copy=False)

steps.append(fc.ExtrusionGeometry(area_model='rectangle', width=2, height=2))
steps.append(fc.Printer(print_speed=300, travel_speed=3000))
steps.append(fc.Fan(speed_percent=0))

# start by adhering to the baseplate
steps.append(fc.Point(x=-side/2-5, y=0, z=0))
steps.append(fc.Point(x=-side/2, y=0, z=0))

#start cube
steps.extend(cube)

# Visualise:
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


vector = fc.Vector(x=100, y=100, z=0.0)
steps = fc.move(steps, vector)

# Save for printer:
initial_settings = {
    "print_speed_percent": 100,
    "material_flow_percent": 100,
    "nozzle_temp": 250,
    "bed_temp": 90,
    "fan_percent": 100,
    "extrusion_width": 0.8,
    "extrusion_height": 0.3,
#    "e_units": "mm3",
#    "relative_e": False,
#    "dia_feed": 2.85,
}
gcode_controls = fc.GcodeControls(printer_name='ender_3', save_as='cube', initialization_data=initial_settings)


fc.transform(steps, 'gcode', gcode_controls)


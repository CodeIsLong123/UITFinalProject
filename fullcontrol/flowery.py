import fullcontrol as fc

from math import sin, cos, tau
steps = []
for i in range(20000):
    angle = tau*i/200
    offset = (3*(i/10000)**2)*cos(angle*6)
    steps.append(fc.Point(x=(50+offset)*sin(angle), y=(50+offset)*cos(angle), z=((i/200)*0.3)-offset/2))

# Visualise:
fc.transform(steps, 'plot', fc.PlotControls(style='line'))


vector = fc.Vector(x=100, y=100, z=0.0)
steps = fc.move(steps, vector)

# Save for printer:
initial_settings = {
#    "print_speed_percent": 100,
#    "material_flow_percent": 100,
    "nozzle_temp": 220,
    "bed_temp": 50,
    "fan_percent": 100,
    "extrusion_width": 0.8,
    "extrusion_height": 0.3,
#    "e_units": "mm3",
#    "relative_e": False,
#    "dia_feed": 2.85,
}
gcode_controls = fc.GcodeControls(printer_name='ender_3', save_as='haha', initialization_data=initial_settings)


fc.transform(steps, 'gcode', gcode_controls)


import fullcontrol as fc
from mpmath import ellipfun
from math import sqrt, asin, sin, cos, tau, pi
import numpy as np

def spherical_spiral_simple(radius=10.0, resolution=0.5, revolutions=3):
    # Calculate total angle range
    a_max = revolutions * 2 * np.pi
    
    # Estimate number of points based on circumference and resolution
    total_path_length = 2 * np.pi * radius * revolutions  # Rough estimate
    num_points = int(total_path_length / resolution)
    
    # Generate points with uniform angular spacing
    a_values = np.linspace(0, a_max, num_points)
    
    points = []
    for a in a_values:
        # Map angle to latitude (from north pole to south pole)
        theta = np.pi/2 - (a/a_max) * np.pi
        phi = a  # Azimuthal angle
        
        x = radius * np.cos(phi) * np.cos(theta)
        y = radius * np.sin(phi) * np.cos(theta)
        z = radius * np.sin(theta) 
        
        points.append(fc.Point(x=x, y=y, z=z))
    
    return reversed(points)

    
steps = []
steps.append(fc.ExtrusionGeometry(area_model='rectangle', width=2, height=2))
steps.append(fc.Printer(print_speed=300, travel_speed=3000))
steps.append(fc.Fan(speed_percent=0))

# start by adhering to the baseplate
steps.append(fc.Point(x=0-5, y=0, z=0))
steps.append(fc.Point(x=0, y=0, z=0))

sphere = spherical_spiral_simple(radius=30, revolutions=40)
#sphere = fc.move(sphere, fc.Vector(z=30), copy=False)
sphere = fc.move(sphere, fc.Vector(z=40), copy=False)
steps.extend(sphere)


# Visualise:
fc.transform(steps, 'plot', fc.PlotControls(style='line', color_type='print_sequence'))


vector = fc.Vector(x=100, y=100, z=0.0)
steps = fc.move(steps, vector)

# Save for printer:
initial_settings = {
#    "print_speed_percent": 100,
#    "material_flow_percent": 100,
    "nozzle_temp": 250,
    "bed_temp": 90,
    "fan_percent": 100,
    "extrusion_width": 0.8,
    "extrusion_height": 0.3,
#    "e_units": "mm3",
#    "relative_e": False,
#    "dia_feed": 2.85,
}
gcode_controls = fc.GcodeControls(printer_name='ender_3', save_as='ball', initialization_data=initial_settings)


fc.transform(steps, 'gcode', gcode_controls)


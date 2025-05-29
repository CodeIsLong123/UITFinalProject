import fullcontrol as fc

offset = 3
steps=[]

def horizontal(w, speed, relative):
    # max_width = 7.6
    # max area = 7.6 * 0.3 = 2.28
    steps.append(fc.Printer(print_speed=speed, travel_speed=3000))
    for i in range(70):
        steps.append(fc.ExtrusionGeometry(area_model='rectangle', width=w+i*0.2, height=0.3))
        steps.append(fc.Point(x=relative.x + i*offset, y=relative.y+0, z=relative.z+0))

38*0.2


def vertical(w, relative):
    steps.append(fc.ExtrusionGeometry(area_model='rectangle', width=1.5, height=1.5))
    steps.append(fc.Printer(print_speed=100, travel_speed=3000))
    for i in range(70):
        steps.append(fc.Point(x=relative.x + 0, y=relative.y+0, z=relative.z+(i)))


vector1 = fc.Point(x=20, y=100, z=1.0)
steps.extend(fc.travel_to(vector1))
horizontal(0, 500, vector1)

vector2 = fc.Point(x=20, y=50, z=1.0)
steps.extend(fc.travel_to(vector2))
horizontal(0, 200, vector2)

vector3 = fc.Point(x=60, y=20, z=0.0)
steps.extend(fc.travel_to(vector3))
vertical(200, vector3)

steps.append(fc.Hotend(temp=275, wait=True))

vector1 = fc.Point(x=20, y=-100, z=1.0)
steps.extend(fc.travel_to(vector1))
horizontal(0, 500, vector1)

vector2 = fc.Point(x=20, y=-50, z=1.0)
steps.extend(fc.travel_to(vector2))
horizontal(0, 200, vector2)

#vector3 = fc.Point(x=20, y=20, z=0.0)
#steps.extend(fc.travel_to(vector3))
#vertical(1, vector3)
#
#vector3 = fc.Point(x=40, y=20, z=0.0)
#steps.extend(fc.travel_to(vector3))
#vertical(3, vector3)

vector3 = fc.Point(x=60, y=20, z=0.0)
steps.extend(fc.travel_to(vector3))
vertical(200, vector3)
# Visualise:
#fc.transform(steps, 'plot', fc.PlotControls(style='line'))
fc.transform(steps, 'plot', fc.PlotControls(color_type='print_sequence', style="tube", tube_type="flow")) # default tube_type="flow"
#fc.transform(steps + [fc.PlotAnnotation(label='tube_type="cylinders" (view from above to see clearly)')], 'plot', fc.PlotControls(color_type='print_sequence', tube_type="cylinders"))

# Save for printer:
initial_settings = {
    "print_speed_percent": 100,
#    "material_flow_percent": 100,
    "nozzle_temp": 220,
    "bed_temp": 50,
    "fan_percent": 100,
    "extrusion_width": 0.8,
    "extrusion_height": 0.3,
    "e_units": "mm3",
#    "relative_e": False,
#    "dia_feed": 2.85,
}

user_input = input("Do you want to save? (yes/no): ")
if user_input.lower() in ["yes", "y"]:
    print("Saving file...")
    gcode_controls = fc.GcodeControls(printer_name='ender_3', save_as='thick', initialization_data=initial_settings)
    fc.transform(steps, 'gcode', gcode_controls)
else:
    print("Exiting...")


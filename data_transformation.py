import pickle
from lap_class import Laps
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def load_raw_data(file_name):
    with open(file_name, 'rb') as file:
        data = pickle.load(file)
        return data


def extract_time_data(raw_data: list) -> list:
    callibrated_time_data = []
    for (index, data) in enumerate(raw_data):
        time_data = data[1]
        try:
            decoded_time_data = time_data.decode('utf-16le', errors="ignore")
            time_parts = decoded_time_data.split(':')
            minute = time_parts[0]
            second = time_parts[1]
            millisecond = time_parts[2]
            total_time = float(minute) * 60 + float(second) + float(millisecond) * 1 / 100
            callibrated_time_data.append(total_time)
        except ValueError:
            continue

    return callibrated_time_data


def extract_data_indices(time_data: list) -> list:
    indices = [index for index, time in enumerate(time_data) if time == 0]
    last_index = -1
    indices.append(last_index)
    return indices


def create_laps(raw_data: list) -> list:
    lap_objects = []
    callibrated_time_data: list = extract_time_data(raw_data)
    lap_time_indices = extract_data_indices(callibrated_time_data)
    for lap in range(len(lap_time_indices) - 1):
        lap_object = Laps()
        lap_object.lap_number = lap
        lap_objects.append(lap_object)
    return lap_objects


def store_lap_data(raw_data: list) -> list:
    time_data = extract_time_data(raw_data)
    lap_objects: list = create_laps(raw_data)
    data_indices = extract_data_indices(time_data)
    for i in range(len(lap_objects)):
        try:
            current_data_index = data_indices[i]
            next_data_index = data_indices[i+1]
            relevant_lap_data = raw_data[current_data_index:next_data_index]
            lap_objects[i].current_lap_time = time_data[current_data_index:next_data_index]
            for data in relevant_lap_data:
                lap_objects[i].gas.append(data[2])
                lap_objects[i].brake.append(data[3])
                lap_objects[i].fuel.append(data[4])
                lap_objects[i].gear.append(data[5])
                lap_objects[i].rpm.append(data[6])
                lap_objects[i].steerAngle.append(data[7])
                lap_objects[i].speed_kph.append(data[8])
                lap_objects[i].tyre_coords.append(data[9])
            continue
        except IndexError:
            break

    return lap_objects


def plot_speed_time(lap, time_intervals: list, speed: list):
    x_axis = time_intervals
    y_axis = speed
    title = f"Speed-Time Plot: Lap {lap}"

    plt.plot(x_axis, y_axis)
    plt.title(title)
    plt.grid()
    plt.xlabel("Time (s)")
    plt.ylabel("Speed (kph)")
    plt.show()


def plot_gas_brake_time(lap, time_intervals: list, gas: list, brake: list):
    x_axis = time_intervals
    y1_axis = gas
    y2_axis = brake
    title = f"Speed-Time Plot: Lap {lap}"

    plt.plot(x_axis, y1_axis, label="Gas", color="green")
    plt.plot(x_axis, y2_axis, label="Brake", color="red")
    plt.title(title)
    plt.grid()
    plt.legend()
    plt.xlabel("Time (s)")
    plt.ylabel("Gas/Brake (%)")
    plt.show()


def plot_steerAngle_time(lap, time_intervals: list, steerAngle: list):
    x_axis = time_intervals
    y_axis = steerAngle
    title = f"Speed-Time Plot: Lap {lap}"

    plt.plot(x_axis, y_axis)
    plt.title(title)
    plt.grid()
    plt.xlabel("Time (s)")
    plt.ylabel("Steering Angle (% lock)")
    plt.show()


def interp_car_loc(laps: list) -> list:

    tyre_coords = [laps[i].tyre_coords for i, lap in enumerate(laps)]

    for lap, lap_coords in enumerate(tyre_coords):
        lap_car_centroid = []
        for coords in lap_coords:
            x_coords = coords[0::3]
            y_coords = coords[1::3]
            z_coords = coords[2::3]

            x_mean = sum(x_coords) / len(x_coords)
            y_mean = sum(y_coords) / len(y_coords)
            z_mean = sum(z_coords) / len(z_coords)

            car_centroid = (x_mean, y_mean, z_mean)
            lap_car_centroid.append(car_centroid)

        laps[lap].car_centroid = lap_car_centroid
        print("Lap Complete")
        continue

    return laps

def plot_racing_line(car_centroid: list[tuple]):
    x_coords = []
    y_coords = []
    for step_index, coords in enumerate(car_centroid):
        y_coords.append(coords[0])
        x_coords.append(coords[2])

    fig, ax = plt.subplots()
    ax.plot(x_coords, y_coords)
    ax.set_aspect('equal')
    plt.show()


# def colour_param(gas: list, brake: list) -> list:
#     colour_param = [gas - brake for gas, brake in zip(gas, brake)]
#     colours = plt.cm.viridis(colour_param)
#
#     return colours



"""
Functions we need:
 - Create a coordinates plan of the 4 tyres. Perhaps interpolate to get the centroid coordinate of the car
 - Figure out how the data file name will be formatted
"""

file_name = "data.pkl"
raw_data = load_raw_data(file_name)
time_data = extract_time_data(raw_data)
laps = store_lap_data(raw_data)
interp_car_loc(laps)
car_centroid = laps[1].car_centroid
gas = laps[1].gas
brake = laps[1].brake
# colours = colour_param(gas, brake)
# plot_racing_line(car_centroid)



# print(laps[-1].tyre_coords[-1])
# plot_speed_time(laps[0].lap_number, laps[0].current_lap_time, laps[0].speed_kph)
# plot_gas_brake_time(laps[0].lap_number, laps[0].current_lap_time, laps[0].gas, laps[0].brake)
# plot_steerAngle_time(laps[0].lap_number, laps[0].current_lap_time, laps[0].steerAngle)

"""
After all the minimum viable information has been organised -> Create a user interface
UI can either be a local app or a web app
or could the data collection part be a local app that runs in the background?
Web app could be a place where people can sign up and upload their telemetry data and view useful insights

"""

import mmap
import struct
import psutil
from lap_class import Laps
import json
import pickle

buffer_size_physics = 704
buffer_size_graphics = 944
buffer_size_static = 820


def get_physics_shared_mem(buffer_size=buffer_size_physics, game_API="acpmf_physics"):

    physics_shared_mem = mmap.mmap(-1, length=buffer_size, access=mmap.ACCESS_READ, offset=0,
                                   tagname=game_API)

    if not physics_shared_mem:
        raise Exception(f'Could not access shared memory object: {game_API}')
    else:
        return physics_shared_mem


def get_physics_data(shared_memory) -> tuple:

    physics_data = shared_memory.read(buffer_size_physics)
    data_format_string = (
                            'I' +                     # packetId
                            'f' +                     # gas
                            'f' +                     # brake
                            'f' +                     # fuel
                            'I' +                     # gear
                            'I' +                     # rpms
                            'f' +                     # steerAngle
                            'f' +                     # speedKmh
                            '3f' +                    # velocity[3]
                            '3f' +                    # accG[3]
                            '4f' +                    # wheelSlip[4]
                            '4f' +                    # wheelLoad[4]
                            '4f' +                    # wheelsPressure[4]
                            '4f' +                    # wheelAngularSpeed[4]
                            '4f' +                    # tyreWear[4]
                            '4f' +                    # tyreDirtyLevel[4]
                            '4f' +                    # tyreCoreTemperature[4]
                            '4f' +                    # camberRAD[4]
                            '4f' +                    # suspensionTravel[4]
                            'f' +                     # drs
                            'f' +                     # tc
                            'f' +                     # heading
                            'f' +                     # pitch
                            'f' +                     # roll
                            'f' +                     # cgHeight
                            '5f' +                    # carDamage[5]
                            'I' +                     # numberOfTyresOut
                            'I' +                     # pitLimiterOn
                            'f' +                     # abs
                            'f' +                     # kersCharge
                            'f' +                     # kersInput
                            'I' +                     # autoShifterOn
                            '2f' +                    # rideHeight[2]
                            'f' +                     # turboBoost
                            'f' +                     # ballast
                            'f' +                     # airDensity
                            'f' +                     # airTemp
                            'f' +                     # roadTemp
                            '3f' +                    # localAngularVel[3]
                            'f' +                     # finalFF
                            'f' +                     # performanceMeter
                            'I' +                     # engineBrake
                            'I' +                     # ersRecoveryLevel
                            'I' +                     # ersPowerLevel
                            'I' +                     # ersHeatCharging
                            'I' +                     # ersIsCharging
                            'f' +                     # kersCurrentKJ
                            'I' +                     # drsAvailable
                            'I' +                     # drsEnabled
                            '4f' +                    # brakeTemp[4]
                            'f' +                     # clutch
                            '4f' +                    # tyreTempI[4]
                            '4f' +                    # tyreTempM[4]
                            '4f' +                    # tyreTempO[4]
                            'I' +                     # isAIControlled
                            '4f' +                    # tyreContactPoint[4][3] (4 sets of 3 floats)
                            '4f' +                    # tyreContactNormal[4][3] (4 sets of 3 floats)
                            '4f' +                    # tyreContactHeading[4][3] (4 sets of 3 floats)
                            'f' +                     # brakeBias
                            '3f' +                    # localVelocity[3]
                            'I' +                     # P2PActivations
                            'I' +                     # P2PStatus
                            'I' +                     # currentMaxRpm
                            '4f' +                    # mz[4]
                            '4f' +                    # fx[4]
                            '4f' +                    # fy[4]
                            '4f' +                    # slipRatio[4]
                            '4f' +                    # slipAngle[4]
                            'I' +                     # tcinAction
                            'I' +                     # absInAction
                            '4f' +                    # suspensionDamage[4]
                            '4f' +                    # tyreTemp[4]
                            'f' +                     # waterTemp
                            '4f' +                    # brakePressure[4]
                            'I' +                     # frontBrakeCompound
                            'I' +                     # rearBrakeCompound
                            '4f' +                    # padLife[4]
                            '4f' +                    # diskLife[4]
                            'I' +                     # ignitionOn
                            'I' +                     # starterEngineOn
                            'I' +                     # isEngineRunning
                            'f' +                     # kerbVibration
                            'f' +                     # slipVibrations
                            'f' +                     # gVibrations
                            'f'                      # absVibrations
                        )
    physics_unpacked_data = struct.unpack(data_format_string, physics_data)

    return physics_unpacked_data


def get_graphics_shared_mem(buffer_size=buffer_size_graphics, game_API="acpmf_graphics"):
    graphics_shared_mem = mmap.mmap(-1, length=buffer_size, access=mmap.ACCESS_READ, offset=0,
                                    tagname=game_API)

    if not graphics_shared_mem:
        raise Exception(f'Could not access shared memory object: {game_API}')
    else:
        return graphics_shared_mem


def get_graphics_data(shared_memory) -> tuple:
    graphics_data = shared_memory.read(buffer_size_graphics)
    data_format_string = (
                    'i'               # packetId
                    'I'               # status (assuming it's an int; adjust as needed)
                    'I'               # session (assuming it's an int; adjust as needed)
                    '15s'             # currentTime
                    '15s'             # lastTime
                    '15s'             # bestTime
                    '15s'             # split
                    'i'               # completedLaps
                    'I'               # position
                    'I'               # iCurrentTime
                    'I'               # iLastTime
                    'I'               # iBestTime
                    'f'               # sessionTimeLeft
                    'f'               # distanceTraveled
                    'I'               # isInPit
                    'I'               # currentSectorIndex
                    'I'               # lastSectorTime
                    'I'               # numberOfLaps
                    '33s'             # tyreCompound
                    'f'               # replayTimeMultiplier
                    'f'               # normalizedCarPosition
                    'I'               # activeCars
                    '60f'             # carCoordinates[60][3] - 60 sets of 3 floats
                    '60I'             # carID[60] - 60 integers
                    'I'               # playerCarID
                    'f'               # penaltyTime
                    'I'               # flag (assuming it's an int; adjust as needed)
                    'I'               # penalty (assuming it's an int; adjust as needed)
                    'I'               # idealLineOn
                    'I'               # isInPitLane
                    'f'               # surfaceGrip
                    'I'               # mandatoryPitDone
                    'f'               # windSpeed
                    'f'               # windDirection
                    'I'               # isSetupMenuVisible
                    'I'               # mainDisplayIndex
                    'I'               # secondaryDisplayIndex
                    'I'               # TC
                    'I'               # TCCut
                    'I'               # EngineMap
                    'I'               # ABS
                    'f'               # fuelXLap
                    'I'               # rainLights
                    'I'               # flashingLights
                    'I'               # lightsStage
                    'f'               # exhaustTemperature
                    'I'               # wiperLV
                    'I'               # DriverStintTotalTimeLeft
                    'I'               # DriverStintTimeLeft
                    'I'               # rainTyres
                    'I'               # sessionIndex
                    'f'               # usedFuel
                    '15s'             # deltaLapTime
                    'I'               # iDeltaLaptime
                    '15s'             # estimatedLaptime
                    'I'               # iEstimatedLapTime
                    'I'               # isDeltaPositive
                    'I'               # isSplit
                    'I'               # isValidLap
                    'f'               # fuelEstimatedLaps
                    '33s'             # trackStatus
                    'I'               # missingMandatoryPits
                    'f'               # clock
                    'I'               # directionLightsLeft
                    'I'               # directionLightsRight
                    'I'               # GlobalYellow
                    'I'               # GlobalYellow1
                    'I'               # GlobalYellow2
                    'I'               # GlobalYellow3
                    'I'               # GlobalWhite
                    'I'               # GlobalGreen
                    'I'               # GlobalChequered
                    'I'               # GlobalRed
                    'I'               # mfdTyreSet
                    'f'               # mfdFuelToAdd
                    'f'               # mfdTyrePressureFL
                    'f'               # mfdTyrePressureFR
                    'f'               # mfdTyrePressureRL
                    'f'               # mfdTyrePressureRR
                    'I'               # trackGripStatus
                    'I'               # rainIntensity
                    'I'               # rainIntensity10min
                    'I'               # rainIntensity30min
                    'I'               # currentTyreSet
                    'I'               # strategyTyreSet
                )
    graphics_unpacked_data = struct.unpack(data_format_string, graphics_data)

    return graphics_unpacked_data


def get_static_shared_mem(buffer_size=buffer_size_static, game_API="acpmf_static"):
    static_shared_mem = mmap.mmap(-1, length=buffer_size, access=mmap.ACCESS_READ, offset=0,
                                  tagname=game_API)

    if not static_shared_mem:
        raise Exception(f'Could not access shared memory object: {game_API}')
    else:
        return static_shared_mem


def get_static_data(shared_memory) -> tuple:

    static_data = shared_memory.read(buffer_size_static)
    data_format_string = (
                    '30s'   # wchar_t smVersion[15]
                    '30s'   # wchar_t acVersion[15]
                    'i'     # int numberOfSessions
                    'i'     # int numCars
                    '66s'   # wchar_t carModel[33]
                    '66s'   # wchar_t track[33]
                    '66s'   # wchar_t playerName[33]
                    '66s'   # wchar_t playerSurname[33]
                    '66s'   # wchar_t playerNick[33]
                    'i'     # int sectorCount
                    'f'     # float maxTorque
                    'f'     # float maxPower
                    'i'     # int maxRpm
                    'f'     # float maxFuel
                    '4f'    # float suspensionMaxTravel[4]
                    '4f'    # float tyreRadius[4]
                    'f'     # float maxTurboBoost
                    'f'     # float deprecated_1
                    'f'     # float deprecated_2
                    'i'     # int penaltiesEnabled
                    'f'     # float aidFuelRate
                    'f'     # float aidTireRate
                    'f'     # float aidMechanicalDamage
                    'i'     # int aidAllowTyreBlankets
                    'f'     # float aidStability
                    'i'     # int aidAutoClutch
                    'i'     # int aidAutoBlip
                    'i'     # int hasDRS
                    'i'     # int hasERS
                    'i'     # int hasKERS
                    'f'     # float kersMaxJ
                    'i'     # int engineBrakeSettingsCount
                    'i'     # int ersPowerControllerCount
                    'f'     # float trackSPlineLength
                    '66s'   # wchar_t trackConfiguration[33]
                    'f'     # float ersMaxJ
                    'i'     # int isTimedRace
                    'i'     # int hasExtraLap
                    '66s'   # wchar_t carSkin[33]
                    'i'     # int reversedGridPositions
                    'i'     # int PitWindowStart
                    'i'     # int PitWindowEnd
                    'i'     # int isOnline
                    '66s'   # wchar_t dryTyresName[33]
                    '66s'   # wchar_t wetTyresName[33]
                )
    static_unpacked_data = struct.unpack(data_format_string, static_data)

    return static_unpacked_data


def game_is_running(game_name: str = "acc.exe"):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == game_name:
            return True
    return False


def check_status(data: tuple) -> bool:

    while data[1] == 0:
        return False
    else:
        return True


def ongoing_session(graphics_data: tuple) -> bool:
    if graphics_data[1] != 0:
        return True
    else:
        return False


def lap_finished(graphics_data: tuple) -> bool:
    current_lap = graphics_data[7]
    if graphics_data[7] == current_lap:
        return True
    else:
        current_lap += 1
        return False


def main():
    driving_data = []

    while game_is_running():
        physics_shared_mem = get_physics_shared_mem()
        graphics_shared_mem = get_graphics_shared_mem()
        static_shared_mem = get_static_shared_mem()

        graphics_data = get_graphics_data(graphics_shared_mem)
        physics_data = get_physics_data(physics_shared_mem)
        static_data = get_static_data(static_shared_mem)

        if ongoing_session(graphics_data):
            '''Can convert this section into a function for collecting data'''
            gas = physics_data[1]
            brake = physics_data[2]
            fuel = physics_data[3]
            gear = physics_data[4]
            rpm = physics_data[5]
            steerAngle = physics_data[6]
            speedkph = physics_data[7]
            current_time = graphics_data[3]
            tyre_coordinates = physics_data[105:117]
            relevant_data = [current_time, gas, brake, fuel, gear, rpm, steerAngle, speedkph, tyre_coordinates]
            driving_data.append(relevant_data)
            continue
        else:
            with open("data.pkl", "wb") as data_file:
                pickle.dump(driving_data, data_file)
            print("Session has ended or you are not in a live session. Please enter a session and re run the program.")
            break

    else:
        try:
            physics_shared_mem.close()
            graphics_shared_mem.close()
            static_shared_mem.close()
            print("ACC is not running. And the shared memories have been closed.")
        except UnboundLocalError:
            print("ACC is not running.")


main()

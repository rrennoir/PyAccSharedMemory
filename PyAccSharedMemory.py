from __future__ import annotations

import copy
import mmap
import struct
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional


class SharedMemoryTimeout(Exception):
    pass


class ACC_STATUS(Enum):

    ACC_OFF = 0
    ACC_REPLAY = 1
    ACC_LIVE = 2
    ACC_PAUSE = 3


class ACC_SESSION_TYPE(Enum):

    ACC_UNKNOW = -1
    ACC_PRACTICE = 0
    ACC_QUALIFY = 1
    ACC_RACE = 2
    ACC_HOTLAP = 3
    ACC_TIME_ATTACK = 4
    ACC_DRIFT = 5
    ACC_DRAG = 6
    ACC_HOTSTINT = 7
    ACC_HOTLAPSUPERPOLE = 8

    def __str__(self) -> str:

        if self == ACC_SESSION_TYPE.ACC_PRACTICE:
            string = "Practice"

        elif self == ACC_SESSION_TYPE.ACC_QUALIFY:
            string = "Qualify"

        elif self == ACC_SESSION_TYPE.ACC_RACE:
            string = "Race"

        elif self == ACC_SESSION_TYPE.ACC_HOTLAP:
            string = "Hotlap"

        elif self == ACC_SESSION_TYPE.ACC_TIME_ATTACK:
            string = "Time_Attack"

        elif self == ACC_SESSION_TYPE.ACC_DRIFT:
            string = "Drift"

        elif self == ACC_SESSION_TYPE.ACC_DRAG:
            string = "Drag"

        elif self == ACC_SESSION_TYPE.ACC_HOTSTINT:
            string = "Hotstint"

        elif self == ACC_SESSION_TYPE.ACC_HOTLAPSUPERPOLE:
            string = "Superpole"

        else:
            string = "Unknow"

        return string


class ACC_FLAG_TYPE(Enum):

    ACC_NO_FLAG = 0
    ACC_BLUE_FLAG = 1
    ACC_YELLOW_FLAG = 2
    ACC_BLACK_FLAG = 3
    ACC_WHITE_FLAG = 4
    ACC_CHECKERED_FLAG = 5
    ACC_PENALTY_FLAG = 6
    ACC_GREEN_FLAG = 7
    ACC_ORANGE_FLAG = 8


class ACC_PENALTY_TYPE(Enum):

    """
    Wrong way is 22 now ?
    What's 18 then ?
    Are there any other non documented enums ... ?
    """

    UnknownValue = -1
    No_penalty = 0
    DriveThrough_Cutting = 1
    StopAndGo_10_Cutting = 2
    StopAndGo_20_Cutting = 3
    StopAndGo_30_Cutting = 4
    Disqualified_Cutting = 5
    RemoveBestLaptime_Cutting = 6

    DriveThrough_PitSpeeding = 7
    StopAndGo_10_PitSpeeding = 8
    StopAndGo_20_PitSpeeding = 9
    StopAndGo_30_PitSpeeding = 10
    Disqualified_PitSpeeding = 11
    RemoveBestLaptime_PitSpeeding = 12

    Disqualified_IgnoredMandatoryPit = 13

    PostRaceTime = 14
    Disqualified_Trolling = 15
    Disqualified_PitEntry = 16
    Disqualified_PitExit = 17
    Disqualified_WrongWay_old = 18

    DriveThrough_IgnoredDriverStint = 19
    Disqualified_IgnoredDriverStint = 20

    Disqualified_ExceededDriverStintLimit = 21
    Disqualified_WrongWay = 22


class ACC_TRACK_GRIP_STATUS(Enum):

    ACC_GREEN = 0
    ACC_FAST = 1
    ACC_OPTIMUM = 2
    ACC_GREASY = 3
    ACC_DAMP = 4
    ACC_WET = 5
    ACC_FLOODED = 6

    def __str__(self) -> str:

        if self == ACC_TRACK_GRIP_STATUS.ACC_GREEN:
            string = "Green"

        elif self == ACC_TRACK_GRIP_STATUS.ACC_FAST:
            string = "Fast"

        elif self == ACC_TRACK_GRIP_STATUS.ACC_OPTIMUM:
            string = "Optimum"

        elif self == ACC_TRACK_GRIP_STATUS.ACC_GREASY:
            string = "Greasy"

        elif self == ACC_TRACK_GRIP_STATUS.ACC_DAMP:
            string = "Damp"

        elif self == ACC_TRACK_GRIP_STATUS.ACC_WET:
            string = "Wet"

        elif self == ACC_TRACK_GRIP_STATUS.ACC_FLOODED:
            string = "Flooded"

        return string


class ACC_RAIN_INTENSITY(Enum):

    ACC_NO_RAIN = 0
    ACC_DRIZZLE = 1
    ACC_LIGHT_RAIN = 2
    ACC_MEDIUM_RAIN = 3
    ACC_HEAVY_RAIN = 4
    ACC_THUNDERSTORM = 5

    def __str__(self) -> str:

        if self == ACC_RAIN_INTENSITY.ACC_NO_RAIN:
            string = "No Rain"

        elif self == ACC_RAIN_INTENSITY.ACC_DRIZZLE:
            string = "Drizzle"

        elif self == ACC_RAIN_INTENSITY.ACC_LIGHT_RAIN:
            string = "Light Rain"

        elif self == ACC_RAIN_INTENSITY.ACC_MEDIUM_RAIN:
            string = "Medium Rain"

        elif self == ACC_RAIN_INTENSITY.ACC_HEAVY_RAIN:
            string = "Heavy rain"

        elif self == ACC_RAIN_INTENSITY.ACC_THUNDERSTORM:
            string = "Thunderstorm"

        return string


@dataclass
class Vector3f:
    x: float
    y: float
    z: float

    def __str__(self) -> str:
        return f"x: {self.x}, y: {self.y}, z: {self.z}"


@dataclass
class Wheels:
    front_left: float
    front_right: float
    rear_left: float
    rear_right: float

    def __str__(self) -> str:
        return f"FL: {self.front_left}\nFR: {self.front_right}\
            \nRL: {self.rear_left}\nRR: {self.rear_right}"


@dataclass
class ContactPoint:
    front_left: Vector3f
    front_right: Vector3f
    rear_left: Vector3f
    rear_right: Vector3f

    @staticmethod
    def from_list(points: List[List[float]]) -> Any:
        fl = Vector3f(*points[0])
        fr = Vector3f(*points[1])
        rl = Vector3f(*points[2])
        rr = Vector3f(*points[3])

        return ContactPoint(fl, fr, rl, rr)

    def __str__(self) -> str:
        return f"FL: {self.front_left},\nFR: {self.front_right},\
            \nRL: {self.rear_left},\nRR: {self.rear_right}"


@dataclass
class CarDamage:
    front: float
    rear: float
    left: float
    right: float
    center: float  # Center is actually the sum of all


@dataclass
class PhysicsMap:

    packed_id: int
    gas: float
    brake: float
    fuel: float
    gear: int
    rpm: int
    steer_angle: float
    speed_kmh: float
    velocity: Vector3f
    g_force: Vector3f

    wheel_slip: Wheels
    wheel_pressure: Wheels
    wheel_angular_s: Wheels
    tyre_core_temp: Wheels

    suspension_travel: Wheels

    tc: float
    heading: float
    pitch: float
    roll: float
    car_damage: CarDamage
    pit_limiter_on: bool
    abs: float

    autoshifter_on: bool
    turbo_boost: float

    air_temp: float
    road_temp: float
    local_angular_vel: Vector3f
    final_ff: float

    brake_temp: Wheels
    clutch: float

    is_ai_controlled: bool

    tyre_contact_point: ContactPoint
    tyre_contact_normal: ContactPoint
    tyre_contact_heading: ContactPoint

    brake_bias: float

    local_velocity: Vector3f

    slip_ratio: Wheels
    slip_angle: Wheels

    suspension_damage: Wheels
    water_temp: float

    brake_pressure: Wheels
    front_brake_compound: int
    rear_brake_compound: int
    pad_life: Wheels
    disc_life: Wheels

    ignition_on: bool
    starter_engine_on: bool
    is_engine_running: bool

    kerb_vibration: float
    slip_vibration: float
    g_vibration: float
    abs_vibration: float

    @staticmethod
    def is_equal(a: PhysicsMap, b: PhysicsMap) -> bool:
        """
        Since I won't check every single attribute,
        comparing suspension_travel is a good alternative
        since there is always a bit of oscillation in the
        suspension when the car is possessed by the player.

        Parameters:
        a: PhysicsMap
        b: PhysicsMap

        Return:
        result: bool
        """

        return a.suspension_travel == b.suspension_travel


@dataclass
class GraphicsMap:

    packed_id: int
    status: ACC_STATUS
    session_type: ACC_SESSION_TYPE
    current_time_str: str
    last_time_str: str
    best_time_str: str
    last_sector_time_str: str
    completed_lap: int
    position: int
    current_time: int
    last_time: int
    best_time: int
    session_time_left: float
    distance_traveled: float
    is_in_pit: bool
    current_sector_index: int
    last_sector_time: int
    number_of_laps: int
    tyre_compound: str
    normalized_car_position: float
    active_cars: int
    car_coordinates: List[Vector3f]
    car_id: List[int]
    player_car_id: int
    penalty_time: float
    flag: ACC_FLAG_TYPE
    penalty: ACC_PENALTY_TYPE
    ideal_line_on: bool
    is_in_pit_lane: bool
    mandatory_pit_done: bool
    wind_speed: float
    wind_direction: float
    is_setup_menu_visible: bool
    main_display_index: int
    secondary_display_index: int
    tc_level: int
    tc_cut_level: int
    engine_map: int
    abs_level: int
    fuel_per_lap: float
    rain_light: bool
    flashing_light: bool
    light_stage: int
    exhaust_temp: float
    wiper_stage: int
    driver_stint_total_time_left: int
    driver_stint_time_left: int
    rain_tyres: bool
    session_index: int
    used_fuel: float
    delta_lap_time_str: str
    delta_lap_time: int
    estimated_lap_time_str: str
    estimated_lap_time: int
    is_delta_positive: bool
    last_sector_time: int
    is_valid_lap: bool
    fuel_estimated_laps: float
    track_status: str
    missing_mandatory_pits: int
    clock: float
    direction_light_left: bool
    direction_light_right: bool
    global_yellow: bool
    global_yellow_s1: bool
    global_yellow_s2: bool
    global_yellow_s3: bool
    global_white: bool
    global_green: bool
    global_chequered: bool
    global_red: bool
    mfd_tyre_set: int
    mfd_fuel_to_add: float
    mfd_tyre_pressure: Wheels
    track_grip_status: ACC_TRACK_GRIP_STATUS
    rain_intensity: ACC_RAIN_INTENSITY
    rain_intensity_in_10min: ACC_RAIN_INTENSITY
    rain_intensity_in_30min: ACC_RAIN_INTENSITY
    current_tyre_set: int
    strategy_tyre_set: int
    gap_ahead: int
    gap_behind: int


@dataclass
class StaticsMap:

    sm_version: str
    ac_version: str
    number_of_session: int
    num_cars: int
    car_model: str
    track: str
    player_name: str
    player_surname: str
    player_nick: str
    sector_count: int
    max_rpm: int
    max_fuel: float
    penalty_enabled: bool
    aid_fuel_rate: float
    aid_tyre_rate: float
    aid_mechanical_damage: float
    aid_stability: float
    aid_auto_clutch: bool
    pit_window_start: int
    pit_window_end: int
    is_online: bool
    dry_tyres_name: str
    wet_tyres_name: str


@dataclass
class ACC_map:

    Physics: PhysicsMap
    Graphics: GraphicsMap
    Static: StaticsMap


class accSM(mmap.mmap):

    def __init__(self, *args, **kwargs):
        super().__init__()

    def unpack_value(self, value_type: str, padding=0) -> float:
        bytes = self.read(4 + padding)
        format = f"={value_type}{padding}x"
        return struct.unpack(format, bytes)[0]

    def unpack_array(self, value_type: str, count: int, padding=0) -> tuple:

        if value_type in ("i", "f"):
            format = f"={count}{value_type}{padding}x"
            bytes = self.read(4 * count + padding)
            value = struct.unpack(format, bytes)

        else:
            value = self.read(2 * count + padding)

        return value

    def unpack_array2D(
            self, value_type: str, count: int, subCount: int) -> tuple:
        data = []
        for _ in range(count):
            data.append(self.unpack_array(value_type, subCount))
        return tuple(data)

    def unpack_string(self, count, padding=0) -> str:
        string_bytes = self.read(2 * count + padding)
        return string_bytes.decode("utf-16", errors="ignore")


def read_physic_map(physic_map: accSM) -> PhysicsMap:
    physic_map.seek(0)
    temp = {
        "packetID": physic_map.unpack_value("i"),

        "gas": physic_map.unpack_value("f"),
        "brake": physic_map.unpack_value("f"),
        "fuel": physic_map.unpack_value("f"),
        "gear": physic_map.unpack_value("i"),
        "rpm": physic_map.unpack_value("i"),
        "steerAngle": physic_map.unpack_value("f"),

        "speedKmh": physic_map.unpack_value("f"),
        "velocity": physic_map.unpack_array("f", 3),
        "accG": physic_map.unpack_array("f", 3),

        "wheelSlip": physic_map.unpack_array("f", 4),
        # Field is not used by ACC
        "wheelLoad": physic_map.unpack_array("f", 4),
        "wheelsPressure": physic_map.unpack_array("f", 4),
        "wheelAngularSpeed": physic_map.unpack_array("f", 4),
        # Field is not used by ACC
        "tyreWear": physic_map.unpack_array("f", 4),
        # Field is not used by ACC
        "tyreDirtyLevel": physic_map.unpack_array("f", 4),
        "tyreCoreTemperature": physic_map.unpack_array("f", 4),
        # Field is not used by ACC
        "camberRAD": physic_map.unpack_array("f", 4),
        "suspensionTravel": physic_map.unpack_array("f", 4),

        # Field is not used by ACC
        "drs": physic_map.unpack_value("i"),
        "tc": physic_map.unpack_value("f"),
        "headeing": physic_map.unpack_value("f"),
        "pitch": physic_map.unpack_value("f"),
        "roll": physic_map.unpack_value("f"),
        # Field is not used by ACC
        "cgHeight": physic_map.unpack_value("f"),
        "carDamage": physic_map.unpack_array("f", 5),
        # Field is not used by ACC
        "numberOfTyresOut": physic_map.unpack_value("i"),
        "pitLimiterOn": physic_map.unpack_value("i"),
        "abs": physic_map.unpack_value("f"),

        # Field is not used by ACC
        "kersCharge": physic_map.unpack_value("f"),
        # Field is not used by ACC
        "kersInput": physic_map.unpack_value("f"),

        "autoshifterOn": physic_map.unpack_value("i"),
        # Field is not used by ACC
        "rideHeight": physic_map.unpack_array("f", 2),
        "turboBoost": physic_map.unpack_value("f"),
        # Not implemented in ACC
        "ballast": physic_map.unpack_value("f"),
        # Field is not used by ACC
        "airDensity": physic_map.unpack_value("f"),
        "airTemp": physic_map.unpack_value("f"),
        "roadTemp": physic_map.unpack_value("f"),
        "localAngularVel": physic_map.unpack_array("f", 3),
        "FinalFF": physic_map.unpack_value("f"),
        # Field is not used by ACC
        "performanceMeter": physic_map.unpack_value("f"),

        # Field is not used by ACC
        "engineBrake": physic_map.unpack_value("i"),
        # Field is not used by ACC
        "ersRecoveryLevel": physic_map.unpack_value("i"),
        # Field is not used by ACC
        "ersPowerLevel": physic_map.unpack_value("i"),
        # Field is not used by ACC
        "ersHeatCharging": physic_map.unpack_value("i"),
        # Field is not used by ACC
        "ersIsCharging": physic_map.unpack_value("i"),
        # Field is not used by ACC
        "kersCurrentKJ": physic_map.unpack_value("f"),

        # Field is not used by ACC
        "drsAvailable": physic_map.unpack_value("i"),
        # Field is not used by ACC
        "drsEnabled": physic_map.unpack_value("i"),

        "brakeTemp": physic_map.unpack_array("f", 4),
        "clutch": physic_map.unpack_value("f"),

        # Field is not used by ACC
        "tyreTempI": physic_map.unpack_array("f", 4),
        # Field is not used by ACC
        "tyreTempM": physic_map.unpack_array("f", 4),
        # Field is not used by ACC
        "tyreTempO": physic_map.unpack_array("f", 4),

        "isAIControlled": physic_map.unpack_value("i"),

        "tyreContactPoint": physic_map.unpack_array2D("f", 4, 3),
        "tyreContactNormal": physic_map.unpack_array2D("f", 4, 3),
        "tyreContactHeading": physic_map.unpack_array2D("f", 4, 3),

        "brakeBias": physic_map.unpack_value("f"),

        "localVelocity": physic_map.unpack_array("f", 3),

        # Field is not used by ACC
        "P2PActivation": physic_map.unpack_value("i"),
        # Field is not used by ACC
        "P2PStatus ": physic_map.unpack_value("i"),

        # Field is not used by ACC
        "currentMaxRpm": physic_map.unpack_value("i"),

        # Field is not used by ACC
        "mz": physic_map.unpack_array("f", 4),
        # Field is not used by ACC
        "fz": physic_map.unpack_array("f", 4),
        # Field is not used by ACC
        "my": physic_map.unpack_array("f", 4),
        "slipRatio": physic_map.unpack_array("f", 4),
        "slipAngle": physic_map.unpack_array("f", 4),

        # Field is not used by ACC
        "tcinAction": physic_map.unpack_value("i"),
        # Field is not used by ACC
        "absinAction": physic_map.unpack_value("i"),
        # Field is not used by ACC
        "suspensionDamage": physic_map.unpack_array("f", 4),
        # Field is not used by ACC
        "tyreTemp": physic_map.unpack_array("f", 4),
        "waterTemp": physic_map.unpack_value("f"),

        "brakePressure": physic_map.unpack_array("f", 4),
        "frontBrakeCompound": physic_map.unpack_value("i"),
        "rearBrakeCompound": physic_map.unpack_value("i"),
        "padLife": physic_map.unpack_array("f", 4),
        "discLife": physic_map.unpack_array("f", 4),

        "ignitionOn": physic_map.unpack_value("i"),
        "starterEngineOn": physic_map.unpack_value("i"),
        "isEngineRunning": physic_map.unpack_value("i"),

        "kerbVibration": physic_map.unpack_value("f"),
        "slipVibrations": physic_map.unpack_value("f"),
        "gVibrations": physic_map.unpack_value("f"),
        "absVibrations": physic_map.unpack_value("f"),
    }

    return PhysicsMap(
        temp["packetID"],
        temp["gas"],
        temp["brake"],
        temp["fuel"],
        temp["gear"],
        temp["rpm"],
        temp["steerAngle"],
        temp["speedKmh"],
        Vector3f(*temp["velocity"]),
        Vector3f(*temp["accG"]),
        Wheels(*temp["wheelSlip"]),
        Wheels(*temp["wheelsPressure"]),
        Wheels(*temp["wheelAngularSpeed"]),
        Wheels(*temp["tyreCoreTemperature"]),
        Wheels(*temp["suspensionTravel"]),
        temp["tc"],
        temp["headeing"],
        temp["pitch"],
        temp["roll"],
        CarDamage(*temp["carDamage"]),
        bool(temp["pitLimiterOn"]),
        temp["abs"],
        bool(temp["autoshifterOn"]),
        temp["turboBoost"],
        temp["airTemp"],
        temp["roadTemp"],
        Vector3f(*temp["localAngularVel"]),
        temp["FinalFF"],
        Wheels(*temp["brakeTemp"]),
        temp["clutch"],
        bool(temp["isAIControlled"]),
        ContactPoint.from_list(temp["tyreContactPoint"]),
        ContactPoint.from_list(temp["tyreContactNormal"]),
        ContactPoint.from_list(temp["tyreContactHeading"]),
        temp["brakeBias"],
        Vector3f(*temp["localVelocity"]),
        Wheels(*temp["slipRatio"]),
        Wheels(*temp["slipAngle"]),
        Wheels(*temp["suspensionDamage"]),
        temp["waterTemp"],
        Wheels(*temp["brakePressure"]),
        temp["frontBrakeCompound"],
        temp["rearBrakeCompound"],
        Wheels(*temp["padLife"]),
        Wheels(*temp["discLife"]),
        bool(temp["ignitionOn"]),
        bool(temp["starterEngineOn"]),
        bool(temp["isEngineRunning"]),
        temp["kerbVibration"],
        temp["slipVibrations"],
        temp["gVibrations"],
        temp["absVibrations"],
    )


def read_graphics_map(graphic_map: accSM) -> GraphicsMap:
    graphic_map.seek(0)
    temp = {
        "packetID": graphic_map.unpack_value("i"),
        "acc_status": ACC_STATUS(graphic_map.unpack_value("i")),
        "acc_session_type": ACC_SESSION_TYPE(graphic_map.unpack_value("i")),
        "currentTime": graphic_map.unpack_string(15),
        "lastTime": graphic_map.unpack_string(15),
        "bestTime": graphic_map.unpack_string(15),
        "split": graphic_map.unpack_string(15),
        "completedLaps": graphic_map.unpack_value("i"),
        "position": graphic_map.unpack_value("i"),
        "iCurrentTime": graphic_map.unpack_value("i"),
        "iLastTime": graphic_map.unpack_value("i"),
        "iBestTime": graphic_map.unpack_value("i"),
        "sessionTimeLeft": graphic_map.unpack_value("f"),
        "distanceTraveled": graphic_map.unpack_value("f"),
        "isInPit": graphic_map.unpack_value("i"),
        "currentSectorIndex": graphic_map.unpack_value("i"),
        "lastSectorTime": graphic_map.unpack_value("i"),
        "numberOfLaps": graphic_map.unpack_value("i"),
        "tyreCompound": graphic_map.unpack_string(33, padding=2),
        # Field is not used by ACC
        "replayTimeMultiplier": graphic_map.unpack_value("f"),
        "normalizedCarPosition": graphic_map.unpack_value("f"),

        "activeCars": graphic_map.unpack_value("i"),
        "carCoordinates": graphic_map.unpack_array2D("f", 60, 3),
        "carID": graphic_map.unpack_array("i", 60),
        "playerCarID": graphic_map.unpack_value("i"),
        "penaltyTime": graphic_map.unpack_value("f"),
        "flag": ACC_FLAG_TYPE(graphic_map.unpack_value("i")),
        "penalty": penalty_workarround(graphic_map),
        "idealLineOn": graphic_map.unpack_value("i"),
        "isInPitLane": graphic_map.unpack_value("i"),
        # Return always 0
        "surfaceGrip": graphic_map.unpack_value("f"),
        "mandatoryPitDone": graphic_map.unpack_value("i"),
        "windSpeed": graphic_map.unpack_value("f"),
        "windDirection": graphic_map.unpack_value("f"),
        "isSetupMenuVisible": graphic_map.unpack_value("i"),
        "mainDisplayIndex": graphic_map.unpack_value("i"),
        "secondaryDisplyIndex": graphic_map.unpack_value("i"),
        "TC": graphic_map.unpack_value("i"),
        "TCCUT": graphic_map.unpack_value("i"),
        "EngineMap": graphic_map.unpack_value("i"),
        "ABS": graphic_map.unpack_value("i"),
        "fuelXLap": graphic_map.unpack_value("f"),
        "rainLights": graphic_map.unpack_value("i"),
        "flashingLights": graphic_map.unpack_value("i"),
        "lightStage": graphic_map.unpack_value("i"),
        "exhaustTemperature": graphic_map.unpack_value("f"),
        "wiperStage": graphic_map.unpack_value("i"),
        "driverStintTotalTimeLeft": graphic_map.unpack_value("i"),
        "driverStintTimeLeft": graphic_map.unpack_value("i"),
        "rainTyres": graphic_map.unpack_value("i"),
        "sessionIndex": graphic_map.unpack_value("i"),
        "usedFuel": graphic_map.unpack_value("f"),
        "deltaLapTime": graphic_map.unpack_string(15, padding=2),
        "ideltaLapTime": graphic_map.unpack_value("i"),
        "estimatedLapTime": graphic_map.unpack_string(15, padding=2),
        "iestimatedLapTime": graphic_map.unpack_value("i"),
        "isDeltaPositive": graphic_map.unpack_value("i"),
        "iSplit": graphic_map.unpack_value("i"),
        "isValidLap": graphic_map.unpack_value("i"),
        "fuelEstimatedLaps": graphic_map.unpack_value("f"),
        "trackStatus": graphic_map.unpack_string(33, padding=2),
        "missingMandatoryPits": graphic_map.unpack_value("i"),
        "Clock": graphic_map.unpack_value("f"),
        "directionLightsLeft": graphic_map.unpack_value("i"),
        "directionLightsRight": graphic_map.unpack_value("i"),
        "GlobalYellow": graphic_map.unpack_value("i"),
        "GlobalYellow1": graphic_map.unpack_value("i"),
        "GlobalYellow2": graphic_map.unpack_value("i"),
        "GlobalYellow3": graphic_map.unpack_value("i"),
        "GlobalWhite": graphic_map.unpack_value("i"),
        "GlobalGreen": graphic_map.unpack_value("i"),
        "GlobalChequered": graphic_map.unpack_value("i"),
        "GlobalRed": graphic_map.unpack_value("i"),
        "mfdTyreSet": graphic_map.unpack_value("i"),
        "mfdFuelToAdd": graphic_map.unpack_value("f"),
        "mfdTyrePressureFL": graphic_map.unpack_value("f"),
        "mfdTyrePressureFR": graphic_map.unpack_value("f"),
        "mfdTyrePressureRL": graphic_map.unpack_value("f"),
        "mfdTyrePressureRR": graphic_map.unpack_value("f"),
        "trackGripStatus": ACC_TRACK_GRIP_STATUS(
            graphic_map.unpack_value("i")),
        "rainIntensity": ACC_RAIN_INTENSITY(
            graphic_map.unpack_value("i")),
        "rainIntensityIn10min": ACC_RAIN_INTENSITY(
            graphic_map.unpack_value("i")),
        "rainIntensityIn30min": ACC_RAIN_INTENSITY(
            graphic_map.unpack_value("i")),
        "currentTyreSet": graphic_map.unpack_value("i"),
        "strategyTyreSet": graphic_map.unpack_value("i"),
        "gapAhead": graphic_map.unpack_value("i"),
        "gapBehind": graphic_map.unpack_value("i")
    }

    return GraphicsMap(
        packed_id=temp["packetID"],
        status=temp["acc_status"],
        session_type=temp["acc_session_type"],
        current_time_str=temp["currentTime"],
        last_time_str=temp["lastTime"],
        best_time_str=temp["bestTime"],
        last_sector_time_str=temp["lastSectorTime"],
        completed_lap=temp["completedLaps"],
        position=temp["position"],
        current_time=temp["iCurrentTime"],
        last_time=temp["iLastTime"],
        best_time=temp["iBestTime"],
        session_time_left=temp["sessionTimeLeft"],
        distance_traveled=temp["distanceTraveled"],
        is_in_pit=bool(temp["isInPit"]),
        current_sector_index=temp["currentSectorIndex"],
        last_sector_time=temp["lastSectorTime"],
        number_of_laps=temp["numberOfLaps"],
        tyre_compound=temp["tyreCompound"],
        normalized_car_position=temp["normalizedCarPosition"],
        active_cars=temp["activeCars"],
        car_coordinates=[Vector3f(*car) for car in temp["carCoordinates"]],
        car_id=temp["carID"],
        player_car_id=temp["playerCarID"],
        penalty_time=temp["penaltyTime"],
        flag=temp["flag"],
        penalty=temp["penalty"],
        ideal_line_on=bool(temp["idealLineOn"]),
        is_in_pit_lane=bool(temp["isInPitLane"]),
        mandatory_pit_done=bool(temp["mandatoryPitDone"]),
        wind_speed=temp["windSpeed"],
        wind_direction=temp["windDirection"],
        is_setup_menu_visible=bool(temp["isSetupMenuVisible"]),
        main_display_index=temp["mainDisplayIndex"],
        secondary_display_index=temp["secondaryDisplyIndex"],
        tc_level=temp["TC"],
        tc_cut_level=temp["TCCUT"],
        engine_map=temp["EngineMap"],
        abs_level=temp["ABS"],
        fuel_per_lap=temp["fuelXLap"],
        rain_light=bool(temp["rainLights"]),
        flashing_light=bool(temp["flashingLights"]),
        light_stage=temp["lightStage"],
        exhaust_temp=temp["exhaustTemperature"],
        wiper_stage=temp["wiperStage"],
        driver_stint_total_time_left=temp["driverStintTotalTimeLeft"],
        driver_stint_time_left=temp["driverStintTimeLeft"],
        rain_tyres=temp["rainTyres"],
        session_index=temp["sessionIndex"],
        used_fuel=temp["usedFuel"],
        delta_lap_time_str=temp["deltaLapTime"],
        delta_lap_time=temp["ideltaLapTime"],
        estimated_lap_time_str=temp["estimatedLapTime"],
        estimated_lap_time=temp["iestimatedLapTime"],
        is_delta_positive=bool(temp["isDeltaPositive"]),
        is_valid_lap=bool(temp["isValidLap"]),
        fuel_estimated_laps=temp["fuelEstimatedLaps"],
        track_status=temp["trackStatus"],
        missing_mandatory_pits=temp["missingMandatoryPits"],
        clock=temp["Clock"],
        direction_light_left=bool(temp["directionLightsLeft"]),
        direction_light_right=bool(temp["directionLightsRight"]),
        global_yellow=bool(temp["GlobalYellow"]),
        global_yellow_s1=bool(temp["GlobalYellow1"]),
        global_yellow_s2=bool(temp["GlobalYellow2"]),
        global_yellow_s3=bool(temp["GlobalYellow3"]),
        global_white=bool(temp["GlobalWhite"]),
        global_green=bool(temp["GlobalGreen"]),
        global_chequered=bool(temp["GlobalChequered"]),
        global_red=bool(temp["GlobalRed"]),
        mfd_tyre_set=temp["mfdTyreSet"],
        mfd_fuel_to_add=temp["mfdFuelToAdd"],
        mfd_tyre_pressure=Wheels(
            temp["mfdTyrePressureFL"],
            temp["mfdTyrePressureFR"],
            temp["mfdTyrePressureRL"],
            temp["mfdTyrePressureRR"]),
        track_grip_status=temp["trackGripStatus"],
        rain_intensity=temp["rainIntensity"],
        rain_intensity_in_10min=temp["rainIntensityIn10min"],
        rain_intensity_in_30min=temp["rainIntensityIn30min"],
        current_tyre_set=temp["currentTyreSet"],
        strategy_tyre_set=temp["strategyTyreSet"],
        gap_ahead=temp["gapAhead"],
        gap_behind=temp["gapBehind"],
    )


def read_static_map(static_map: accSM) -> StaticsMap:
    static_map.seek(0)

    temp = {
        "smVersion": static_map.unpack_string(15),
        "acVersion": static_map.unpack_string(15),
        "numberOfSessions": static_map.unpack_value("i"),
        "numCars": static_map.unpack_value("i"),
        "carModel": static_map.unpack_string(33),
        "track": static_map.unpack_string(33),
        "playerName": static_map.unpack_string(33),
        "playerSurname": static_map.unpack_string(33),
        "playerNick": static_map.unpack_string(33, 2),
        "sectorCount": static_map.unpack_value("i"),
        # Not shown in ACC
        "maxTorque": static_map.unpack_value("f"),
        # Not shown in ACC
        "maxPower": static_map.unpack_value("f"),
        "maxRpm": static_map.unpack_value("i"),
        "maxFuel": static_map.unpack_value("f"),
        # Not shown in ACC
        "suspensionMaxTravel": static_map.unpack_array("f", 4),
        # Not shown in ACC
        "tyreRadius": static_map.unpack_array("f", 4),
        # Not shown in ACC
        "maxTurboBoost": static_map.unpack_value("f"),
        "deprecated_1": static_map.unpack_value("f"),
        "deprecated_2": static_map.unpack_value("f"),
        "penaltiesEnabled": static_map.unpack_value("i"),
        "aidFuelRate": static_map.unpack_value("f"),
        "aidTireRate": static_map.unpack_value("f"),
        "aidMechanicalDamage": static_map.unpack_value("f"),
        "AllowTyreBlankets": static_map.unpack_value("f"),
        "aidStability": static_map.unpack_value("f"),
        "aidAutoClutch": static_map.unpack_value("i"),
        "aidAutoBlip": static_map.unpack_value("i"),
        # Not shown in ACC
        "hasDRS": static_map.unpack_value("i"),
        # Not shown in ACC
        "hasERS": static_map.unpack_value("i"),
        # Not shown in ACC
        "hasKERS": static_map.unpack_value("i"),
        # Not shown in ACC
        "kersMaxJ": static_map.unpack_value("f"),
        # Not shown in ACC
        "engineBrakeSettingsCount": static_map.unpack_value("i"),
        # Not shown in ACC
        "ersPowerControllerCount": static_map.unpack_value("i"),
        # Not shown in ACC
        "trackSplineLength": static_map.unpack_value("f"),
        # Not shown in ACC
        "trackConfiguration": static_map.unpack_string(33, 2),
        # Not shown in ACC
        "ersMaxJ": static_map.unpack_value("f"),
        # Not shown in ACC
        "isTimedRace": static_map.unpack_value("i"),
        # Not shown in ACC
        "hasExtraLap": static_map.unpack_value("i"),
        # Not shown in ACC
        "carSkin": static_map.unpack_string(33, 2),
        # Not shown in ACC
        "reversedGridPositions": static_map.unpack_value("i"),
        "PitWindowStart": static_map.unpack_value("i"),
        "PitWindowEnd": static_map.unpack_value("i"),
        "isOnline": static_map.unpack_value("i"),
        "dryTyresName": static_map.unpack_string(33),
        "wetTyresName": static_map.unpack_string(33)
    }

    return StaticsMap(
        temp["smVersion"],
        temp["acVersion"],
        temp["numberOfSessions"],
        temp["numCars"],
        temp["carModel"],
        temp["track"],
        temp["playerName"],
        temp["playerSurname"],
        temp["playerNick"],
        temp["sectorCount"],
        temp["maxRpm"],
        temp["maxFuel"],
        bool(temp["penaltiesEnabled"]),
        temp["aidFuelRate"],
        temp["aidTireRate"],
        temp["aidMechanicalDamage"],
        temp["aidStability"],
        bool(temp["aidAutoClutch"]),
        temp["PitWindowStart"],
        temp["PitWindowEnd"],
        bool(temp["isOnline"]),
        temp["dryTyresName"],
        temp["wetTyresName"]
    )


def penalty_workarround(graphic_map: accSM) -> ACC_PENALTY_TYPE:

    try:
        return ACC_PENALTY_TYPE(graphic_map.unpack_value("i"))

    except(ValueError):
        return ACC_PENALTY_TYPE.UnknownValue


class accSharedMemory():

    def __init__(self) -> None:

        self.physicSM = accSM(-1, 800, tagname="Local\\acpmf_physics",
                              access=mmap.ACCESS_WRITE)
        self.graphicSM = accSM(-1, 1588, tagname="Local\\acpmf_graphics",
                               access=mmap.ACCESS_WRITE)
        self.staticSM = accSM(-1, 784, tagname="Local\\acpmf_static",
                              access=mmap.ACCESS_WRITE)

        self.physics_old = None
        self.last_physicsID = 0

    def read_shared_memory(self) -> Optional[ACC_map]:

        physics = read_physic_map(self.physicSM)
        graphics = read_graphics_map(self.graphicSM)
        statics = read_static_map(self.staticSM)

        if (physics.packed_id == self.last_physicsID
                or (self.physics_old is not None
                    and PhysicsMap.is_equal(self.physics_old, physics))):
            return None

        else:
            self.physics_old = copy.deepcopy(physics)
            return ACC_map(physics, graphics, statics)

    def get_shared_memory_data(self) -> ACC_map:

        # try 1000 time to get the data, else raise exception
        for i in range(1000):

            data = self.read_shared_memory()
            if data is not None:
                return data

        else:
            raise SharedMemoryTimeout("No data available to read")

    def close(self) -> None:
        print("[ASM_Reader]: Closing memory maps.")
        self.physicSM.close()
        self.graphicSM.close()
        self.staticSM.close()


def simple_test() -> None:

    asm = accSharedMemory()

    for i in range(1000):
        sm = asm.read_shared_memory()

        if sm is not None and i % 200 == 0:
            print("Physics:")
            print(f"Pad life: {sm.Physics.pad_life}")

            print("Graphics:")
            print(f"Strategy tyre set: {sm.Graphics.penalty.name}")

            print("Static: ")
            print(f"Max RPM: {sm.Static.max_rpm}")

    asm.close()


if __name__ == "__main__":
    simple_test()

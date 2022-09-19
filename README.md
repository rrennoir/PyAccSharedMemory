# PyAccSharedMemory

ACC shared memory reader written in python 😀.

- [PyAccSharedMemory](#pyaccsharedmemory)
  - [Usage](#usage)
  - [DataClass](#dataclass)
    - [ACC_map](#acc_map)
    - [PhysicsMap](#physicsmap)
    - [GraphicsMap](#graphicsmap)
    - [StaticsMap](#staticsmap)
    - [Wheels](#wheels)
    - [CarDamage](#cardamage)
    - [Vector3f](#vector3f)
    - [ContactPoint](#contactpoint)
  - [additional information](#additional-information)
    - [Enums](#enums)
      - [ACC_STATUS](#acc_status)
      - [ACC_SESSION_TYPE](#acc_session_type)
      - [ACC_FLAG_TYPE](#acc_flag_type)
      - [ACC_PENALTY_TYPE](#acc_penalty_type)
      - [ACC_TRACK_GRIP_STATUS](#acc_track_grip_status)
      - [ACC_RAIN_INTENSITY](#acc_rain_intensity)
    - [Car Model](#car-model)
      - [GT3](#gt3)
      - [GT4](#gt4)
      - [TC](#tc)
      - [Cup cars](#cup-cars)

## Usage

Basic code example.

```py
from pyaccsharedmemory import accSharedMemory

asm = accSharedMemory()
sm = asm.read_shared_memory()

if (sm is not None):
    print("Physics:")
    print(f"Pad life: {sm.Physics.pad_life}")

    print("Graphics:")
    print(f"Strategy tyre set: {sm.Graphics.penalty.name}")

    print("Static: ")
    print(f"Max RPM: {sm.Static.max_rpm}")

asm.close()
```

## DataClass

Description are moslty a copy past of the ACCSharedMemoryDocumentationV1.x.x.pdf

### ACC_map

| Field    | Type                        | Description                                                                                                                                                      |
| -------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Physics  | [PhysicsMap](#physicsmap)   | Data that change at each graphic step. They all refer to the player’s car.                                                                                       |
| Graphics | [GraphicsMap](#graphicsmap) | Data that are updated at each graphical step. They mostly refer to player’s car except for carCoordinates and carID, which refer to the cars currently on track. |
| Statics  | [StaticsMap](#staticsmap)   | Data that are initialized when the instance starts and never changes until the instance is closed.                                                               |

### PhysicsMap

| Field                | Type                              | Description                                      | Comment                        |
| -------------------- | --------------------------------- | ------------------------------------------------ | ------------------------------ |
| packed_id            | int                               | Current step index                               |                                |
| gas                  | float                             | Gas pedal input value                            | From 0.0 to 1.0                |
| brake                | float                             | Brake pedal input value                          | From 0.0 to 1.0                |
| fuel                 | float                             | Amount of fuel remaining in liters               |                                |
| gear                 | int                               | Current gear                                     |                                |
| rpm                  | int                               | engine rpm                                       |                                |
| steer_angle          | float                             | Steering input value                             | From 0.0 to 1.0                |
| speed_kmh            | float                             | Car speed                                        |                                |
| velocity             | [Vector3f](#vector3f)             | Car velocity vector in global coordinates        | Contain 3 floats x, y, z       |
| g_force              | [Vector3f](#vector3f)             | Car acceleration vector in global coordinates    | Contain 3 floats x, y, z       |
| wheel_slip           | [Wheels](#wheels)                 | Tyre slip for each tyre                          |                                |
| wheel_pressure       | [Wheels](#wheels)                 | Tyre pressure                                    |                                |
| wheel_angular_s      | [Wheels](#wheels)                 | Wheel angular speed in rad/s                     |                                |
| tyre_core_temp       | [Wheels](#wheels)                 | Tyre rubber core temperature                     |                                |
| suspension_travel    | [Wheels](#wheels)                 | Suspension travel                                |                                |
| tc                   | float                             | TC in action                                     |                                |
| heading              | float                             | Car yaw orientation                              |                                |
| pitch                | float                             | Car pitch orientation                            |                                |
| roll                 | float                             | Car roll orientation                             |                                |
| car_damage           | [CarDamage](#cardamage)           | Car damage                                       |                                |
| pit_limiter_on       | bool                              | Pit limiter is on                                |                                |
| abs                  | float                             | ABS in action                                    |                                |
| autoshifter_on       | bool                              | Automatic transmission on                        |                                |
| turbo_boost          | float                             | Car turbo level                                  |                                |
| air_temp             | float                             | Air temperature                                  |                                |
| road_temp            | float                             | Road temperature                                 |                                |
| local_angular_vel    | [Vector3f](#vector3f)             | Car angular velocity vector in local coordinates | Contain 3 floats x, y, z       |
| final_ff             | float                             | Force feedback signal                            |                                |
| brake_temp           | [Wheels](#wheels)                 | Brake discs temperatures                         |                                |
| clutch               | float                             | Clutch pedal input value                         | From 0.0 to 1.0                |
| is_ai_controlled     | bool                              | Car is controlled by the AI                      |                                |
| tyre_contact_point   | List of [ContactPoint](#vector3f) | Tyre contact point global coordinates            |                                |
| tyre_contact_normal  | List of [ContactPoint](#vector3f) | Tyre contact normal                              |                                |
| tyre_contact_heading | List of [ContactPoint](#vector3f) | Tyre contact heading                             |                                |
| brake_bias           | float                             | Front brake bias                                 |                                |
| local_velocity       | [Vector3f](#vector3f)             | Car velocity vector in local coordinates         |                                |
| slit_ratio           | [Wheels](#wheels)                 | Tyre slip ratio                                  |                                |
| slit_angle           | [Wheels](#wheels)                 | Tyre slip angle                                  |                                |
| suspension_damage    | [Wheels](#wheels)                 | Damage of the suspension                         | From 0.0 to 0.1 (x30 for in s) |
| water_temp           | float                             | Water Temperature                                |                                |
| brake_pressure       | float                             | Brake pressure                                   |                                |
| front_brake_compound | int                               | Brake pad compund front                          |                                |
| rear_brake_compound  | int                               | Brake pad compund rear                           |                                |
| pad_life             | [Wheels](#wheels)                 | Brake pad wear                                   | Pad start at 29mm              |
| disc_life            | [Wheels](#wheels)                 | Brake disk wear                                  | Disc start at 32mm             |
| ignition_on          | bool                              | Ignition is on                                   |                                |
| starter_engine_on    | bool                              | Engine starter on                                |                                |
| is_engine_running    | bool                              | Engine running                                   |                                |
| kerb_vibration       | float                             | Kerb vibrations sent to the FFB                  |                                |
| slip_vibration       | float                             | Slip vibrations sent to the FFB                  |                                |
| g_vibration          | float                             | G force vibrations sent to the FFB               |                                |
| abs_vibration        | float                             | Abs vibrations sent to the FFB                   |                                |

### GraphicsMap

| Field                        | Type                                            | Description                                   | Comment                                                                       |
| ---------------------------- | ----------------------------------------------- | --------------------------------------------- | ----------------------------------------------------------------------------- |
| packed_id                    | int                                             | Current step index                            |                                                                               |
| status                       | [ACC_STATUS](#acc_status)                       |                                               |                                                                               |
| session_type                 | [ACC_SESSION_TYPE](#acc_session_type)           |                                               |                                                                               |
| current_time_str             | string                                          | Current lap time in string                    | Limited to 15 char                                                            |
| last_time_str                | string                                          | Last lap time in string                       | Limited to 15 char                                                            |
| best_time_str                | string                                          | Best lap time in string                       | Limited to 15 char                                                            |
| last_sector_time_str         | string                                          | Last split time in wide string                | Limited to 15 char                                                            |
| completed_lap                | int                                             | Number of completed laps                      |                                                                               |
| position                     | int                                             | Current player position                       |                                                                               |
| current_time                 | int                                             | Current lap time in milliseconds              |                                                                               |
| last_time                    | int                                             | Last lap time in milliseconds                 |                                                                               |
| best_time                    | int                                             | Best lap time in milliseconds                 |                                                                               |
| session_time_left            | float                                           | Session time left                             |                                                                               |
| distance_traveled            | float                                           | Distance travelled in the current stint       |                                                                               |
| is_in_pit                    | bool                                            | Car is pitting                                |                                                                               |
| current_sector_index         | int                                             | Current track sector                          |                                                                               |
| last_sector_time             | int                                             | Last sector time in milliseconds              |                                                                               |
| number_of_laps               | int                                             | Number of completed laps                      | Only has a value when the session is over                                     |
| tyre_compound                | string                                          | Tyre compound used                            |                                                                               |
| normalized_car_position      | float                                           | Car position on track spline                  |                                                                               |
| active_cars                  | int                                             | Number of cars on track                       |                                                                               |
| car_coordinates              | List of [Vector3f](#vector3f)                   | Coordinates of cars on track                  | 60 car max                                                                    |
| car_id                       | List of int                                     | Car IDs of cars on track                      | 60 car max                                                                    |
| player_car_id                | int                                             | Player Car ID                                 |                                                                               |
| penaltyTime                  | float                                           | Penalty time to wait                          |                                                                               |
| flag                         | [ACC_FLAG_TYPE](#acc_flag_type)                 |                                               |                                                                               |
| penalty                      | [ACC_PENALTY_TYPE](#acc_penalty_type)           |                                               | Added DSQ for driving the wrong way with value 22, 18 seems not used anymore. |
| ideal_line_on                | bool                                            | Ideal line on                                 |                                                                               |
| is_in_pit_lane               | bool                                            | Car is in pit lane                            |                                                                               |
| mandatory_pit_done           | bool                                            | Mandatory pit is completed                    |                                                                               |
| wind_speed                   | float                                           | Wind speed                                    | In m/s                                                                        |
| wind_direction               | float                                           | wind direction                                | In Radian                                                                     |
| is_setup_menu_visible        | bool                                            | Is in setup menu                              |                                                                               |
| main_display_index           | int                                             | Current car main display index                |                                                                               |
| secondary_display_index      | int                                             | Current car secondary display index           |                                                                               |
| tc_level                     | int                                             | Traction control level                        |                                                                               |
| tc_cut_level                 | int                                             | Traction control cut level                    |                                                                               |
| engine_map                   | int                                             | Current engine map                            |                                                                               |
| abs_level                    | int                                             | ABS level                                     |                                                                               |
| fuel_per_lap                 | float                                           | Average fuel consumed per lap in liters       |                                                                               |
| rain_light                   | bool                                            | Rain lights on                                |                                                                               |
| flashing_light               | bool                                            | Flashing lights on                            |                                                                               |
| light_stage                  | int                                             | Current lights stage                          |                                                                               |
| exhaust_temp                 | float                                           | Exhaust temperature                           |                                                                               |
| wiper_stage                  | int                                             | Current wiper stage                           |                                                                               |
| driver_stint_total_time_left | int                                             | Time the driver is allowed to drive/race      | In millisecond                                                                |
| driver_stint_time_left       | int                                             | Timethe driverisallowed to drive/stint        | In millisecond                                                                |
| rain_tyres                   | bool                                            | Are rain tyres equipped                       |                                                                               |
| session_index                | int                                             |                                               | idk wtf is this                                                               |
| used_fuel                    | float                                           | Used fuel since last time refueling           |                                                                               |
| delta_lap_time_str           | string                                          | Delta time in string                          |                                                                               |
| delta_lap_time               | int                                             | Delta time time in milliseconds               |                                                                               |
| estimated_lap_time_str       | string                                          | Estimated lap time in string                  |                                                                               |
| estimated_lap_time           | int                                             | Estimated lap time in milliseconds            |                                                                               |
| is_delta_positive            | bool                                            | Is delta positive                             |                                                                               |
| last_sector_time             | int                                             | Last split time in milliseconds               |                                                                               |
| is_valid_lap                 | bool                                            | Is Lap is valid for timing                    |                                                                               |
| fuel_estimated_laps          | float                                           | Laps possible with current fuel level         |                                                                               |
| track_status                 | string                                          | Track status                                  | Green, Fast, Optimum, Greasy, Damp, Wet, Flooded                              |
| missing_mandatory_pits       | int                                             | Mandatory pitstops the player still has to do |                                                                               |
| clock                        | int                                             | Time of day in secondso                       |                                                                               |
| direction_light_left         | bool                                            | Is Blinker left on                            |                                                                               |
| direction_light_right        | bool                                            | Is Blinker right on                           |                                                                               |
| global_yellow                | bool                                            | Yellow Flag is out ?                          |                                                                               |
| global_yellow_s1             | bool                                            | Yellow Flag in Sector 1 is out ?              |                                                                               |
| global_yellow_s2             | bool                                            | Yellow Flag in Sector 2 is out ?              |                                                                               |
| global_yellow_s3             | bool                                            | Yellow Flag in Sector 3 is out ?              |                                                                               |
| global_white                 | bool                                            | White Flag is out ?                           |                                                                               |
| global_green                 | bool                                            | Green Flag is out ?                           |                                                                               |
| global_chequered             | bool                                            | CheckeredFlag is out ?                        |                                                                               |
| global_red                   | bool                                            | RedFlag is out ?                              |                                                                               |
| mfd_tyre_set                 | int                                             | Number of tyre set on the MFD                 |                                                                               |
| mfd_fuel_to_add              | float                                           | How much fuel to add on the MFD               |                                                                               |
| mfd_tyre_pressure            | [Wheels](#wheels)                               | Tyre pressure to add                          |                                                                               |
| track_grip_status            | [ACC_TRACK_GRIP_STATUS](#acc_track_grip_status) | Track grip status                             |                                                                               |
| rain_intensity               | [ACC_RAIN_INTENSITY](#acc_rain_intensity)       | Rain intensity                                |                                                                               |
| rain_intensity_in_10min      | [ACC_RAIN_INTENSITY](#acc_rain_intensity)       | Rain intensity in 10 min                      |                                                                               |
| rain_intensity_in_30min      | [ACC_RAIN_INTENSITY](#acc_rain_intensity)       | Rain intensity in 30 min                      |                                                                               |
| current_tyre_set             | int                                             | Tyre Set currently in use                     |                                                                               |
| strategy_tyre_set            | int                                             | Next tyre set per strategy                    | Original tyre set used for this strategy                                      |
| gap_ahead                    | int                                             | Gap to the next car in ms                     |                                                                               |
| gap_behind                   | int                                             | Gap to the previous car in ms                 |                                                                               |

### StaticsMap

| Field                 | Type   | Description                 | Comment                    |
| --------------------- | ------ | --------------------------- | -------------------------- |
| sm_version            | string | Shared memory version       |                            |
| ac_version            | string | Assetto Corsa version       |                            |
| number_of_session     | int    | Number of sessions          |                            |
| num_cars              | int    | Number of cars              |                            |
| car_model             | string | Name of the car             | see [carmodel](#car-model) |
| track                 | string | Track name                  |                            |
| player_name           | string | Player name                 |                            |
| player_surname        | string | Player surname              |                            |
| player_nick           | string | Player nickname             |                            |
| sector_count          | int    | Number of sectors           |                            |
| max_rpm               | int    | Maximum rpm                 |                            |
| max_fuel              | float  | Maximum fuel tank capacity  | why float ? idk ask kunos  |
| penalty_enabled       | bool   | Penalties enabled           |                            |
| aid_fuel_rate         | float  | Fuel consumption rate       | from 0.0 to 1.0            |
| aid_tyre_rate         | float  | Tyre wear rate              | from 0.0 to 1.0            |
| aid_mechanical_damage | float  | Mechanical damage rate      | from 0.0 to 1.0            |
| aid_stability         | float  | Stability control used      | from 0.0 to 1.0            |
| aid_auto_clutch       | bool   | Auto clutch used            |                            |
| pit_window_start      | int    | Pit window opening time     |                            |
| pit_window_end        | int    | Pit windows closing time    |                            |
| is_online             | bool   | If is a multiplayer session |                            |
| dry_tyres_name        | string | Name of the dry tyres       |                            |
| wet_tyres_name        | string | Name of the wet tyres       |                            |

### Wheels

| Field       | Type  | Description      | Comment |
| ----------- | ----- | ---------------- | ------- |
| front_left  | float | Front left tyre  |         |
| front_right | float | Front right tyre |         |
| rear_left   | float | Rear left tyre   |         |
| rear_right  | float | Rear right tyre  |         |

### CarDamage

| Field  | Type  | Description                    | Comment                                                        |
| ------ | ----- | ------------------------------ | -------------------------------------------------------------- |
| front  | float | Damage at the front of the car | from 0.0 to idfk (multiply by 0.284 to get the time in second) |
| rear   | float | Damage at the rear of the car  | from 0.0 to idfk (multiply by 0.284 to get the time in second) |
| left   | float | Damage at the left of the car  | from 0.0 to idfk (multiply by 0.284 to get the time in second) |
| right  | float | Damage at the right of the car | from 0.0 to idfk (multiply by 0.284 to get the time in second) |
| center | float | Total damage of the car        | from 0.0 to idfk (multiply by 0.284 to get the time in second) |

### Vector3f

| Field | Type  |
| ----- | ----- |
| x     | float |
| y     | float |
| z     | float |

### ContactPoint

| Field       | Type                  |
| ----------- | --------------------- |
| front_left  | [Vector3f](#vector3f) |
| front_right | [Vector3f](#vector3f) |
| rear_left   | [Vector3f](#vector3f) |
| rear_right  | [Vector3f](#vector3f) |

## additional information

### Enums

#### ACC_STATUS

| Name       | Value |
| ---------- | ----- |
| ACC_OFF    | 0     |
| ACC_REPLAY | 1     |
| ACC_LIVE   | 2     |
| ACC_PAUSE  | 3     |

#### ACC_SESSION_TYPE

| Name                | Value |
| ------------------- | ----- |
| ACC_UNKNOW          | -1    |
| ACC_PRACTICE        | 0     |
| ACC_QUALIFY         | 1     |
| ACC_RACE            | 2     |
| ACC_HOTLAP          | 3     |
| ACC_TIME_ATTACK     | 4     |
| ACC_DRIFT           | 5     |
| ACC_DRAG            | 6     |
| ACC_HOTSTINT        | 7     |
| ACC_HOTLAPSUPERPOLE | 8     |

#### ACC_FLAG_TYPE

| Name               | Value |
| ------------------ | ----- |
| ACC_NO_FLAG        | 0     |
| ACC_BLUE_FLAG      | 1     |
| ACC_YELLOW_FLAG    | 2     |
| ACC_BLACK_FLAG     | 3     |
| ACC_WHITE_FLAG     | 4     |
| ACC_CHECKERED_FLAG | 5     |
| ACC_PENALTY_FLAG   | 6     |
| ACC_GREEN_FLAG     | 7     |
| ACC_ORANGE_FLAG    | 8     |

#### ACC_PENALTY_TYPE

| Name                                  | Value |
| ------------------------------------- | ----- |
| Unknown                               | -1    |
| No_penalty                            | 0     |
| DriveThrough_Cutting                  | 1     |
| StopAndGo_10_Cutting                  | 2     |
| StopAndGo_20_Cutting                  | 3     |
| StopAndGo_30_Cutting                  | 4     |
| Disqualified_Cutting                  | 5     |
| RemoveBestLaptime_Cutting             | 6     |
| DriveThrough_PitSpeeding              | 7     |
| StopAndGo_10_PitSpeeding              | 8     |
| StopAndGo_20_PitSpeeding              | 9     |
| StopAndGo_30_PitSpeeding              | 10    |
| Disqualified_PitSpeeding              | 11    |
| RemoveBestLaptime_PitSpeeding         | 12    |
| Disqualified_IgnoredMandatoryPit      | 13    |
| PostRaceTime                          | 14    |
| Disqualified_Trolling                 | 15    |
| Disqualified_PitEntry                 | 16    |
| Disqualified_PitExit                  | 17    |
| ~~Disqualified_WrongWay~~  ????       | 18    |
| DriveThrough_IgnoredDriverStint       | 19    |
| Disqualified_IgnoredDriverStint       | 20    |
| Disqualified_ExceededDriverStintLimit | 21    |
| Disqualified_WrongWay                 | 22    |

#### ACC_TRACK_GRIP_STATUS

| Name        | Value |
| ----------- | ----- |
| ACC_GREEN   | 0     |
| ACC_FAST    | 1     |
| ACC_OPTIMUM | 2     |
| ACC_GREASY  | 3     |
| ACC_DAMP    | 4     |
| ACC_WET     | 5     |
| ACC_FLOODED | 6     |

#### ACC_RAIN_INTENSITY

| Name             | Value |
| ---------------- | ----- |
| ACC_NO_RAIN      | 0     |
| ACC_DRIZZLE      | 1     |
| ACC_LIGHT_RAIN   | 2     |
| ACC_MEDIUM_RAIN  | 3     |
| ACC_HEAVY_RAIN   | 4     |
| ACC_THUNDERSTORM | 5     |

### Car Model

#### GT3

| Name                                | Kunos ID                     |
| ----------------------------------- | ---------------------------- |
| Aston Martin Vantage V12 GT3 2013   | amr_v12_vantage_gt3          |
| Audi R8 LMS 2015                    | audi_r8_lms                  |
| Bentley Continental GT3 2015        | bentley_continental_gt3_2016 |
| Bentley Continental GT3 2018        | bentley_continental_gt3_2018 |
| BMW M6 GT3 2017                     | bmw_m6_gt3                   |
| Emil Frey Jaguar G3 2012            | jaguar_g3                    |
| Ferrari 488 GT3 2018                | ferrari_488_gt3              |
| Honda NSX GT3 2017                  | honda_nsx_gt3                |
| Lamborghini Gallardo G3 Reiter 2017 | lamborghini_gallardo_rex     |
| Lamborghini Huracan GT3 2015        | lamborghini_huracan_gt3      |
| Lexus RCF GT3 2016                  | lexus_rc_f_gt3               |
| McLaren 650S GT3 2015               | mclaren_650s_gt3             |
| Mercedes AMG GT3 2015               | mercedes_amg_gt3             |
| Nissan GTR Nismo GT3 2015           | nissan_gt_r_gt3_2017         |
| Nissan GTR Nismo GT3 2018           | nissan_gt_r_gt3_2018         |
| Porsche 991 GT3 R 2018              | porsche_991_gt3_r            |
| Aston Martin V8 Vantage GT3 2019    | amr_v8_vantage_gt3           |
| Audi R8 LMS Evo 2019                | audi_r8_lms_evo              |
| Honda NSX GT3 Evo 2019              | honda_nsx_gt3_evo            |
| Lamborghini Huracan GT3 EVO 2019    | lamborghini_huracan_gt3_evo  |
| McLaren 720S GT3 2019               | mclaren_720s_gt3             |
| Porsche 911 II GT3 R 2019           | porsche_991ii_gt3_r          |
| Ferrari 488 GT3 Evo 2020            | ferrari_488_gt3_evo          |
| Mercedes AMG GT3 Evo 2020           | mercedes_amg_gt3_evo         |
| BMW M4 GT3 2021                     | bmw_m4_gt3                   |
| Audi R8 LMS Evo II 2022             | audi_r8_lms_evo_ii           |

#### GT4

| Name                              | Kunos ID                  |
| --------------------------------- | ------------------------- |
| Alpine A110 GT4 2018              | alpine_a110_gt4           |
| Aston Martin Vantage AMR GT4 2018 | amr_v8_vantage_gt4        |
| Audi R8 LMS GT4 2016              | audi_r8_gt4               |
| BMW M4 GT4 2018                   | bmw_m4_gt4                |
| Chevrolet Camaro GT4 R 2017       | chevrolet_camaro_gt4r     |
| Ginetta G55 GT4 2012              | ginetta_g55_gt4           |
| Ktm Xbow GT4 2016                 | ktm_xbow_gt4              |
| Maserati Gran Turismo MC GT4 2016 | maserati_mc_gt4           |
| McLaren 570s GT4 2016             | mclaren_570s_gt4          |
| Mercedes AMG GT4 2016             | mercedes_amg_gt4          |
| Porsche 718 Cayman GT4 MR 2019    | porsche_718_cayman_gt4_mr |

#### TC

| Name            | Kunos ID         |
| --------------- | ---------------- |
| BMW M2 Cup 2020 | bmw_m2_cs_racing |

#### Cup cars

| Name                             | Kunos ID                    |
| -------------------------------- | --------------------------- |
| Porsche9 91 II GT3 Cup 2017      | porsche_991ii_gt3_cup       |
| Lamborghini Huracan ST 2015      | lamborghini_huracan_st      |
| Ferrari 488 Challenge Evo 2020   | ferrari_488_challenge_evo   |
| Lamborghini Huracan ST Evo2 2021 | lamborghini_huracan_st_evo2 |
| Porsche 992 GT3 Cup 2021         | porsche_992_gt3_cup         |

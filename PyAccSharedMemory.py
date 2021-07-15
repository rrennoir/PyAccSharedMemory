import mmap
from multiprocessing.connection import Connection
import queue
import struct
import copy
from enum import Enum
from multiprocessing import Process, Queue, Pipe


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
    Disqualified_WrongWay = 18

    DriveThrough_IgnoredDriverStint = 19
    Disqualified_IgnoredDriverStint = 20

    Disqualified_ExceededDriverStintLimit = 21


class ACC_TRACK_GRIP_STATUS(Enum):

    ACC_GREEN = 0
    ACC_FAST = 1
    ACC_OPTIMUM = 2
    ACC_GREASY = 3
    ACC_DAMP = 4
    ACC_WET = 5
    ACC_FLOODED = 6


class ACC_RAIN_INTENSITY(Enum):

    ACC_NO_RAIN = 0
    ACC_DRIZZLE = 1
    ACC_LIGHT_RAIN = 2
    ACC_MEDIUM_RAIN = 3
    ACC_HEAVY_RAIN = 4
    ACC_THUNDERSTORM = 5


class accSM(mmap.mmap):

    def __init__(self, *args, **kwargs):
        super().__init__()

    def unpack_value(self, value_type: str, padding=0) -> float:
        return struct.unpack(f"={value_type}{padding}x", self.read(4 + padding))[0]

    def unpack_array(self, value_type: str, count: int, padding=0) -> tuple:

        if value_type in ("i", "f"):
            value = struct.unpack(
                f"={count}{value_type}{padding}x", self.read(4 * count + padding))

        else:
            value = self.read(2 * count + padding)

        return value

    def unpack_array2D(self, value_type: str, count: int, subCount: int) -> tuple:
        data = []
        for _ in range(count):
            data.append(self.unpack_array(value_type, subCount))
        return tuple(data)

    def unpack_string(self, count, padding=0) -> str:
        string_bytes = self.read(2 * count + padding)
        return string_bytes.decode("utf-16", errors="ignore")


def read_physic_map(physic_map: accSM) -> dict:
    physic_map.seek(0)
    return {
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


def read_graphics_map(graphic_map: accSM) -> dict:
    graphic_map.seek(0)
    return {
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
        "penalty": ACC_PENALTY_TYPE(graphic_map.unpack_value("i")),
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
        "mfdTyrePressureLF": graphic_map.unpack_value("f"),
        "mfdTyrePressureRF": graphic_map.unpack_value("f"),
        "mfdTyrePressureLR": graphic_map.unpack_value("f"),
        "mfdTyrePressureRR": graphic_map.unpack_value("f"),
        "trackGripStatus": ACC_TRACK_GRIP_STATUS(graphic_map.unpack_value("i")),
        "rainIntensity": ACC_RAIN_INTENSITY(graphic_map.unpack_value("i")),
        "rainIntensityIn10min": ACC_RAIN_INTENSITY(graphic_map.unpack_value("i")),
        "rainIntensityIn30min": ACC_RAIN_INTENSITY(graphic_map.unpack_value("i")),
        "currentTyreSet": graphic_map.unpack_value("i"),
        "strategyTyreSet": graphic_map.unpack_value("i")
    }


class accSharedMemory():

    def __init__(self) -> None:

        print("[pyASM]: Setting up shared memory reader process...")
        self.child_com, self.parent_com = Pipe()
        self.data_queue = Queue()
        self.asm_reader = Process(target=self.read_shared_memory, args=(self.child_com, self.data_queue))


    def start(self) -> bool:
        print("[pyASM]: Reading ACC Shared Memory...")
        self.asm_reader.start()
        if self.parent_com.recv() == "READING_SUCCES":
            return True

        return False


    def stop(self):
        print("[pyASM]: Sending stopping command to process...")
        self.parent_com.send("STOP_PROCESS")

        print("[pyASM]: Waiting for process to finish...")   
        if (self.parent_com.recv() == "PROCESS_TERMINATED"):
            # Need to empty the queue before joining process (qsize() isn't 100% accurate)
            while self.data_queue.qsize() != 0:
                try:
                    _ = self.data_queue.get_nowait()
                except queue.Empty:
                    pass
        else:
            print("[pyASM]: Received unexpected message, program might be deadlock now.")

        self.asm_reader.join()


    def get_sm_data(self) -> dict:

        sm_data = None
        self.parent_com.send("DATA_REQUEST")
        if self.parent_com.recv() == "DATA_OK":
            try:
                sm_data = self.data_queue.get(timeout=0.1)
            
            except(Queue.empty):
                # idk 
                pass

        return sm_data


    def get_queue_size(self):
        """"Only for debugging purpose, return the size of the queue."""
        return self.data_queue.qsize()


    @staticmethod
    def read_shared_memory(comm: Connection, data_queue: Queue):

        with accSM(-1, 804, tagname="Local\\acpmf_physics", access=mmap.ACCESS_READ) as physicSM, accSM(-1, 1580, tagname="Local\\acpmf_graphics", access=mmap.ACCESS_READ) as graphicSM:

            if sum(physicSM.read()) != 0:
                # Still pass if acc created the memory map first and is now closed but it's fine in this case.
                physicSM.seek(0)

                comm.send("READING_SUCCES")

                physics = {}
                graphics = {}
                last_pPacketID = 0
                last_gPacketID = 0

                message = ""
                while message != "STOP_PROCESS":

                    if comm.poll():
                        message = comm.recv()

                    pPacketID = physicSM.unpack_value("i")
                    gPacketID = graphicSM.unpack_value("i")

                    if pPacketID != last_pPacketID:
                        last_pPacketID = pPacketID
                        physics = read_physic_map(physicSM)

                        if gPacketID != last_gPacketID:
                            last_gPacketID = gPacketID
                            graphics = read_graphics_map(graphicSM)

                    if message == "DATA_REQUEST":
                        data = {"physics": physics, "graphics": graphics}
                        data_queue.put(copy.deepcopy(data))
                        comm.send("DATA_OK")
                        message = ""

                    physicSM.seek(0)
                    graphicSM.seek(0)

            else:
                print("[ASM_Reader]: ACC isn't running.")
                comm.send("READING_FAILURE")

        comm.send("PROCESS_TERMINATED")
        print("[ASM_Reader]: Process Terminated.")


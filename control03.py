from starship import IMU, Controller
from math import radians

class GuidanceAndControl:
    def __init__(self):
        print("Hello world control starting...")
        self.mode=0
        self.res_pitch=0
        self.res_rVel=0
        self.res_posX=0
        self.res_velX=0

    def control(self, imu, controller, fuel, dt):

        self.res_pitch = imu.getPitch()
        self.res_rVel = imu.getRotationalVelocity()
        self.res_velX = imu.getVelocity().x
        print(f"vel x: {self.res_velX}")
        print(f"vel y: {imu.getVelocity().y}")
        # print(f"pos x: {imu.getPosition().x}")
        # print(f"pos y: {imu.getPosition().y}")
        print(f"left power: {controller.raptor_left_power}")
        print(f"right power: {controller.raptor_right_power}")
        print(f"down acceleration: {imu.getAcceleration().y}")

        self.rot_feedback = 1 * self.res_pitch + 1.5 * self.res_rVel - 0.01 * self.res_velX
        self.path_gain = 0.5 * (200 - imu.getPosition().y)
        self.path_feedback = self.path_gain * (- imu.getVelocity().y - (5 + 0.2 * imu.getPosition().y))
        self.land_feedback = 10 * (- imu.getVelocity().y - 2)


        if imu.getPosition().y < 200:
            if imu.getVelocity().y < -5:
                controller.raptor_left_power = 41 + max(0, min(60, self.path_feedback))
                controller.raptor_right_power = 40
            else:
                controller.raptor_left_power = 43.5 + max(-4, min(56, self.land_feedback))
                controller.raptor_right_power = 0
                controller.raptor_right_pitch = 15 / radians(90) * self.rot_feedback
        else:
            controller.raptor_left_power = 42

        if imu.getPosition().y < 80:
            if imu.getVelocity().x > 0.8:
                controller.rcs_top_left_power = 0
                controller.rcs_top_right_power = 100
                controller.rcs_bot_right_power = 100
                controller.rcs_bot_left_power = 0
            elif imu.getVelocity().x < -0.8:
                controller.rcs_top_left_power = 100
                controller.rcs_top_right_power = 0
                controller.rcs_bot_right_power = 0
                controller.rcs_bot_left_power = 100
            else:
                controller.rcs_top_left_power = 0
                controller.rcs_top_right_power = 0
                controller.rcs_bot_right_power = 0
                controller.rcs_bot_left_power = 0

        if fuel <= 0:
            print("OUT OF FUEL")

        controller.raptor_left_pitch = 15 / radians(90) * self.rot_feedback




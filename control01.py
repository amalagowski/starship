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

        self.res_pitch = -imu.getPitch()
        self.res_rVel = -imu.getRotationalVelocity()
        self.res_posX = 20 - imu.getPosition().x
        self.res_velX = -imu.getVelocity().x


        if self.mode == 0:
            controller.raptor_left_power = 0
            controller.raptor_right_power = 0
            controller.rcs_bot_right_power = 0
            controller.rcs_bot_left_power = 0
            controller.rcs_top_left_power = 0
            controller.rcs_top_right_power = 0

        if self.mode == 2:
            controller.raptor_left_power = 40
            controller.raptor_right_power = 40
            controller.rcs_bot_right_power = 0
            controller.rcs_bot_left_power = 0
            controller.rcs_top_left_power = 0
            controller.rcs_top_right_power = 0

        self.rot_feedback = self.res_pitch + 2.8 * self.res_rVel
        print(f'Total residual: {self.rot_feedback}')

        if abs(self.rot_feedback) > radians(15):
            self.mode = 1
            if self.rot_feedback < 0:
                print('CONTROL')
                controller.rcs_top_left_power = 100
                controller.rcs_top_right_power = 0
                controller.rcs_bot_right_power = 100
                controller.rcs_bot_left_power = 0
            if self.rot_feedback > 0:
                print('CONTROL')
                controller.rcs_top_left_power = 0
                controller.rcs_top_right_power = 100
                controller.rcs_bot_right_power = 0
                controller.rcs_bot_left_power = 100
        elif self.mode == 1 and self.res_posX < 0:
            controller.rcs_top_left_power = 0
            controller.rcs_top_right_power = 100
            controller.rcs_bot_right_power = 100
            controller.rcs_bot_left_power = 0

        if fuel <= 0:
            print("OUT OF FUEL")



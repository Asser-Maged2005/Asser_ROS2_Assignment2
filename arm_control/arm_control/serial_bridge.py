import math
import time
import serial
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory


class SerialServoBridge(Node):
    def __init__(self):
        super().__init__('serial_servo_bridge')
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 115200)
        self.port = self.get_parameter('port').get_parameter_value().string_value
        self.baud = self.get_parameter('baudrate').get_parameter_value().integer_value

        self.ser = None
        self.last_tx_time = 0.0
        self.last_packet = None
        self.connect_serial()

        self.subscription = self.create_subscription(
            JointTrajectory, '/arm_controller/joint_trajectory', self.listener_callback, 10
        )

    def connect_serial(self):
        try:
            ser = serial.Serial()
            ser.port = self.port
            ser.baudrate = self.baud
            ser.timeout = 0.05
            ser.dsrdtr = False
            ser.rtscts = False
            ser.open()
            ser.dtr = False
            ser.rts = False
            time.sleep(1.5)
            self.ser = ser
            self.get_logger().info(f'Connected to microcontroller on {self.port} @ {self.baud}')
        except serial.SerialException as e:
            self.ser = None
            self.get_logger().warning(f'Serial port unavailable ({e})')

    def rad_to_servo_deg(self, rad: float) -> int:
        deg = int(round(math.degrees(rad) + 90.0))
        return max(0, min(180, deg))

    def listener_callback(self, msg: JointTrajectory):
        if not msg.points:
            return

        now = time.monotonic()
        if now - self.last_tx_time < 0.05:
            return

        positions = msg.points[-1].positions
        angles = [self.rad_to_servo_deg(p) for p in positions]
        while len(angles) < 4:
            angles.append(90)

        packet = f"{angles[0]},{angles[1]},{angles[2]},{angles[3]}\n"
        if packet == self.last_packet:
            return

        self.last_tx_time = now
        self.last_packet = packet
        self.get_logger().info(f'TX -> {packet.strip()}')

        if self.ser is None or not self.ser.is_open:
            self.connect_serial()

        if self.ser and self.ser.is_open:
            try:
                self.ser.write(packet.encode('utf-8'))
            except serial.SerialException as e:
                self.get_logger().warning(f'Serial write failed ({e}), will retry...')
                try:
                    self.ser.close()
                except Exception:
                    pass
                self.ser = None


def main(args=None):
    rclpy.init(args=args)
    node = SerialServoBridge()
    rclpy.spin(node)
    if node.ser and node.ser.is_open:
        node.ser.close()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

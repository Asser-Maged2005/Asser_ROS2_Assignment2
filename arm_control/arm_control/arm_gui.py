import tkinter as tk
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


class ArmSliderGUI(Node):
    def __init__(self):
        super().__init__('arm_slider_gui')
        self.publisher_ = self.create_publisher(
            JointTrajectory, '/arm_controller/joint_trajectory', 10
        )
        self.joint_names = ['joint1', 'joint2', 'joint3', 'joint4']

        self.root = tk.Tk()
        self.root.title('4-DOF Arm Trajectory Controller')
        self.sliders = []

        for name in self.joint_names:
            frame = tk.Frame(self.root, padx=12, pady=6)
            frame.pack(fill='x')
            tk.Label(frame, text=name, width=8, anchor='w').pack(side='left')
            slider = tk.Scale(
                frame,
                from_=-1.57,
                to=1.57,
                resolution=0.02,
                orient='horizontal',
                length=280,
                command=lambda _val: self.send_trajectory(),
            )
            slider.set(0.0)
            slider.pack(side='right')
            self.sliders.append(slider)

        btn_frame = tk.Frame(self.root, pady=8)
        btn_frame.pack()
        tk.Button(btn_frame, text='Reset to Zero', command=self.reset_all).pack()

    def send_trajectory(self):
        msg = JointTrajectory()
        msg.joint_names = self.joint_names
        point = JointTrajectoryPoint()
        point.positions = [float(s.get()) for s in self.sliders]
        point.time_from_start = Duration(sec=0, nanosec=300_000_000)
        msg.points = [point]
        self.publisher_.publish(msg)

    def reset_all(self):
        for s in self.sliders:
            s.set(0.0)
        self.send_trajectory()

    def run(self):
        self.root.mainloop()


def main(args=None):
    rclpy.init(args=args)
    node = ArmSliderGUI()
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

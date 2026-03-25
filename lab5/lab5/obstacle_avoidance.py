"""Obstacle avoidance

Implement potential fields (or Bug, Tangent Bug, DWA, RL).
Use /scan (LaserScan) and /odom; publish /cmd_vel.
"""
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
import math

class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__("obstacle_avoidance")

        # Настройка времени симуляции
        if not self.has_parameter('use_sim_time'):
            self.declare_parameter('use_sim_time', True)

        # Настройка QoS для работы с Gazebo (Best Effort)
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            depth=10
        )

        # Параметры цели и порогов
        self.goal_x = self.declare_parameter("goal_x", 3.0).value
        self.goal_y = self.declare_parameter("goal_y", 3.0).value
        self.dist_threshold = 0.5  # Дистанция до препятствия
        self.goal_tolerance = 0.1  # Радиус достижения цели

        # Внутреннее состояние робота
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0
        self.obstacle_ahead = False

        # Подписки (используем созданный qos)
        self.scan_sub = self.create_subscription(LaserScan, "/scan", self.scan_callback, qos)
        self.odom_sub = self.create_subscription(Odometry, "/odom", self.odom_callback, qos)
        
        # Паблишер для команд скорости (TwistStamped)
        self.cmd_pub = self.create_publisher(TwistStamped, "/cmd_vel", 10)

        # Таймер управления (10 Гц)
        self.timer = self.create_timer(0.1, self.control_loop)

    def scan_callback(self, msg):
        # Проверяем сектор перед роботом (индексы зависят от лидара, обычно 0 - центр)
        # Для TurtleBot3 берем срезы в начале и конце массива
        front_ranges = msg.ranges[:30] + msg.ranges[-30:]
        # Фильтруем значения (игнорируем 0 и inf)
        valid_ranges = [r for r in front_ranges if r > 0.05 and not math.isinf(r)]
        
        if valid_ranges:
            min_dist = min(valid_ranges)
            self.obstacle_ahead = min_dist < self.dist_threshold
        else:
            self.obstacle_ahead = False

    def odom_callback(self, msg):
        # Позиция
        pos = msg.pose.pose.position
        self.current_x = pos.x
        self.current_y = pos.y

        # Угол (Yaw) из кватерниона
        q = msg.pose.pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        self.current_yaw = math.atan2(siny_cosp, cosy_cosp)

    def control_loop(self):
        # Лог раз в 2 секунды
        self.get_logger().info(
            f"Pos: ({self.current_x:.1f}, {self.current_y:.1f}), Obstacle: {self.obstacle_ahead}", 
            throttle_duration_sec=2.0
        )

        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "base_link"

        # Расстояние до цели
        dist_to_goal = math.sqrt((self.goal_x - self.current_x)**2 + (self.goal_y - self.current_y)**2)

        if dist_to_goal < self.goal_tolerance:
            self.get_logger().info("!!! GOAL REACHED !!!")
            msg.twist.linear.x = 0.0
            msg.twist.angular.z = 0.0
            self.cmd_pub.publish(msg)
            return

        # Угол на цель
        angle_to_goal = math.atan2(self.goal_y - self.current_y, self.goal_x - self.current_x)
        angle_diff = angle_to_goal - self.current_yaw
        
        # Нормализация угла в диапазон [-pi, pi]
        angle_diff = math.atan2(math.sin(angle_diff), math.cos(angle_diff))

        if self.obstacle_ahead:
            # Препятствие: стоим и крутимся
            msg.twist.linear.x = 0.0
            msg.twist.angular.z = 0.5
        else:
            # Путь свободен: едем к цели
            if abs(angle_diff) > 0.3:  # Если сильно отклонились, поворачиваем активнее
                msg.twist.linear.x = 0.05
                msg.twist.angular.z = 0.5 if angle_diff > 0 else -0.5
            else:
                msg.twist.linear.x = 0.2
                msg.twist.angular.z = angle_diff * 0.5 # Плавное подруливание

        self.cmd_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # При остановке выключаем двигатели
        stop_msg = TwistStamped()
        node.cmd_pub.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()
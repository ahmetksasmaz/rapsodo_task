import sys
import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    data = {
        "message_id" : [],
        "ball_3d_center_x" : [],
        "ball_3d_center_y" : [],
        "ball_3d_center_z" : [],
        "ball_avg_3d_speed_vector_x" : [],
        "ball_avg_3d_speed_vector_y" : [],
        "ball_avg_3d_speed_vector_z" : [],
        "gt_ball_bbox_iou" : [],
    }
    
    def __init__(self, output_file_name):
        self.output_file_name = output_file_name
        self.output_file = open(output_file_name, "r")
        for line in self.output_file.readlines():
            line = line.strip()
            parts = line.split("\t")
            self.data["message_id"].append(int(parts[0]))
            self.data["ball_3d_center_x"].append(float(parts[1]))
            self.data["ball_3d_center_y"].append(float(parts[2]))
            self.data["ball_3d_center_z"].append(float(parts[3]))
            self.data["ball_avg_3d_speed_vector_x"].append(float(parts[4]))
            self.data["ball_avg_3d_speed_vector_y"].append(float(parts[5]))
            self.data["ball_avg_3d_speed_vector_z"].append(float(parts[6]))
            self.data["gt_ball_bbox_iou"].append(float(parts[7]))
    def plot(self):
        frame_indices = np.array(self.data["message_id"])
        ball_3d_center_x = np.array(self.data["ball_3d_center_x"])
        ball_3d_center_y = np.array(self.data["ball_3d_center_y"])
        ball_3d_center_z = np.array(self.data["ball_3d_center_z"])
        ball_avg_3d_speed_vector_x = np.array(self.data["ball_avg_3d_speed_vector_x"])
        ball_avg_3d_speed_vector_y = np.array(self.data["ball_avg_3d_speed_vector_y"])
        ball_avg_3d_speed_vector_z = np.array(self.data["ball_avg_3d_speed_vector_z"])
        gt_ball_bbox_iou = np.array(self.data["gt_ball_bbox_iou"])
        ball_avg_speed = np.sqrt(ball_avg_3d_speed_vector_x ** 2 + ball_avg_3d_speed_vector_y ** 2 + ball_avg_3d_speed_vector_z ** 2)
        
        # Plotting Speed
        ball_avg_speed_plot = plt.figure(1)
        ax = plt.gca()
        ax.set_xlim([0, 15])
        ax.set_ylim([0, 60])
        ax.set_xlabel('Frame Number')
        ax.set_ylabel('Speed (m/s)')
        
        plt.plot(frame_indices, ball_avg_speed)
        ball_avg_speed_plot.savefig("outputs/plots/ball_avg_speed_plot.png")
        plt.close(ball_avg_speed_plot)

        # Plotting Ground Truth Errors
        gt_ball_bbox_iou_plot = plt.figure(2)
        ax = plt.gca()
        ax.set_xlim([0, 15])
        ax.set_ylim([0, 1.0])
        ax.set_xlabel('Frame Number')
        ax.set_ylabel('Ground Truth Ball Bbox IOU')
        plt.plot(frame_indices, gt_ball_bbox_iou)
        gt_ball_bbox_iou_plot.savefig("outputs/plots/gt_ball_bbox_iou_plot.png")
        plt.close(gt_ball_bbox_iou_plot)
        
        ball_3d_center_plot = plt.figure(4)
        ball_3d_center_plot.add_subplot(111, projection='3d')
        ax = plt.gca()
        ax.set_xlim([-1.0, 1.0])
        ax.set_ylim([-2.0, 0.0])
        ax.set_zlim([0.0, 5.0])
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')
        plt.plot(ball_3d_center_x, ball_3d_center_y, ball_3d_center_z)
        ball_3d_center_plot.savefig("outputs/plots/ball_3d_center_plot.png")
        # plt.show()
        plt.close(ball_3d_center_plot)

if __name__ == "__main__":
    if sys.argv[1:]:
        plotter = Plotter(sys.argv[1])
    else:
        raise ValueError("Output file name is required.")
    plotter.plot()
import numpy as np
import trimesh
import pyrender
from matplotlib import pyplot
from pyrender.constants import RenderFlags
from pyvirtualdisplay import Display
import os
import argparse
# 需要在mac或者Linux运行 windows不支持Pyvirtualdisplay
# notice：需要pip install pyrender pyvirtualdisplay matplotlib
# git clone https://github.com/mmatl/pyopengl.git
# pip install ./pyopengl
os.environ['PYOPENGL_PLATFORM'] = 'egl'

def render_image(obj_file, i, thres):
    # 创建虚拟显示
    display = Display(visible=0, size=(800, 800))
    display.start()

    # 加载 OBJ 文件
    mesh = trimesh.load(obj_file)

    # 创建 Pyrender 场景
    scene = pyrender.Scene()

    # 创建 Pyrender 网格
    mesh_node = pyrender.Mesh.from_trimesh(mesh)
    scene.add(mesh_node)

    # 创建摄像机
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 4.0, aspectRatio=1.0)

    # 设置摄像机视角
    # 将摄像机位置设置在人的背后
    camera_pose = np.eye(4)
    camera_pose[0:3, 3] = [0, 0, -3]  # 将相机位置移动到人的背后

    # 将相机的朝向调整为面向人的正面
    target = np.array([0, 0, 0])  # 人的位置
    forward = target - camera_pose[0:3, 3]  # 相机指向人的方向
    forward /= np.linalg.norm(forward)  # 归一化向量
    up = np.array([0, 1, 0])  # 定义相机的上方向
    right = np.cross(forward, up)  # 计算相机的右方向
    up_new = np.cross(right, forward)  # 重新计算相机的上方向，以确保垂直于新的右方向和前方向
    camera_pose[0:3, 0] = right
    camera_pose[0:3, 1] = up_new
    camera_pose[0:3, 2] = -forward

    # 在场景中添加摄像机
    scene.add(camera, pose=camera_pose)

    r = pyrender.OffscreenRenderer(viewport_width=800, viewport_height=800)
    # 添加光源
    light = pyrender.PointLight(color=[1.0, 1.0, 1.0], intensity=100.0)
    light_pose = np.eye(4)
    light_pose[0:3, 3] = [0, 0, -3]  # 设置光源位置
    scene.add(light, pose=light_pose)

    color, depth = r.render(scene)

    # 保存深度图
    # 深度处理（重要，需注意）
    depth_image = np.where(depth < thres, 0, (depth - thres) / (5 - thres) * 255)
    depth_image = depth_image.astype(np.uint8)
    depth_image = np.rot90(depth_image, 2)# obj是倒过来的，所以要旋转180度
    pyplot.imsave("./depth/"+str(i)+".png", depth_image, cmap="gray")

    # 保存颜色图（观测图）
    color = np.rot90(color, 2)
    pyplot.imsave("./color/"+str(i)+".png", color)

if __name__ == "__main__":
    # 参数
    parser = argparse.ArgumentParser()
    parser.add_argument("--obj", type=str, default="data_obj/001_01.obj")
    parser.add_argument("--i", type=int, default=3)
    parser.add_argument("--thres", type=int, default=2.5)
    args = parser.parse_args()

    # 创建color和depth文件夹
    if not os.path.exists("color"):
        os.makedirs("color")
    if not os.path.exists("depth"):
        os.makedirs("depth")
    render_image(args.obj, args.i, args.thres)

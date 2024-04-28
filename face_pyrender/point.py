import numpy as np
import trimesh
import pyrender
from matplotlib import pyplot
from pyrender.constants import RenderFlags
from pyvirtualdisplay import Display
import os
import argparse
# 设置环境变量
os.environ['PYOPENGL_PLATFORM'] = 'egl'

def render_image(obj_file, i, thres):
    # 创建虚拟显示并启动
    display = Display(visible=0, size=(800, 800))
    display.start()

    # 加载 OBJ 文件
    mesh = trimesh.load(obj_file)

    """     # 获取顶点坐标
    vertices = mesh.vertices
    
    # 计算顶点坐标中最大的z坐标
    max_z = np.max(vertices[:, 2])
    
    # 将最大的z坐标用作阈值
    thres = max_z"""

    # 创建 Pyrender 场景
    scene = pyrender.Scene()

    # 创建 Pyrender 网格
    mesh_node = pyrender.Mesh.from_trimesh(mesh)
    scene.add(mesh_node)

    # 创建摄像机
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 4.0, aspectRatio=1.0)

    # 设置摄像机位置和方向
    camera_pose = np.eye(4)
    camera_pose[0:3, 3] = [0, 0, -3]  # 设置摄像机位置
    camera_pose[0:3, 2] = [-1, 0, 0]   # 设置摄像机方向

    # 在场景中添加摄像机
    scene.add(camera, pose=camera_pose)

    # 创建渲染器
    r = pyrender.OffscreenRenderer(viewport_width=0, viewport_height=0)

    # 添加光源
    light = pyrender.PointLight(color=[1.0, 1.0, 1.0], intensity=100.0)
    light_pose = np.eye(4)
    light_pose[0:3, 3] = [0, 0, -3]  # 设置光源位置
    scene.add(light, pose=light_pose)

    # 渲染并保存深度图
    color, depth = r.render(scene)
    max_depth = np.max(depth)  # 找到深度图像中的最大值.也就是最靠前的位置
    thres = max_depth  # 将最大值作为阈值

    # 深度图处理
    depth_image = np.where(depth > thres, 0, (depth - thres) / (5 - thres) * 255)
    depth_image = depth_image.astype(np.uint8)
    depth_image = np.rot90(depth_image, 2)
    pyplot.imsave("./depth/"+str(i)+".png", depth_image, cmap="gray")

    # 保存颜色图
    color = np.rot90(color, 2)
    pyplot.imsave("./color/"+str(i)+".png", color)


if __name__ == "__main__":
    # 参数解析
    parser = argparse.ArgumentParser()
    parser.add_argument("--obj", type=str, default="003_01.obj")
    parser.add_argument("--i", type=int, default=3)
    parser.add_argument("--thres", type=int, default=2.5)
    args = parser.parse_args()

    # 创建 color 和 depth 文件夹
    if not os.path.exists("color"):
        os.makedirs("color")
    if not os.path.exists("depth"):
        os.makedirs("depth")

    # 渲染并保存图像
    render_image(args.obj, args.i, args.thres)

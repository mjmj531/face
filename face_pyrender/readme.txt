python 环境3.8（更高版本没尝试过）
1. 安装依赖
pip install pyrender pyvirtualdisplay matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple

git clone https://github.com/mmatl/pyopengl.git

pip install ./pyopengl

2. 输入参数：
-obj obj文件名字
-id 图片的Index
-thres thres(see part3)默认2.5

3. 深度处理
背景深度是0，人像深度大于0（大约在2.7-4.2之间）
为了使保存的深度信息更精准，对于深度进行如下操作，对于不高于thres的赋值为0，高于thres的，在thres和5之间线性映射

4. 相机角度
应该不用改变
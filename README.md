# e-bicycle-petalmail
设计制作一个基于搭载了SG2000芯片的Milk-V系统板和Linux系统之上，驱动8英寸MIPI屏，使用LVGL呈现丰富的骑行数据与导航数据的电动自行车屏显产品。
## 配置说明
### 配置Makefile文件
- 将CC修改为当前系统环境下的riscv64-unknown-linux-musl-gcc路径
- 将CFLAGS修改为当前系统环境下的Python头文件路径
- 将LDFLAGS的-L的后缀修改为库文件路径
- 生成的程序位于build/bin/demo
### 配置LVGL代码
- 自定义的LVGL代码都存放于lvgl/src/custom目录下
- 添加和删除.c文件需要编辑该目录下的.mk文件

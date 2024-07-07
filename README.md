# EBikeComponent
Based Milk-V Duo S device, design a program to achive that visualize cycling and navigation data.
## Makefile文件配置
- 将CC修改为你的riscv64-unknown-linux-musl-gcc路径
- 将CFLAGS修改为你的Python头文件路径
- 将LDFLAGS的-L的后缀修改为库文件路径
- 生成的程序位于build/bin/demo
## LVGL代码导入与修改
- LVGL所有文件都存放于lvgl/src/custom目录下
- 添加和删除.c文件需要编辑该目录下的.mk文件

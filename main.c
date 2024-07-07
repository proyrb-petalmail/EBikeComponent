#include <unistd.h>
#include <pthread.h>
#include <sys/time.h>
#include <stdio.h>
#include <time.h>
#include <Python.h>

#include "lvgl/lvgl.h"
#include "lv_drivers/display/fbdev.h"
#include "lvgl/src/custom/ui.h"

#define DISP_BUF_SIZE (128 * 1024)

char* list = NULL;

static void getListFromPython(void);
static void process(void);

int main(void) {
	//getListFromPythonv();

    /*LittlevGL init*/
    lv_init();

    /*Linux frame buffer device init*/
    fbdev_init();

    /*A small buffer for LittlevGL to draw the screen's content*/
    static lv_color_t buf[DISP_BUF_SIZE];

    /*Initialize a descriptor for the buffer*/
    static lv_disp_draw_buf_t disp_buf;
    lv_disp_draw_buf_init(&disp_buf, buf, NULL, DISP_BUF_SIZE);

    /*Initialize and register a display driver*/
    static lv_disp_drv_t disp_drv;
    lv_disp_drv_init(&disp_drv);
    disp_drv.draw_buf   = &disp_buf;
    disp_drv.flush_cb   = fbdev_flush;
    disp_drv.hor_res    = 240;
    disp_drv.ver_res    = 320;
    lv_disp_drv_register(&disp_drv);

	ui_init();

    /*Handle LitlevGL tasks (tickless mode)*/
    while(1) {
    	process();
        lv_timer_handler();
        usleep(1000);
    }

    return 0;
}

void getListFromPython(void) {
	Py_Initialize();//initialize python
	
	PyRun_SimpleString("import sys");//import modules
	PyRun_SimpleString("sys.path.append('.')");//append current path
	//PyRun_SimpleString("print(sys.path)");//print paths in sys
	
	PyObject *pModule = PyImport_ImportModule("api");//import extern module
	if(!pModule) {
		PyErr_Print();
		printf("failed to import module!\n");
		return;
	}
	
	PyObject *pFunc = PyObject_GetAttrString(pModule, "get_steps");//get function in module
	if(!pFunc) {
		PyErr_Print();
		printf("function not found or not callable!\n");
		return;
	}
	/*if(!pFunc || !PyCallable_Check(pFunc)) {
		PyErr_Print();
		printf("function not found or not callable!\n");
		return -1;
	}*/
	
	//第四步：新建python中的tuple对象（构建参数）
	//PyObject *pArgs = PyTuple_New(2);
	////PyTuple_SetItem(pArgs, 0, Py_BuildValue(""));
	//PyTuple_SetItem(pArgs, 0, Py_BuildValue("i", a));
	//PyTuple_SetItem(pArgs, 1, Py_BuildValue("i", b));
	
	//第五步：调用函数
	PyObject *pValue = PyObject_CallObject(pFunc, NULL);//pArgs
	if(!pValue) {
		PyErr_Print();
		printf("function call failed!\n");
		return;
	}

	//第六步：清空PyObject 
	Py_DECREF(pValue);
	//Py_DECREF(pArgs);
	Py_DECREF(pFunc);
	Py_DECREF(pModule);
	Py_Finalize();
}

void process(void) {
    static int count;
    
	static time_t current_time;
	static char cur_time[9] = "";
	static struct tm* now_time;
    time(&current_time);
    now_time = localtime(&current_time);
    now_time->tm_hour = (now_time->tm_hour + 8) % 24;
    strftime(cur_time, sizeof(cur_time), "%T", now_time);
    lv_label_set_text(ui_LabelTime, cur_time);
    
    static int dist;
    static char dist_text[9] = "";
    sprintf(dist_text, "%d.%dkm", dist / 10000, (dist % 10000) / 10);
	lv_label_set_text(ui_LabelDistence, dist_text);
    
    static int select;
	lv_roller_set_selected(ui_RollerCmd, select = (count / 500) % 13, LV_ANIM_OFF);
	
	static int power_value;
    static char power_text[4] = "";
    lv_arc_set_value(ui_ArcPower, power_value = 100 - ((count / 200) % 101));
    sprintf(power_text, "%d", power_value);
    lv_label_set_text(ui_LabelPower, power_text);
    
    static char cmd[13] = {0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0};
    char cmdValue = cmd[select];
    switch(cmdValue) {
   		default:
   			//as to case 0
   		case 0:
   			lv_label_set_text(ui_LabelIcon, "");
   			break;
   		case 1:
   			lv_label_set_text(ui_LabelIcon, "");
   			break;
   		case 2:
   			lv_label_set_text(ui_LabelIcon, "");
   			break;
    }
    
	static int speed_value;
    static char speed_text[3] = "";
	lv_arc_set_value(ui_ArcSpeed, speed_value = (count / 40) % 51);
    sprintf(speed_text, "%d", speed_value);
	lv_label_set_text(ui_LabelSpeed, speed_text);
	dist += speed_value;
	
	count++;
}

/*Set in lv_conf.h as `LV_TICK_CUSTOM_SYS_TIME_EXPR`*/
uint32_t custom_tick_get(void) {
    static uint64_t start_ms = 0;
    if(start_ms == 0) {
        struct timeval tv_start;
        gettimeofday(&tv_start, NULL);
        start_ms = (tv_start.tv_sec * 1000000 + tv_start.tv_usec) / 1000;
    }

    struct timeval tv_now;
    gettimeofday(&tv_now, NULL);
    uint64_t now_ms;
    now_ms = (tv_now.tv_sec * 1000000 + tv_now.tv_usec) / 1000;

    uint32_t time_ms = now_ms - start_ms;
    return time_ms;
}

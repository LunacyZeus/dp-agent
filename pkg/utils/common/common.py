import inspect
import json
import os
import sys
import time
import traceback


def catch_exception(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            traceback.print_exc()
            print("运行崩溃", e)
            except_type, except_value, except_traceback = sys.exc_info()
            except_file = os.path.split(except_traceback.tb_frame.f_code.co_filename)[1]
            exc_dict = {
                "报错类型": except_type,
                "报错信息": except_value,
                "报错文件": except_file,
                "报错行数": except_traceback.tb_lineno,
            }
            print(exc_dict)

    return wrapper


def record_data(file_path, data, is_parse=False):
    if type(data) == str:
        if is_parse:
            save_data = json.loads(data)
            save_data = json.dumps(save_data, ensure_ascii=False, indent=4)
        else:
            save_data = data
    else:
        save_data = json.dumps(data, ensure_ascii=False, indent=4)

    open(file_path, "w", encoding="utf8").write(save_data)


def get_record_data(file_path, is_json=True):
    data = open(file_path, "r", encoding="utf8").read()
    if is_json:
        data = json.loads(data)

    return data


def dict2ck(ck_dict):
    cookie_list = [k + "=" + v for k, v in ck_dict.items()]
    cookie = ';'.join(item for item in cookie_list)
    return cookie


def del_progress():
    time.sleep(0.2)


def progress_print(total_cnt=20, index_cha='+', pro_total_cnt=50, fun=None):
    """
    :param total_cnt: 总循环次数
    :param index_cha: 进度指示符号，可以任意替换喜欢的符号
    :param pro_total_cnt: 100%进度显示的总符号个数
    :param fun: 每次进度循环处理的回调函数
    """

    start_time = time.time()
    for i in range(total_cnt):
        current_cnt = int((i + 1) / total_cnt * pro_total_cnt)
        str_progress = index_cha * current_cnt + ' ' * (pro_total_cnt - current_cnt)
        spend_time = time.time() - start_time
        print("\033[31m\r{:.1%} [{}] total time: {:.2f}s\033[0m".format((i + 1) / total_cnt, str_progress, spend_time),
              end="", flush=True)
        if fun is not None:
            fun()


def wait_time(seconds):
    def del_progress():
        time.sleep(0.2)

    total_cnt = seconds * 5

    progress_print(total_cnt=total_cnt, fun=del_progress)

def get_current_location():
    # 获取当前的帧
    frame = inspect.currentframe()
    # 获取帧的信息，包括文件名和行号
    frame_info = inspect.getframeinfo(frame.f_back)
    # 返回文件名和行号
    return frame_info.filename, frame_info.lineno


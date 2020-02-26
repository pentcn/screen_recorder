from apscheduler.schedulers.background  import BackgroundScheduler
from pyautogui import screenshot
from PIL import Image
from datetime import datetime
from time import sleep
import sys
import os

from setting import capture_time, create_pdf_time

SHOTS_DIRCTORY_NAME = 'shots'
PDF_DIRCTORY_NAME = 'pdfs'

def capture_screen():
    file_name = os.path.join(sys.path[0] , SHOTS_DIRCTORY_NAME , datetime.now().strftime('%y%m%d%H%M%S.png'))
    screenshot(file_name)
    print(datetime.now())


def create_pdf_from_pics(path):
    file_start = datetime.today().strftime('%y%m%d')
    pics =[p for p in os.listdir(path) if p.endswith('.png') and p.startswith(file_start)]
    pics.sort()
    images = []
    for pic in pics:
        images.append(Image.open(os.path.join(path,pic)).convert('RGB'))

    pdf_file = os.path.join(PDF_DIRCTORY_NAME,file_start+'.pdf')
    if len(images) > 1:
        images[0].save(pdf_file, save_all=True, append_images=images[1:])
    else:
        images[0].save(pdf_file)
    
    for pic in pics:
        os.remove(os.path.join(path,pic))
    
    print('pdf文件创建完成')

if __name__ == '__main__':
    scheduler = BackgroundScheduler()

    # 生成每个时间点的截屏任务
    today = datetime.today()   
    for t in capture_time:
        task_time = today.replace(hour=int(t.split(':')[0]), minute=int(t.split(':')[1]), second=0, microsecond=0)
        scheduler.add_job(capture_screen, 'date', run_date=task_time)

    # 生成创建pdf文件的任务
    picture_path = os.path.join(sys.path[0],SHOTS_DIRCTORY_NAME)
    create_time = today.replace(hour=int(create_pdf_time.split(':')[0]), minute=int(create_pdf_time.split(':')[1]), second=0, microsecond=0)
    scheduler.add_job(create_pdf_from_pics, 'date', run_date=create_time, args=(picture_path,))
    
    # 启动所有任务
    scheduler.start()

    # 循环等待用户中止程序
    while True:
        sleep(1)

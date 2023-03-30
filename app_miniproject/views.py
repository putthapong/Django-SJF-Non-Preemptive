from ctypes import pointer
from django.shortcuts import render
from django.http.response import HttpResponse , HttpResponseRedirect
import random
from .models import PCB
from django.urls import reverse
import sys
# Create your views here.

class Queuese(): # คลาสสำหรับการจัดการคิวต่าง ๆ 
    def __init__(self):
        self.__job_queue = {} # ประการตัวแปร Job คิว แบบ Private จะใช้ __ ในการระบุถึง Privete
        self.__ready_queue = {} # ประการตัวแปร Ready คิว
        self.__io_queue = {} # ประการตัวแปร IO คิว หรือ Waitting คิว
        self.__memory = 0 # ประการตัวแปร memory ไว้สำหรับทราบถึงขนาด Process ที่อยู่ในเครื่องมีขนาดเท่าไหร่ (คล้ายๆ Ram)
       
    #### Memory ####
    def setMemory(self): # ถ้าถูกเรียกใช้ Set Memory จะทำการตั้งค่าขนาด Process ที่อยู่ในเครื่อง
        job_in_memory = {pointer:data for pointer,data in self.__job_queue.items() if data['State'] != 'Terminate'} #ทำการวนลูปทุกๆ Process ที่ State ไม่ใช่ Terminate ที่อยู่ใน job คิว
        if len(job_in_memory) > 0: # ถ้ามี Process ที่ State ไม่ใช่ Terminate มากกว่า 0
            self.__memory = sys.getsizeof(job_in_memory) # ทำการ get ขนาดของprocess ที่ขอพื้นที่ในmemory
        else: # ถ้าไม่ใช่ให้
            self.__memory = 0  # ทำการ set ขนาดของ memory ให้มีค่าเท่ากับ 0
        
    def getMemory(self): 
        return self.__memory

    #### Clear ####
    def clear(self): # ฟังก์ชัั่นสำหรับการ clear คิวต่าง ๆ 
        self.__job_queue.clear()
        self.__ready_queue.clear()
        self.__io_queue.clear()

    def addJob(self,Arrival_time,pointer): # ฟังก์ชั่นสำหรับการ Add job เข้ามาในระบบ
        Arrival_time = Arrival_time  # Arrival_time คือ เป็นเวลาที่ทำการกดปุ่ม add process
        random_Burst = random.randint(2, 20)
        if pointer == 1: # ถ้า Process เป็นตำแหน่งแรกให้ทำการ set State -> Running 
            self.__job_queue[pointer] = {
            'ID':pointer,
            'State':'Runing', # - #
            'Arrival':Arrival_time,
            'Burst':random_Burst,
            'Execue':0,
            'BE':random_Burst-0,
            'Waitting':0,
            'IO':0,
            'IOW':0
            }
        else: # แต่ถ้าไม่ใช่ตำแหน่งแรกให้ทำการ set State -> New
            self.__job_queue[pointer] = {
                'ID':pointer,
                'State':'New',  # - #
                'Arrival':Arrival_time,
                'Burst':random_Burst,
                'Execue':0,
                'BE':random_Burst-0,
                'Waitting':0,
                'IO':0,
                'IOW':0
            }
    #### Job Queue ####
    def setJobQueue(self,pointer,job): 
        self.__job_queue[pointer] = job
        
    def getJobQueue(self):
        return self.__job_queue

    #### Ready Queue ####
    def setReadyQueue(self,pointer = None): # ฟังก์ชั่นสำหรับการ set ready คิว  
        if pointer != None: # Waitting -> Ready ถ้า pointer ที่ส่งมาไม่ใช่ none แสดงว่า process นั้นจะถูกส่งมาจาก IO คิว หรือ Waitting คิว จะถูกอัพเดทให้เป็น State Ready
            update_state = {'State':'Ready'}
            self.__job_queue[pointer].update(update_state)
            self.__ready_queue[pointer] = self.__job_queue[pointer]
        else: # New -> Ready ถ้า pointer ที่ส่งมาเป็น none แสดงว่า process นั้นจะเป็น process ที่พึ่ง add job มาใหม่
            for pointer in self.__job_queue: # ทำการวนลูป job คิวทั้งหมด  
                if self.__job_queue[pointer]['State'] == 'New': # ทำการตรวจสอบว่า process นั้นมี state เป็น New ถ้าใช้จะถูกอัพเดทให้เป็น State Ready
                    update_state = {'State':'Ready'}
                    self.__job_queue[pointer].update(update_state)
                    self.__ready_queue[pointer] = self.__job_queue[pointer]

    def getReadyQueue(self):
        self.__ready_queue = {pointer:data for pointer,data in self.__job_queue.items() if data['State'] == 'Ready'} # ทำการวนลูป job คิวแล้วตรวจสอบ State ว่าเป็น Ready ถ้าใช้จะเป็นไว้ที่ตัวแปร __ready_queue
        return self.__ready_queue

    def popReadyQueue(self,pointer):
        self.__ready_queue.pop(pointer)
    
    #### I/O Queue ####
    def getIoQueue(self):
        self.__io_queue = {pointer:data for pointer,data in self.__job_queue.items() if data['State'] == 'Waitting'} # ทำการวนลูป job คิวแล้วตรวจสอบ State ว่าเป็น Waitting ถ้าใช้จะเป็นไว้ที่ตัวแปร __io_queue
        return self.__io_queue

    def setIoQueue(self,pointer): # ฟังก์ชั่นสำหรับ set io คิว ซึ่งจะส่ง pointer มา pointer ที่ถูกส่งมานั้นจะเป็น State Running จะถูกอัพเดทให้เป็น State Waitting
        update_state = {'State':'Waitting'} 
        self.__job_queue[pointer].update(update_state)
        self.__io_queue[pointer] = self.__job_queue[pointer]

    def popIOQueue(self,pointer):
        self.__io_queue.pop(pointer)

class Clock(): # คลาสสำหรับจัดการเกี่ยวกับเวลา
    def __init__(self):
        self.__time = 0
        
    #### Clear ####
    def clear(self): # ทำการ reset ให้เป็น เวลาเริ่มต้น
        self.__time = 0

    #### Time ####
    def setTime(self): # ฟังก์ชั่น ในการบวกเวลาเพิ่มทีละ 1
        self.__time = self.__time + 1

    def getTime(self):
        return self.__time

pcb = PCB()
clock = Clock()
queuese = Queuese()

def home(request):
    return render(request,'home.html')

#### Index #####
def index(request):
    contexts = {
        'clock':clock.getTime(),
        'job_queue':queuese.getJobQueue(),
        'ready_queue':pcb.getList_of_open_file(),
        'io_queue':queuese.getIoQueue(),
        'programe_counter':pcb.getProgram_counter(),
        'programe_counter_io':pcb.getProgram_counter_IO(),
        'memory':queuese.getMemory(),
        'bar':progress_bar(),
    }
    return render(request,'index.html',context=contexts)

#### Add Process and Reset ####
def preprocess(request):
    clock_time = clock.getTime()
    if 'add' in request.POST:
        pointer = len(queuese.getJobQueue())+1
        if pointer == 1:
            queuese.addJob(Arrival_time=clock_time,pointer=pointer)
            pcb.setProgram_counter(pointer)
            pcb.setList_of_open_file([(queuese.getJobQueue()[1])])          
        else:
            queuese.addJob(Arrival_time=clock_time,pointer=pointer)
    elif 'reset' in request.POST:
        clock.clear()
        queuese.clear()
        pcb.clearList_of_open_file()
        pcb.setProgram_counter(pointer=None)
        pcb.setProgram_counter_IO(pointer=None)
    return HttpResponseRedirect(reverse('index'))

#### Terminate ####
def terminates(request):
    pointer = int(request.POST['terminate'])
    job = queuese.getJobQueue()[pointer]
    update_state = {'State':'Terminate'}
    job.update(update_state)
    queuese.setJobQueue(pointer,job)
    pcb.setProgram_counter(pointer = None)
    return HttpResponseRedirect(reverse('index'))
    
#### Add I/O ####
def add_io(request):
    if pcb.getProgram_counter() != None:
        pointer = pcb.getProgram_counter()
        queuese.setIoQueue(pointer)
        pcb.popList_of_open_file(pointer)
        pcb.setProgram_counter(pointer=None)
        
    return HttpResponseRedirect(reverse('index'))

def close_io(request):
    pointer = int(request.POST['close'])
    queuese.setReadyQueue(pointer)
    queuese.popIOQueue(pointer)
    sortReady_Queue()
    pcb.setProgram_counter_IO(pointer=None)  
    return HttpResponseRedirect(reverse('index'))

#### Progress ####
def progress_bar():
    return int(queuese.getMemory())*100/(5000) # 5 Kbyte

#### Time ####
def time(request):
    clock.setTime()
    queuese.setMemory()
    if len(queuese.getJobQueue()) > 0:
        queuese.setReadyQueue()
        non_preemptive_SJF()
        sortReady_Queue()
        wating_time()
    if len(queuese.getIoQueue()) > 0:
        io_process()
        wating_time_io()
    contexts = {
        'clock':clock.getTime(),
        'job_queue':queuese.getJobQueue(),
        'ready_queue':pcb.getList_of_open_file(),
        'io_queue':queuese.getIoQueue(),
        'programe_counter':pcb.getProgram_counter(),
        'programe_counter_io':pcb.getProgram_counter_IO(),
        'memory':queuese.getMemory(),
        'bar':progress_bar(),
    }
    return render(request,'index.html',context=contexts)

#### Non Preemptive SJF ####
def job_in_cpu(job):
    if job['BE'] > 0:
        execue = job['Execue']+1
        update_state = {
            'State':'Runing',
            'Execue':execue,
            'BE':job['Burst']-execue}
        job.update(update_state)
        queuese.setJobQueue(job['ID'],job)
    else:
        update_state = {'State':'Terminate'}
        job.update(update_state)
        queuese.setJobQueue(job['ID'],job)
        sortReady_Queue()
        if len(pcb.getList_of_open_file()) > 0:
            pcb.setProgram_counter(pcb.getList_of_open_file()[0]['ID']) # set Program counter == file แรกที่ถูก Sort Burst time
        else:
            pcb.setProgram_counter(None)

def sortReady_Queue():
    if len(queuese.getReadyQueue()) > 0:
        list_sort = sorted(queuese.getReadyQueue().values(),key=lambda d:d['BE'],reverse=False) # Sort Burst 
        pcb.setList_of_open_file(list_sort)
    else:
        pcb.setList_of_open_file([])

def non_preemptive_SJF():
    if pcb.getProgram_counter() == None:
        sortReady_Queue()
        if len(pcb.getList_of_open_file()) > 0:
            pcb.setProgram_counter(pcb.getList_of_open_file()[0]['ID'])
            if pcb.getProgram_counter() != None:
                job_in_cpu(queuese.getJobQueue()[pcb.getProgram_counter()])
    else:
            job_in_cpu(queuese.getJobQueue()[pcb.getProgram_counter()])

#### Wating Time ####
def wating_time():
    for pointer,job in queuese.getJobQueue().items():
         if job['State'] == 'Ready' and job['ID'] != pcb.getProgram_counter():
            update_state = {'Waitting':job['Waitting']+1}
            job.update(update_state)
            queuese.setJobQueue(pointer,job)

#### IO Process ####
def job_in_io(job):
    update_state = {'IO':job['IO']+1}
    job.update(update_state)
    queuese.setJobQueue(job['ID'],job)

def io_process():
    if pcb.getProgram_counter_IO() == None:
        pointer = list(queuese.getIoQueue())[0]
        pcb.setProgram_counter_IO(pointer)
        job_in_io(queuese.getJobQueue()[pcb.getProgram_counter_IO()])
    else:
        job_in_io(queuese.getJobQueue()[pcb.getProgram_counter_IO()])

def wating_time_io():
    for pointer,job in queuese.getJobQueue().items():
         if job['State'] == 'Waitting' and job['ID'] != pcb.getProgram_counter_IO():
            update_state = {'IOW':job['IOW']+1}
            job.update(update_state)
            queuese.setJobQueue(pointer,job)
            

# การทำงาน SJF Nonpreemptive 
# - เมื่อ add Process แรกมาแล้ว จะทำการรัน Prcess นั้นเลย หากมี Process เข้ามาในช่วงที่รันอยู่จะไม่ถูกแทรกการทำงานเนื่องจากเป็น Nonpreemptive 
# - เมื่อรันเสร็จจะทำการ sort หรือเลือก Process ที่จะมาทำงานใหม่จาก Burst time ที่น้อยที่สุดก่อน

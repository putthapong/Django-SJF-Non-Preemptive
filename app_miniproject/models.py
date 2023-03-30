class PCB(): # Process Contol Block โปรแกรมเราใช้ภาษา Python ในการเขียน ใช้เฟรมเวิร์ค Django (ดีจังโก้)
    def __init__(self): # ฟังก์ชั่นหลักหรือฟังก์ชั่น main 
        self.__program_counter = None # สำหรับเก็บตำแหน่งของโปรแกรมที่อยู่ใน CPU หรือโปรแกรมที่มีสถานะ Running 
        self.__list_of_open_file = {} # สำหรับเก็บ Process ที่ถูกเรียงลำดับ Burst Time ของ Ready คิว จากน้อยไปมาก
        self.__program_counter_IO = None # สำหรับเก็บตำแหน่งของโปรแกรมที่อยู่ใน IO 
 
    # Get คือการดูหรือเรียกขอดู , Set คือการตั้งค่าหรือตั้งค่าใหม่

    #### List of Open File ####  
    def clearList_of_open_file(self):
        self.__list_of_open_file.clear()

    def setList_of_open_file(self,list_file): # ถ้าถูกเรียกใช้ฟังก์ชั่น Set list_of_open_file จะทำการตั้งค่า Process ที่ถูกเรียงลำดับ Burst Time ของ Ready คิว จากน้อยไปมากใหม่
        self.__list_of_open_file = list_file # list_file จะถูกเรียงลำดับมา Burst Time จากน้อยไปมาก

    def getList_of_open_file(self): # ถ้าถูกเรียกใช้ฟังก์ชั่น Get list_of_open_file จะทำการเรียกดู Process ที่ถูกเรียงลำดับ Burst Time ของ Ready คิว จากน้อยไปมาก
        return  self.__list_of_open_file

    def popList_of_open_file(self,pointer): # ส่งพารามิเตอร์มา pop  ฟังก์ชันนี้
        for index,data in enumerate(self.__list_of_open_file):
            if data['ID'] == pointer: 
                self.__list_of_open_file.pop(index) 
        
    #### Program Counter ####
    def setProgram_counter(self,pointer): # ถ้าถูกเรียกใช้ฟังก์ชั่น Set Programe_counter จะทำการตั้งตำแหน่งของโปรแกรมที่กำลังรันอยู่ใน CPU ใหม่
        self.__program_counter = pointer

    def getProgram_counter(self): # ถ้าถูกเรียกใช้ฟังก์ชั่น Get Programe_counter จะทำการเรียกดูตำแหน่งของโปรแกรมที่กำลังรันอยู่ใน CPU 
        return self.__program_counter

     #### Program Counter IO ####
    def setProgram_counter_IO(self,pointer): # ถ้าถูกเรียกใช้ฟังก์ชั่น Set Programe_counter_IO จะทำการตั้งค่าตำแหน่งของโปรแกรมที่กำลังรันอยู่ใน IO  ใหม่
        self.__program_counter_IO = pointer

    def getProgram_counter_IO(self): # ถ้าถูกเรียกใช้ฟังก์ชั่น Get Programe_counter_IO จะทำการเรียกดูตำแหน่งของโปรแกรมที่กำลังรันอยู่ใน IO
        return self.__program_counter_IO

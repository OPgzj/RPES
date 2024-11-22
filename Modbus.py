#采用Modbus-rtu协议，通过03（读保持寄存器），06（写单个字节），16（0x10，写多个保持寄存器），06返回的是8位定长数据
"""
协议介绍（均为16进制）:
获取重量指令：01 03 00 00 00 02 C4 0B 
01：从机选择
03：功能码，读保持寄存器
00 00 ：寄存器起始地址的高8位与低8位，表示开始地址位0x00
00 02 ：寄存器数量的高8位与低8位,表示读取两个地址为，即结束地址为0x02
C4 0B :CRC校验码

获取小数位置：01 03 00 02 00 01 25 CA
获取天平状态：01 03 00 03 00 01 74 0A
置零操作：01 06 00 04 00 01 09 CB
一次性获取重量小数点和状态指令：01 03 00 00 00 04 44 09

"""
import serial
import struct
import time

class ScaleModbusRTU:
    """
        初始化Modbus RTU串口连接。
        参数:
        port: 串口号，例如 '/dev/ttyUSB0' 或 'COM9',根据实际情况传入
        baudrate: 波特率，默认9600
        timeout: 读取超时时间，默认1秒
    """
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=1):  # 串口号，波特率，超时时间
        self.ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=timeout
        )
        self.decimal_position = self.get_decimal()

    """
        计算CRC16校验码。

        参数:
        data: 要计算CRC的字节数据

        返回:
        计算得到的CRC16校验码
    """
    def crc16(self, data: bytes):  # CRC校验
        crc = 0xFFFF  # 预置1个16位的寄存器为十六进制FFFF
        for pos in data:
            crc ^= pos  # 低字节
            for _ in range(8):
                if crc & 1:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc
    """
        发送Modbus命令并附加CRC校验码。

        参数:
        command: 要发送的Modbus命令字节数据
    """
    def send_command(self, command: bytes):  # 发送命令
        crc = self.crc16(command)  # 计算CRC校验
        command += struct.pack('<H', crc)  # 高低字节交换并追加到command
        self.ser.write(command)

    """
        接收Modbus响应数据并进行CRC校验。

        返回:
        接收到的响应数据
    """
    def receive_response(self):
        # 读取头部（地址 + 功能码 + 字节数 = 3个字节）
        header = self.ser.read(3)
        if len(header) < 3:
            raise Exception("未收到完整响应头部")
        
        address, function, byte_count = struct.unpack('BBB', header)

        # 读取数据（数据字节数 + CRC校验的两个字节 = byte_count + 2）
        data = self.ser.read(byte_count + 2)  # 数据长度+CRC
        if len(data) < byte_count + 2:
            raise Exception(f"未收到完整响应数据: 收到 {len(data)} 字节，期望 {byte_count + 2} 字节")

        # 合并header和data
        response = header + data

        # 校验CRC
        crc_received = struct.unpack('<H', response[-2:])[0]  # 从响应中提取CRC
        calculated_crc = self.crc16(response[:-2])  # 计算CRC
        if calculated_crc != crc_received:
            raise Exception(f"CRC校验失败: 预期 {crc_received}, 实际 {calculated_crc}")
        
        return response


    """
        接收8位Modbus响应数据并进行CRC校验。

        返回:
        接收到的8位响应数据
    """
    def receive_8bitresponse(self):
        """接收Modbus响应数据"""
        # 写单个寄存器的响应固定为 8 字节
        expected_length = 8  # 固定响应长度为 8 字节

        response = self.ser.read(expected_length)
        
        if len(response) < expected_length:
            raise Exception("未收到完整响应数据")


        # 校验CRC
        crc_received = struct.unpack('<H', response[-2:])[0]
        if self.crc16(response[:-2]) != crc_received:
            raise Exception(f"CRC校验失败: 预期 {crc_received}, 实际 {self.crc16(response[:-2])}")
        
        return response
    
    """
        解析16位的天平状态值。

        参数:
        status: 16位的天平状态值

        返回:
        解析后的状态信息，包括零点状态、称重稳定状态、过载状态和单位
    """       
    def parse_scale_status(self, status):
        """解析16位的天平状态值"""
        zero_state = status & 0x01  # 第0位，零点状态
        stable_state = (status >> 1) & 0x01  # 第1位，称重稳定状态
        overload_state = (status >> 2) & 0x01  # 第2位，过载状态
        
        unit_code = (status >> 3) & 0x1F  # 第3-7位，单位信息（提取5位）
        
        
        # 单位信息对应的单位名称
        unit_dict = {
            0: "ct", 1: "lb", 2: "oz", 3: "ozt", 4: "dr", 5: "lbt", 6: "gr", 7: "dwt",
            8: "tl", 9: "T.tl", 10: "H.tl", 11: "S.tl", 12: "T", 13: "M", 14: "CI", 15: "Mom",
            16: "BG",17:"kg",18:"mg",19:"g"
        }
        
        # 使用get方法防止单位代码超出字典范围
        unit = unit_dict.get(unit_code, "未知单位")
        
        return {
            "零点状态": "零点" if zero_state == 1 else "非零点",
            "称重稳定状态": "稳定" if stable_state == 1 else "不稳定",
            "过载状态": "超载" if overload_state == 1 else "正常",
            "单位": unit
        }

    
    """
        执行Modbus命令并返回响应数据。

        参数:
        command: 要执行的Modbus命令

        返回:
        响应数据
    """
    def execute_command(self, command: bytes):
        """
        通用函数，用于执行任何Modbus命令
        command: 要发送的Modbus命令
        """
        self.send_command(command)
        response = self.receive_response()
        return response

    """
        执行8位Modbus命令并返回响应数据。
        控制码为06时，调用该函数
        参数:
        command: 要执行的8位Modbus命令

        返回:
        响应数据
    """
    def execute_8bitcommand(self, command: bytes):
        self.send_command(command)
        response = self.receive_8bitresponse()
        return response
    def close(self):  # 关闭串口
        if self.ser and self.ser.is_open:
            self.ser.close()
    """
        多点校准步骤:
        1. 清空秤台
        2. 40008地址写入1，启动四点校准
        3. 查询40009的bit4-bit5，直到该值为1，表示可以加载砝码
        4. 查询40010，根据提示放上相应重量的砝码
        5. 放上砝码后，查询40009，bit4-bit5为0，直到该值为2，表示可以取下砝码
        6. 循环执行步骤3-5，直到完成所有校准点
        7. 标定结束后，40009的bit7置1，表示校准成功
    """
    def multi_point_calibration(self):
        # 1. 清空秤台
        print("请清空秤台")

        # 2. 40008地址写入1，启动四点校准
        self.execute_8bitcommand(b'\x01\x06\x00\x07\x00\x01')

        while True:
            # 3. 查询40009的bit4-bit5，直到该值为1，表示可以加载砝码
            response = self.execute_command(b'\x01\x03\x00\x08\x00\x01')
            calibration_status = response[4]
            if (calibration_status >> 4) & 0x03 == 1:
                print("请加载砝码")
                break
            time.sleep(1)  # 等待1秒再发送下一次查询
        # 4. 查询40010，根据提示放上相应重量的砝码
        while True:
            response = self.execute_command(b'\x01\x03\x00\x09\x00\x01')
            calibration_weight = struct.unpack('>H', response[3:5])[0]
            print(f"请放上 {calibration_weight}g 的砝码")
            time.sleep(1)  # 等待1秒再发送下一次查询
            # 5. 放上砝码后，查询40009的bit4-bit5为0，直到该值为2，表示可以取下砝码
            while True:
                response = self.execute_command(b'\x01\x03\x00\x08\x00\x01')
                calibration_status = response[4]
                if (calibration_status >> 4) & 0x03 == 2:
                    print("可以取下砝码")
                    break
                time.sleep(1)  # 等待1秒再发送下一次查询            
            # 检查是否完成所有校准点，查询bit0-bit3
            current_point = calibration_status & 0x0F
            print(f"当前标定点数: {current_point}")
            if current_point == 0:
                break  # 完成所有标定点

        # 7. 标定结束后，40009的bit7置1，表示校准成功
        response = self.execute_command(b'\x01\x03\x00\x08\x00\x01')
        calibration_complete = response[4]
        if (calibration_complete >> 7) & 0x01 == 1:
            print("校准成功")
        else:
            print("校准失败")

    """
        单点校准步骤:
        1. 清空秤台
        2. 40008地址写入2，启动单点校准
        3. 查询40009的bit4-bit5，直到该值为1，表示可以加载砝码
        4. 查询40010，根据提示放上相应重量的砝码
        5. 放上砝码后，查询40009的bit4-bit5为0
        6. 标定结束后，40009的bit7置1，表示校准成功
    """
    def single_point_calibration(self):
        # 1. 清空秤台
        print("请清空秤台")

        # 2. 40008地址写入2，启动单点校准
        self.execute_8bitcommand(b'\x01\x06\x00\x07\x00\x02')

        while True:
            # 3. 查询40009的bit4-bit5，直到该值为1，表示可以加载砝码
            response = self.execute_command(b'\x01\x03\x00\x08\x00\x01')
            calibration_status = response[4]
            if (calibration_status >> 4) & 0x03 == 1:
                print("请加载砝码")
                break
            time.sleep(1)  # 等待1秒再发送下一次查询
        # 4. 查询40010，根据提示放上相应重量的砝码
        response = self.execute_command(b'\x01\x03\x00\x09\x00\x01')
        calibration_weight = struct.unpack('>H', response[3:5])[0]
        print(f"请放上 {calibration_weight}g 的砝码")

        # 5. 放上砝码后，查询40009的bit4-bit5为0
        while True:
            response = self.execute_command(b'\x01\x03\x00\x08\x00\x01')
            calibration_status = response[4]
            if (calibration_status >> 4) & 0x03 == 0:
                print("校准完成")
                break
            time.sleep(1)  # 等待1秒再发送下一次查询
        # 6. 标定结束后，40009的bit7置1，表示校准成功
        response = self.execute_command(b'\x01\x03\x00\x08\x00\x01')
        calibration_complete = response[4]
        if (calibration_complete >> 7) & 0x01 == 1:
            print("校准成功")
        else:
            print("校准失败")

    def get_weight(self):
        weight_command = b'\x01\x03\x00\x00\x00\x02'  # 获取重量的命令
        weight_response = self.execute_command(weight_command)  # 响应中第4字节开始为重量数据，根据返回的字节数判断是否有符号32位整数
        # byte_count = weight_response[2]  # 第3字节表示返回数据的长度
        weight = struct.unpack('>i', weight_response[3:7])[0]  # 解析32位有符号整数
        return weight/(10**self.decimal_position)

    def get_decimal(self):
        decimal_command = b'\x01\x03\x00\x02\x00\x01'  # 获取小数点位置命令
        decimal_response = self.execute_command(decimal_command)
        decimal_position = decimal_response[4]  # 小数点位置在返回数据的第5字节
        return decimal_position

    def get_zero(self):
        zero_command = b'\x01\x06\x00\x04\x00\x01'  # 置零操作命令
        zero_response = self.execute_8bitcommand(zero_command)  # 返回的是8位定长数据
        print(f"置零操作响应: {zero_response.hex().upper()}")  # 发送与返回相等即置零成功


# 使用示例
if __name__ == '__main__':
    scale = None

    try:
        # 初始化串口
        scale = ScaleModbusRTU(port='COM6', baudrate=9600, timeout=1)  # 连接串口,其中"COM9"为串口号，根据实际情况输入，其他参数保持不变
        print(scale.decimal_position)

        # 1. 获取重量（不定长度响应),其他命令可以依此类推，比如获取小数点位置、天平状态等


        # weight_command = b'\x01\x03\x00\x00\x00\x02'  # 获取重量的命令
        # weight_response = scale.execute_command(weight_command)  # 响应中第4字节开始为重量数据，根据返回的字节数判断是否有符号32位整数
        # byte_count = weight_response[2]  # 第3字节表示返回数据的长度
        # weight = struct.unpack('>i', weight_response[3:7])[0]  # 解析32位有符号整数
        # print(f"当前重量: {weight} g")

        # # 2. 获取小数点位置

        #
        # # 3. 获取天平状态
        # status_command = b'\x01\x03\x00\x03\x00\x01'  # 获取天平状态的命令
        # status_response = scale.execute_command(status_command)
        # status = status_response[3]  # 状态信息在返回数据的第4字节
        # st1 = status_response[3]  # 状态的高8位
        # st2 = status_response[4]  # 状态的低8位
        # status = (st1 << 8) | st2  # 将st1和st2组合成16位状态数据
        # parsed_status = scale.parse_scale_status(status)#解析状态
        # print(f"天平状态: {parsed_status}")
        #
        # # 4. 置零操作
        weight = scale.get_weight()
        print(f"当前重量: {weight} g")
        scale.get_zero()
        weight = scale.get_weight()
        print(f"当前重量: {weight} g")
        #
        # # 5. 一次性获取重量、小数点和状态
        # combined_command = b'\x01\x03\x00\x00\x00\x04'  # 一次性获取重量、小数点和状态的命令
        # combined_response = scale.execute_command(combined_command)
        # weight = struct.unpack('>i', combined_response[3:7])[0]  # 解析重量数据
        # decimal_position = combined_response[8]  # 小数点位置
        # st1 = combined_response[9]  # 状态的高8位
        # st2 = combined_response[10]  # 状态的低8位
        # status = (st1 << 8) | st2  # 将st1和st2组合成16位状态数据
        # parsed_status = scale.parse_scale_status(status) # 解析天平状态
        # print(f"重量: {weight} g, 小数点位置: {decimal_position}, 天平状态: {parsed_status}")
        #
        # # 6. 调用多点校准
        # scale.multi_point_calibration()
        #
        # # 7. 调用单点校准
        # scale.single_point_calibration()

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        if scale is not None:
            scale.close()

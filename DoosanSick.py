# -*- coding: utf-8 -*-
"""
DoosanSick class is used for the dialogue between a SICK camera and a Doosan robot.
Please read the README.md file before use.
Copyright (C) 2022 HumaRobotics

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# Keep thoses lines in order to test the code without a Doosan:
import socket
tp_popup = print
tp_log = print
DR_PM_ALARM = 'ALARM POPUP'

socket_IN = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

is_first_client = True
def client_socket_open(ip, port):
    global is_first_client
    print("port", port)
    if is_first_client:
        r = socket_IN.connect((ip, port))
        is_first_client = False
    else:
        r = socket_IN.connect((ip, port))
    return r

def client_socket_read(_socketIN, length, timeout):
    r = socket_IN.recv(14158)
    return 10,r

def client_socket_write(_socketIN, send_TRG):
    socket_IN.send(send_TRG)

#####################
# DON'T FORGET TO REMOVE THOSE LINES ABOVE BEFORE USED ON THE DOOSAN

class DoosanSick:
    """
    Interface to use SICK camera with Doosan robot
    """

    def __init__(self, ip="192.168.0.5", portIN=14158):
        """
        Initialize the connection between the camera and the Doosan.
        
        Params:\n
            - 'ip': ip of SICK camera
            - 'portIN': port number of the camera TCP connection
        """

        self.ip = ip
        self.portIN = portIN
        self.nb_parts = 0

        tp_log("Connexion to the camera : ")
        try:
            self._socketIN = client_socket_open(self.ip, self.portIN)
            tp_log("Connection to the camera ok !")
        except Exception as e:
            tp_popup("Socket connection failed. Error: {0}".format(
                str(e)), DR_PM_ALARM)
            raise e


    def write(self, cmd, socket = None):
        """
        Write 'cmd' in the socket
        
        Params:\n
            - 'cmd': a TCP Protocol command
	        - 'socket': socket to write (None will write to default socket)
         
        Return:\n
            - 'res': result of the writing
        """

        if socket == None:
            socket = self._socketIN

        # Convert cmd in ascii before sending
        cmd = bytes(cmd, encoding="ascii")

        res = client_socket_write(socket, cmd)

        # Check res value
        if res == -1:
            tp_log("error  " + 
                "Error during a socket write: Server not connected")
        elif res == -2:
            tp_log("error  " + 
                "Error during a socket write: Socket error")
        elif res == 0:
            tp_log("info " + 
                "Sending {0} command ok".format(cmd))
        return res


    def read(self, length=-1, timeout=-1, socket = None):
        """
        Read the socket
        
        Params:\n
            - 'length': number of bytes to read (default = -1)
            - 'timeout': waiting time (default = -1)
            - 'socket': socket to read (None will read to default socket)
            
        Return:\n
            - 'res': result of the reading
            - 'rx_data': data received
        """

        if socket == None:
            socket = self._socketIN

        res, rx_data = client_socket_read(socket, length, timeout)
        #rx_data type is bytes so we will need to decode it before using it

        # Check res value
        if res == -1:
            tp_log("error " + 
                "Error during a socket read: Server not connected")
        elif res == -2:
            tp_log("error " + 
                "Error during a socket read: Socket error")
        elif res == -3:
            tp_log("error " + 
                "Error during a socket read: Waiting time has expired")
        elif res > 0:
            tp_log("info" + 
                "Read res = {0} and rx_data = {1}".format(res, rx_data))

        # tp_popup("res={0}, rx_data={1}".format(res, rx_data))
        return res, rx_data
    
    
    def get_nb_parts(self, job_number=1):
        """
        Send `Run.Locate, Job` to the camera in order to trigger a capture
        
        Params:\n
            - 'job_number': int corresponding to the number of the job to call (between 1 and 256, default = 1)
            
        Return:\n
            - 'nb_parts': int corresponding to the number of parts located in the capture
        """
        
        cmd = "Run.Locate, " + str(job_number)
        self.write(cmd)
        res, rx_data = self.read()
        decoded_rx_data = rx_data.decode()
        #tp_log(decoded_rx_data)
        
        read_locate = decoded_rx_data.split(',')
        valid_locate = read_locate[0].split('.')[2]
        
        if valid_locate=="Ok":
            tp_log("Capture successful")
            self.nb_parts = int(read_locate[3])
            return self.nb_parts
            
        elif valid_locate=="Error":
            tp_log("error " + 
                "Error during the capture : " + read_locate[-1])
            return None
            
        else:
            tp_log("error" + 
                "Unknown error in get_nb_part")
            return None
        
        
    def locate_one_part(self, job_number=1, part_number=1):
        """
        Send `Run.Locate, Job, Match` to the camera in order to trigger a capture and locate the selected part
        
        Params:\n
            - 'job_number': int corresponding to the number of the job to call (between 1 and 256, default = 1)
            - 'part_number': int corresponding to the number of the part to locate (default = 1)
            
        Return:\n
            - '(x, y, z, r1, r2, r3, scale, score, match_time, exposure, identified)': tuple with part position and capture informations
        """

        if (part_number==0) or (part_number<0) or (part_number>self.nb_parts):
            tp_log("error" + 
                "Wrong part number")
            return None
        
        else:    
            cmd = "Run.Locate, " + str(job_number) + ", " + str(part_number)
            self.write(cmd)
            res, rx_data = self.read()
            decoded_rx_data = rx_data.decode()
            #tp_log(decoded_rx_data)
            
            read_locate = decoded_rx_data.split(',')
            valid_locate = read_locate[0].split('.')[2]
            datas = read_locate[4:]
            
            if valid_locate=="Ok":
                tp_log("Capture successful")

                x = float(datas[0])
                y = float(datas[1])
                z = float(datas[2])
                r1 = float(datas[3])
                r2 = float(datas[4])
                r3 = float(datas[5])
                scale = float(datas[6])
                score = int(datas[7])
                match_time = int(datas[8])
                exposure = int(datas[9])
                identified = int(datas[10])
                
                #tp_log("x: {0}, y: {1}, z: {2}, r1: {3}, r2: {4}, r3: {5}, scale: {6}, score: {7}, time: {8}, exposure: {9}, identified: {10}".format(x,y,z,r1,r2,r3,scale,score,match_time,exposure,identified))
                return (x, y, z, r1, r2, r3, scale, score, match_time, exposure, identified)
            
            elif valid_locate=="Error":
                tp_log("error " + 
                    "Error during the capture : " + read_locate[-1])
                return None
            
            else:
                tp_log("error" + 
                    "Unknown error Run.Locate!")
                return None
        
    
    def locate_all_parts(self, job_number=1):
        """
        Send `Run.LocateAll, Job` to the camera in order to trigger a capture and get the position of each part located
        
        Params:\n
            - 'job_number': int corresponding to the number of the job to call (between 1 and 256, default = 1)
            
        Return:\n
            - '[[x, y, z, r1, r2, r3, scale, score, exposure], ...]': list of the datas (position, scale, score, exposure) send back by the camera for each part located
        """
        
        cmd = "Run.LocateAll, " + str(job_number)
        self.write(cmd)
        res, rx_data = self.read()
        decoded_rx_data = rx_data.decode()
        #tp_log(decoded_rx_data)
        
        read_locate = decoded_rx_data.split(',')
        valid_locate = read_locate[0].split('.')[2]
        datas = read_locate[2:]
        
        if valid_locate=="Ok":
            tp_log("Capture successful")
            self.nb_parts = int(read_locate[1])
            list_res = []
            
            for i in range(self.nb_parts):
                res_match = []
                new_match = 11*i
                x = float(datas[new_match+2])
                res_match.append(x)
                y = float(datas[new_match+3])
                res_match.append(y)
                z = float(datas[new_match+4])
                res_match.append(z)
                r1 = float(datas[new_match+5])
                res_match.append(r1)
                r2 = float(datas[new_match+6])
                res_match.append(r2)
                r3 = float(datas[new_match+7])
                res_match.append(r3)
                scale = float(datas[new_match+8])
                res_match.append(scale)
                score = int(datas[new_match+9])
                res_match.append(score)
                exposure = int(datas[new_match+10])
                res_match.append(exposure)
                #tp_log("x: {0}, y: {1}, z: {2}, r1: {3}, r2: {4}, r3: {5}, scale: {6}, score: {7}, exposure: {8}".format(x,y,z,r1,r2,r3,scale,score,exposure))
                list_res.append(res_match)
            
            return list_res
                
        elif valid_locate=="Error":
            tp_log("error " + 
                "Error during the capture : " + read_locate[-1])
            return None
            
        else:
            tp_log("error" + 
                "Unknown error in Run.LocateAll!")
            return None

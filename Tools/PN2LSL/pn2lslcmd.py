from pylsl import StreamInfo, StreamOutlet
import socket, time


class Pn2lsl:
    def __init__(self, ip='127.0.0.1', port=7010):

        self.TCP_IP = '127.0.0.1'
        self.TCP_PORT = 7010
        self.BUFFER_SIZE = 1800
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.info = StreamInfo('AxisNeuron', 'BVH', 138, 125, 'float32', 'myuid2424')
        self.info.desc().append_child_value("manufacturer", "AxisNeuron")
        channels = self.info.desc().append_child("channels")


        #for c in ["Y", "X", "Z"]:
        for c in ["J37, X pos", "J37, Y pos", "J37, Z pos", "J37, Yrot", "J37, Xrot", "J37, Zrot",
                  "J38, X pos", "J38, Y pos", "J38, Z pos", "J38, Yrot", "J38, Xrot", "J38, Zrot",
                  "J39, X pos", "J39, Y pos", "J39, Z pos", "J39, Yrot", "J39, Xrot", "J39, Zrot",
                  "J40, X pos", "J40, Y pos", "J40, Z pos", "J40, Yrot", "J40, Xrot", "J40, Zrot",
                  "J41, X pos", "J41, Y pos", "J41, Z pos", "J41, Yrot", "J41, Xrot", "J41, Zrot",
                  "J42, X pos", "J42, Y pos", "J42, Z pos", "J42, Yrot", "J42, Xrot", "J42, Zrot",
                  "J43, X pos", "J43, Y pos", "J43, Z pos", "J43, Yrot", "J43, Xrot", "J43, Zrot",
                  "J44, X pos", "J44, Y pos", "J44, Z pos", "J44, Yrot", "J44, Xrot", "J44, Zrot",
                  "J45, X pos", "J45, Y pos", "J45, Z pos", "J45, Yrot", "J45, Xrot", "J45, Zrot",
                  "J46, X pos", "J46, Y pos", "J46, Z pos", "J46, Yrot", "J46, Xrot", "J46, Zrot",
                  "J47, X pos", "J47, Y pos", "J47, Z pos", "J47, Yrot", "J47, Xrot", "J47, Zrot",
                  "J48, X pos", "J48, Y pos", "J48, Z pos", "J48, Yrot", "J48, Xrot", "J48, Zrot",
                  "J49, X pos", "J49, Y pos", "J49, Z pos", "J49, Yrot", "J49, Xrot", "J49, Zrot",
                  "J50, X pos", "J50, Y pos", "J50, Z pos", "J50, Yrot", "J50, Xrot", "J50, Zrot",
                  "J51, X pos", "J51, Y pos", "J51, Z pos", "J51, Yrot", "J51, Xrot", "J51, Zrot",
                  "J52, X pos", "J52, Y pos", "J52, Z pos", "J52, Yrot", "J52, Xrot", "J52, Zrot",
                  "J53, X pos", "J53, Y pos", "J53, Z pos", "J53, Yrot", "J53, Xrot", "J53, Zrot",
                  "J54, X pos", "J54, Y pos", "J54, Z pos", "J54, Yrot", "J54, Xrot", "J54, Zrot",
                  "J55, X pos", "J55, Y pos", "J55, Z pos", "J55, Yrot", "J55, Xrot", "J55, Zrot",
                  "J56, X pos", "J56, Y pos", "J56, Z pos", "J56, Yrot", "J56, Xrot", "J56, Zrot",
                  "J57, X pos", "J57, Y pos", "J57, Z pos", "J57, Yrot", "J57, Xrot", "J57, Zrot",
                  "J58, X pos", "J58, Y pos", "J58, Z pos", "J58, Yrot", "J58, Xrot", "J58, Zrot",
                  "J59, X pos", "J59, Y pos", "J59, Z pos", "J59, Yrot", "J59, Xrot", "J59, Zrot", ]:
            channels.append_child("channel") \
                    .append_child_value("label", c) \
                    .append_child_value("unit", "angle") \
                    .append_child_value("type", "BVH")

        self.outlet = StreamOutlet(self.info)
        #self.buff = []
        #self.count = 0

        self.counter = 0.0


    def connect_ip(self):
        conn=False
        err=False
        while not conn:
            try:
                self.s.connect((self.TCP_IP, self.TCP_PORT))
            except:
                if not err:
                    print('connection not established - check adress, port and Axis Neuron streaming')
                    err=True
                time.sleep(5)
            else:
                conn=True
                print('connection established')

    def get_data(self):
        self.connect_ip()
        res = []
        data_full = True
        while 1:
            try:
                data_in = self.s.recv(self.BUFFER_SIZE) #Recieve a string of data from Axis Neuron
                if data_full: #If the previous string was full
                    if (data_in.decode("utf-8")).find("C") > 0: #If there is a sample beginning
                        index = (data_in.decode("utf-8")).find("C") #Find index for data beginning
                        index2 = (data_in.decode("utf-8")).find("|") #Find indef for data ending
                        if index2 > 0 & index2 > index: #If indexes are correct
                            res = data_in[index + 7:index2 - 2].decode("utf-8") #Store the data
                            res = res.split(" ") #Split the string
                            numbers = [float(i) for i in res] #Create an array with the recieved data
                            self.send_data(numbers) #send_data pushes the array into lsl
                        else: #If the recieved string doesn't contain the complete data sample
                            res = (data_in[index + 7:]).decode("utf-8") #Store the incomplete data
                            data_full = False #Flag that the data is incomplete
                else: #If previously didn't recieve a complete data sample
                    if (data_in.decode("utf-8")).find("C") > 0:
                        index = (data_in.decode("utf-8")).find("C") #Find indexes
                        index2 = (data_in.decode("utf-8")).find("|")
                        res1 = data_in[:index - 5].decode("utf-8") #Get the ending for the previous sample
                        res = res + res1 #Get a complete sample from two parts
                        res = res.split(" ")
                        numbers = [float(i) for i in res] #Create an array
                        self.send_data(numbers) #Send the array through lsl
                        if index2 > 0 & index2 > index: #If there is a complete sample
                            res = data_in[index + 7:index2 - 2].decode("utf-8")
                            res = res.split(" ")
                            numbers = [float(i) for i in res]
                            self.send_data(numbers)
                            data_full = True
                        else: #If there isn't
                            res = (data_in[(index + 7):]).decode("utf-8") #Store the beginning of a new sample
                    else: #If there is no sample beginning
                        index2 = (data_in.decode("utf-8")).find("|") #Find the ending
                        if index2 > 0: #If it is there
                            res1 = data_in[:index2 - 2].decode("utf-8")
                            res = res + res1
                            res = res.split(" ")
                            numbers = [float(i) for i in res]
                            self.send_data(numbers)
                            data_full = True
                        else:
                            data_full = True
            except Exception:
                print('connection aborted')
                self.connect_ip()
                
                    

    def send_data(self, numbers):
        joint = self.comboBox.currentIndex()
        print(numbers[237:240])

        self.graph_data_1.append({'x': self.t.elapsed(), 'y': numbers[joint * 6 + 3]})
        self.graph_data_2.append({'x': self.t.elapsed(), 'y': numbers[joint * 6 + 4]})
        self.graph_data_3.append({'x': self.t.elapsed(), 'y': numbers[joint * 6 + 5]})

        if len(self.graph_data_1) > 950:
            self.graph_data_1.popleft()
            self.graph_data_2.popleft()
            self.graph_data_3.popleft()

        #, numbers[joint * 6 + 4], numbers[joint * 6 + 5]
        
        #mysample = numbers[237:240]
        mysample = numbers[216:]

        #if self.count < 10:
        #    self.buff.append(mysample)
        #    self.count = self.count+1
        #else:
        #    self.outlet.push_chunk(self.buff)
        #    self.count = 0
        #    self.buff.clear()

        self.outlet.push_sample(mysample, self.counter/125)
        self.counter += 1
        #print(self.outlet.channel_count)
        #time.sleep(0.00833)


prog = Pn2lsl()
prog.get_data()

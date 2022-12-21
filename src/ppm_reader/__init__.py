import machine
import time


class PpmReader:
    def __init__(self,pin_id,channels,min_value=1000,max_value=2000,packet_gap=4000):
        self.channels=channels
        self.min_value=min_value
        self.max_value=max_value
        self.packet_gap=packet_gap
        self.pin = machine.Pin(pin_id, machine.Pin.IN)
        self.pin.irq(trigger=machine.Pin.IRQ_RISING,handler=self._irq_handler,hard=True)
        
        self.timer=time.ticks_us()
        self.last_valid_time=0
        self.valid_packets=0
        self.invalid_packets=0
        self.last_packet_length=0
        self.current_packet=[]
        self.current_channel=0
        self.last_valid_packet=[]
        
        for i in range(self.channels):
            self.current_packet.append(0)
            self.last_valid_packet.append(0)
        
    def _irq_handler(self,_p):
        now = time.ticks_us()
        delta = time.ticks_diff(now,self.timer)
        self.timer = now
        if delta > self.packet_gap:
            #end of a packet
            self.last_packet_length=self.current_channel
            #check packet length
            if self.last_packet_length == self.channels:
                #packet is good
                self.valid_packets+=1
                self.last_valid_packet=self.current_packet
                self.last_valid_time=now
            else:
                #something went wrong
                self.invalid_packets+=1
                
            #start new packet
            self.current_channel=0
        else:
            if self.current_channel < self.channels:
                #save time between pulses
                self.current_packet[self.current_channel]=delta
            self.current_channel+=1

    def time_since_last_packet(self):
        return time.ticks_diff(time.ticks_us(),self.last_valid_time)
    
    def get_valid_packets(self):
        return self.valid_packets

    def get_inalid_packets(self):
        return self.invalid_packets
    
    def reset_packet_counters(self):
        self.valid_packets=0
        self.invalid_packets=0

    def get_raw_value(self,channel):
        return self.last_valid_packet[channel]
    
    def get_raw_values(self):
        return self.last_valid_packet
    
    def get_values(self):
        values=[]
        for i in range(self.channels):
            values.append(self.get_value(i))
        return values
    
    def get_value(self,channel):
        return (self.last_valid_packet[channel]-self.min_value)/(self.max_value-self.min_value)

    def get_values_bi(self):
        values=[]
        for i in range(self.channels):
            values.append(self.get_value_bi(i))
        return values

    def get_value_bi(self,channel):
        return self.get_value_uni(channel)*2.0-1.0
    
    def guess_channel_count(self):
        return self.last_packet_length
## Description
A micropython library to decode PPM signals coming from a RC receiver (as used for rc planes and drones).

This library is focused on savety and includes functions that can be used to detect a faulty or lost signal.
**For this it is required to init the PpmReader class with the correct number of channels in the PPM signal. This might be a different number than the amount of servo connectors on the RC receiver hardware!**

Created for the use with pi pico, but should work on other boards as well.
You can find the [API documentation](https://github.com/redoxcode/micropython-ppm_reader/#API) and a few [examples](https://github.com/redoxcode/micropython-ppm_reader/#Examples) below.

## Examples

### Print the values of all channels
```Python
from ppm_reader import PpmReader
ppm_pin_id=28
ppm_channels=8
ppmReader=PpmReader(ppm_pin_id,ppm_channels)
while True:
    time.sleep(0.5)
    print(ppmReader.get_values())
```
### Find the number of channels
```Python
#the number of channels should be known before you init PpmReader
#if the channel number is incorrect only guess_channel_count will work
from ppm_reader import PpmReader
ppm_pin_id=28
ppmReader=PpmReader(ppm_pin_id,channels=0)
while True:
    time.sleep(0.5)
    print(ppmReader.guess_channel_count())
```
### Find values for min_value and max_value
```Python
#move the controls to the extreme positions and observe the values
from ppm_reader import PpmReader
ppm_pin_id=28
ppm_channels=8
ppmReader=PpmReader(ppm_pin_id,ppm_channels)
while True:
    time.sleep(0.5)
    print(ppmReader.get_raw_values())
```
### Check for a loss of signal
```Python
from ppm_reader import PpmReader
ppm_pin_id=28
ppm_channels=8
ppmReader=PpmReader(ppm_pin_id,ppm_channels)

#wait initial connection with the remote
while ppmReader.get_valid_packets() == 0:
    print("waiting for connection ...")
    time.sleep(0.5)
print("connected.")

#got signal, continue to main loop
while True:
    last_packet_time=ppmReader.time_since_last_packet()
    print(last_packet_time)
    if last_packet_time>25000: 
        #25ms without a new packet
        #take security measures here (for example stop all motors)
        print("connection lost")
        #wait for connection
        while ppmReader.time_since_last_packet()>25000:
            pass
        print("connected again")
    else:
        #connection ok. Do something here
        print(ppmReader.get_values())
```

## API
### class PpmReader(pin_id,channels,min_value=1000,max_value=2000,packet_gap=4000)
- pin_id: GPIO pin connected to the PPM signal comming from the RC receiver.
- channels: Number of channels in the PPM signal. if the channel count is wrong the packts will be considered invalid.       
- min_value: Minimum timeframe per channel in us (this should be around 1000us for standard equipment).
- max_value: Minimum timeframe per channel in us (this should be around 2000us for standard equipment).   
- packet_gap: Minimum time gap between packets in us (4000us should be used for standard equipment).

```time_since_last_packet()```
- returns the time passed since the last valid packet arrived in us. This will stay below about 5000us if every packet is received correctly. Missing 2 or 3 packets is usually not a problem.

```get_valid_packets()```
- returns the number of valid packets received

```get_inalid_packets()```
- returns the number of invalid packets received
    
```reset_packet_counters()```
- resets counters for valid and invalid packets received
    
```get_raw_values()```
- returns a list of all raw timeframes in us in the last valid packet received

```get_raw_value(channel)```
- returns the raw timeframe in us in the last valid packet received for a given channel
- channel: channel to get the value from

```get_values()```
- returns a list of all values in the last valid packet maped to a range of 0.0 to 1.0 (values are not clipped)

```get_value(channel)```
- the value for a given channel in the last valid packet maped to a range of 0.0 to 1.0 (values are not clipped)
- channel: channel to get the value from

```get_values_bi()```
- returns a list of all values in the last valid packet maped to a range of -1.0 to 1.0 (values are not clipped)

```get_value_bi(channel)```
- the value for a given channel in the last valid packet maped to a range of -1.0 to 1.0 (values are not clipped)
- channel: channel to get the value fro


```guess_channel_count()```
- returns the number of channels in the last packet (incase you are not sure how many channels your signal has)

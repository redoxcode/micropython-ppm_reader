# Description
A micropython library to decode PPM signals comming from a RC receiver (as used for rc planes and drones).

This library is focused on savety and includes functions that can be used to detect a faulty or lost signal.
**For this it is required to init the PpmReader class with the correct number of channels in the PPM signal. This might be a different number than the amount of servo connectors on the RC receiver hardware!**

Created for the use with pi pico, but should work on other boards as well.

# Api
```class PpmReader(pin_id,channels,min_value=1000,max_value=2000,packet_gap=4000)```
- pin_id: GPIO pin connected to the PPM signal comming from the RC receiver.
- channels: Number of channels in the PPM signal. if the channel count is wrong the packts will be considered invalid.       
- min_value: Minimum timeframe per channel in us (this should be around 1000us for standard equipment).
- max_value: Minimum timeframe per channel in us (this should be around 2000us for standard equipment).   
- packet_gap: Minimum time gap between packets in us (4000us should be used for standard equipment).

```PpmReader.time_since_last_packet()```
- returns the time passed since the last valid packet arrived in us

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

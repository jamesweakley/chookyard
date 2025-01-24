# chookyard

Pin layout

| L                        |    R                 |
| ---------------------    |    ----------------- |
| door switch button +  1  | 2  -                 |
| -                     3  | 4  motion sensor +   |
| -                     5  | 6  moton sensor gnd  |
| white LED +           7  | 8  -                 |
| red leds gnd          9  | 10 door switch signal|
| motion sensor signal  11 | 12 door latch signal |
| -                     13 | 14 white LED gnd     |
| -                     15 | 16 -                 |
| door latch +          17 | 18 red LED +         |
| -                     19 | 20 door latch ground |
| -                     21 | 22 -                 |
| -                     23 | 24 -                 |
| -                     25 | 26 door reed switch 1|
| -                     27 | 28 -                 |
| door opener control 1 29 | 30 door reed switch 2|
| door opener control 2 31 | 32 -                 |
| -                     33 | 34 -                 |
| -                     35 | 36 -                 |
| -                     37 | 38 -                 |
| -                     39 | 40 -                 |

![Pinout](https://www.raspberrypi.com/documentation/computers/images/GPIO-Pinout-Diagram-2.png)

# Systemd config
cp systemd_files/* /etc/systemd/system/
sudo systemctl enable door_opener
sudo systemctl enable streamlit

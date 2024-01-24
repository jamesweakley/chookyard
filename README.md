# chookyard

Pin layout

| L                     | R                 |
| --------------------- | ----------------- |
| door switch button +  | -                 |
| -                     | motion sensor +   |
| -                     | moton sensor gnd  |
| white LED +           | -                 |
| red leds gnd          | door switch signal|
| motion sensor signal  | -                 |
| -                     | white LED gnd     |
| -                     | -                 |
| -                     | -                 |
| -                     | -                 |
| -                     | door reed switch 1|
| -                     | -                 |
| door opener control 1 | door reed switch 2|
| door opener control 2 | -                 |
| -                     | -                 |
| -                     | -                 |
| -                     | -                 |
| -                     | -                 |


# Systemd config
cp systemd_files/* /etc/systemd/system/
sudo systemctl enable door_opener
sudo systemctl enable streamlit

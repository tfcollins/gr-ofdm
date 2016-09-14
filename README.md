# gr-ofdm
gnuradio OFDM blocks for over the air communications.  Tested with hardware (USRP's).

The purpose of this project is to provide multichannel OFDM reception with phase coherent receivers.  Working with only SIMO configurations now, but maybe will expand in the future.

Notes:
- Found issue with `digital_ofdm_frame_acquisition`: block really only works with manually created python, since it will always wrap input with parentheses.  Currently using a hier block hack workaround 

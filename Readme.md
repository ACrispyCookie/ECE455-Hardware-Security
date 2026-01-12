# SDR-Based DDR Air-Gap Data Exfiltration

By Nikas Ioannis Iason, Tsiantos Dimitrios and Tsogkas Panagiotis Nikolaos

### Project Structure

The project contains three main directories, helper scripts and dummy data to be transfered.

The `demodulators` folder contains all GNU Radio Companion `.grc` files used to demodulate the signal. The final and best implementation is `03_FIR.grc`, which was also used for the experiments. The files should open and run on GNU Radio Companion on the "attacker" device.

The `modulators` contain two implementations of the malware to be executed on the "target" device, the `pagefaulter.c` inspired by the ramear [Github repo](https://github.com/fyquah/ramear) and the `pagefaulter.c` implemented by ourselves. The first has better results for larger bitrate (8, 16 and 32 bps), so it was used for the metrics.


### Attacker setup

To setup the attacker device, download and install [GNU Radio Companion](https://wiki.gnuradio.org/index.php/InstallingGR). Then open the application using the `gnuradio-companion` command or the application icon in the menu. To run the demodulator, press Ctrl + O, select the `demodulators/03_FIR.grc` file and then click on the "Execute the Flowgraph" button on the top bar (play button). This will listen for any signals at the frequency specified. To stop the capture, click on the "X" icon on the opened window.

### Target setup

To setup the target device, transfer the `Makefile`, `ramear.c` and optionally the `pagefaulter.c`. Then navigate to the folder containing these files and run `make ramear` to make the ramear code. As the first argument you should pass the bitrate as a number and as the second the file you want to transmit. Example usage:

```bash
# Transmit the aes.key file contents at 16bps
./ramear 16 ../aes.key
```

### Helper scripts


#### print_message.py
On the attacker side, you can use the `print_message.py` which prints the message received from `/tmp/output.bin`, aligning the bits at the preamble, or prints in real time the characters received. Accepts up to 2 bit errors at the preamble.

### Compare key
Compares the `/tmp/output.bin` with the `aes.key`. Prints the wrong bits and their number.

### Shift bits
Shift the bits of the given file to the direction specified by the amount specified.

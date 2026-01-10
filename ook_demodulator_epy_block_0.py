import numpy as np
from gnuradio import gr
import pmt

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name='Byte to ASCII Message',
            in_sig=[np.uint8], # Receives packed bytes (0-255)
            out_sig=None       # No streaming output
        )
        # Register a message output port
        self.message_port_register_out(pmt.intern('out_msg'))

    def work(self, input_items, output_items):
        in0 = input_items[0]
        
        for s in in0:
            # Convert byte to ASCII character
            # We use try/except to handle non-ASCII noise gracefully
            try:
                char = chr(s)
                # Wrap the string in a PMT (Polymorphic Type) message
                msg = pmt.string_to_symbol(char)
                # Publish the message to the output port
                self.message_port_pub(pmt.intern('out_msg'), msg)
            except:
                pass 

        return len(in0)

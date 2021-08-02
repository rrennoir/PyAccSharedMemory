# PyAccSharedMemory

ACC shared memory reader written python 😀.

## Usage

```py
# Create a reader instance
asm = accSharedMemory()

# Start the reader process
asm.start() # Return false if failed

while (condition):
    # Receive most latest data available
    sm = asm.get_sm_data()

# Close reader process
asm.stop()
```

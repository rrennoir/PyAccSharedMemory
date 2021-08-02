# PyAccSharedMemory

ACC shared memory reader written in python 😀.

## Usage

Basic code example.

```py
# Create a reader instance
asm = accSharedMemory()

# Start the reader process
asm.start() # Return false if failed

while (condition):
    # Receive most latest data available
    sm = asm.get_sm_data() # Return a dict

# Close reader process
asm.stop()
```

## Data structure

Dictionary containing 3 dictionaries, each one of them contains all the information available through the shared memory and have the same as the official documentation.

```py
{
    "physics": {...},
    "graphics": {...},
    "statics": {...}
}
```

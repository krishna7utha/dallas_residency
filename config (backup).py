# Import the necessary gem5 components
from m5.objects import *
from m5.util import *

# Set up the system
system = System()

# Set up the clock domain (for system clock frequency)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'  # Set system clock frequency
system.clk_domain.voltage_domain = VoltageDomain(voltage='0.1V')

# Set up the memory mode and memory size
system.mem_mode = 'timing'  # Use a timing model for memory
system.mem_ranges = [AddrRange('512MB')]  # Define memory size (512MB in this case)

# Set up the CPU
system.cpu = TimingSimpleCPU()  # Use a simple in-order CPU model

# Set up the memory bus (connects CPU to memory)
system.membus = SystemXBar()

# Set up the memory controller (DDR3 in this case)
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()  # You can change this to other memory types like LPDDR3, etc.
system.mem_ctrl.dram.range = system.mem_ranges[0]  # Map the memory controller to the system memory range
system.mem_ctrl.port = system.membus.master  # Connect the memory controller to the bus

# Connect CPU to memory bus
system.cpu.icache_port = system.membus.slave  # Connect CPU instruction cache to the bus
system.cpu.dcache_port = system.membus.slave  # Connect CPU data cache to the bus

# Set up the interrupt controller (standard for simple CPU)
system.cpu.createInterruptController()

# Set up the system memory port (for direct memory access)
system.system_port = system.membus.slave

# Set up the binary to run (path to your RISC-V binary)
binary = "/home/krishna/Desktop/riscv-gnu-toolchain/riscv-binary"  # Replace with the actual path to your RISC-V binary
system.workload = SEWorkload.init_compatible(binary)
# Set up the process (RISC-V binary) that will be executed
process = Process()
process.cmd = [binary]  # Command to run (your RISC-V binary)
system.cpu.workload = process  # Set the binary as the workload for the CPU
system.cpu.createThreads()  # Create thread for the process

# Set up the simulation root object
root = Root(full_system=False, system=system)  # This is user mode (syscall emulation)

# Instantiate the system
m5.instantiate()

print("Starting RISC-V simulation!")

# Run the simulation for the maximum ticks (-1 runs indefinitely)
exit_event = m5.simulate()

# Print the reason for the simulation to end
print(f"Simulation ended: {exit_event.getCause()}")





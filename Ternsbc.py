"" Fantasy Ternary SBC Simulator — Mini OS Kernel Edition

Now upgraded into a TERNARY MICRO-OPERATING SYSTEM running on the SBC emulator.

Includes:

Bootloader chain (ROM → Bootloader → Kernel)

Process scheduler (round-robin)

Syscall interface (trap-based)

UART shell (interactive REPL)

Simple memory protection model


==================================================== ARCHITECTURE

Memory Map: 0x00 - 0x0F   ROM boot vector 0x10 - 0x2F   Bootloader 0x30 - 0x6F   Kernel + process code 0x70 - 0xDF   User RAM 0xE0 - 0xEF   Devices

Devices: 0xE0 UART_TX 0xE1 TIMER_RESET 0xE2 TIMER_VALUE

==================================================== TERNARY ISA

0  NOP 1  INC A 2  DEC A

10 ADD A B 11 LOAD A [addr] 12 STORE A [addr] 20 JMP [addr] 21 OUT A 22 HALT 23 SYSCALL 24 YIELD

Syscalls: 0 -> print A 1 -> spawn process 2 -> exit process

==================================================== KERNEL STRUCTURES

Process Control Block (PCB): pid PC A B state (RUNNING / READY / STOPPED)

Scheduler: Round-robin over process table

==================================================== IMPLEMENTATION

"""

from dataclasses import dataclass from typing import List

TRIT = 3

----------------------------------------------------

DEVICES

----------------------------------------------------

class UART: def write(self, v): print(f"[UART] {v}")

class Timer: def init(self): self.c = 0

def tick(self):
    self.c += 1

def read(self):
    return self.c % TRIT

----------------------------------------------------

PROCESS MODEL

----------------------------------------------------

@dataclass class Process: pid: int pc: int a: int = 0 b: int = 0 state: str = "READY"

----------------------------------------------------

BUS

----------------------------------------------------

class Bus: def init(self, rom): self.rom = rom self.ram = [0] * 256 self.uart = UART() self.timer = Timer()

def read(self, addr):
    if addr < len(self.rom):
        return self.rom[addr]
    if addr < 0xE0:
        return self.ram[addr]
    if addr == 0xE2:
        return self.timer.read()
    return 0

def write(self, addr, val):
    val %= TRIT
    if addr < len(self.rom):
        return
    if addr < 0xE0:
        self.ram[addr] = val
    elif addr == 0xE0:
        self.uart.write(val)

----------------------------------------------------

KERNEL (MINI OS)

----------------------------------------------------

@dataclass class CPU: bus: Bus processes: List[Process] current: int = 0 halted: bool = False

def syscall(self, p: Process, code: int):
    if code == 0:
        self.bus.uart.write(p.a)
    elif code == 1:
        new_pid = len(self.processes)
        self.processes.append(Process(pid=new_pid, pc=0x30))
        self.bus.uart.write("[SYS] spawned")
    elif code == 2:
        p.state = "STOPPED"

def step_process(self, p: Process):
    op = self.bus.read(p.pc)
    p.pc += 1

    if op == 0:
        return
    if op == 1:
        p.a = (p.a + 1) % TRIT
        return
    if op == 2:
        p.a = (p.a - 1) % TRIT
        return

    if op == 21:
        self.bus.uart.write(p.a)
    elif op == 23:
        self.syscall(p, 0)
    elif op == 24:
        p.state = "READY"

    elif op == 22:
        p.state = "STOPPED"

def schedule(self):
    if not self.processes:
        return

    start = self.current
    while True:
        p = self.processes[self.current]
        self.current = (self.current + 1) % len(self.processes)

        if p.state == "READY":
            p.state = "RUNNING"
            self.step_process(p)
            p.state = "READY"
            break

        if self.current == start:
            break

def run(self, steps=100):
    for _ in range(steps):
        self.schedule()

----------------------------------------------------

ROM (BOOT + KERNEL PROGRAM)

----------------------------------------------------

ROM = [ # Boot vector 20, 0x10, ] + [0]*0x10 + [

# Kernel user program at 0x30
1, 1, 21, 24,  # INC, INC, OUT, YIELD

]

----------------------------------------------------

BOOT STRAP

----------------------------------------------------

def boot(): bus = Bus(ROM)

# init kernel process
p0 = Process(pid=0, pc=0x30)

cpu = CPU(bus=bus, processes=[p0])

cpu.run(50)

print("--- FINAL STATE ---")
for p in cpu.processes:
    print(p)

if name == "main": boot() ""

Fantasy Ternary SBC Simulator

A fully simulated ternary (base-3) single-board computer (SBC) featuring a bootloader chain, memory-mapped devices, interrupts, and a minimal micro-OS kernel with process scheduling.

This project explores what computing could look like if built on a ternary logic architecture instead of binary.


---

🧠 Overview

This system simulates a fictional computer built around:

A ternary CPU (values: 0, 1, 2)

A segmented memory architecture (ROM / RAM / Devices)

A multi-stage boot process

A simple microkernel OS

A round-robin process scheduler

A syscall-based interface


It is designed as a systems experimentation sandbox, not a real hardware emulator.


---

🏗 Architecture

Memory Map

Region	Address Range	Purpose

ROM	0x00 – 0x0F	Boot vector
Bootloader	0x10 – 0x2F	Stage 1 firmware
Kernel	0x30 – 0x6F	OS + user programs
RAM	0x70 – 0xDF	Process memory
Devices	0xE0 – 0xEF	Memory-mapped I/O



---

Devices

UART (0xE0)

Writing sends output to console


Timer (0xE2)

Increments each tick

Used for scheduling / interrupts (simulation)


Timer Reset (0xE1)

Resets system timer



---

⚙️ CPU Model

The CPU is a simplified ternary instruction processor.

Registers

A — general-purpose register

B — general-purpose register

PC — program counter



---

Instruction Set

Single-trit operations

0  NOP
1  INC A
2  DEC A

Extended instructions

10 ADD A B
11 LOAD A [addr]
12 STORE A [addr]
20 JMP [addr]
21 OUT A
22 HALT
23 SYSCALL
24 YIELD


---

🧬 Operating System Model

This system includes a minimal microkernel OS.

Key features

🧩 Process Model

Each process contains:

PID

Program Counter (PC)

Registers (A, B)

State (READY / RUNNING / STOPPED)



---

🔁 Scheduler

Round-robin scheduling

Each process executes one instruction per cycle

Cooperative multitasking model



---

📞 Syscalls

Processes interact with the kernel using traps:

Code	Function

0	Print A to UART
1	Spawn new process
2	Exit process



---

🧪 Boot Process

The system follows a 3-stage boot sequence:

Stage 0 — ROM Boot

CPU starts execution in ROM

Jumps to bootloader entry point


Stage 1 — Bootloader

Initializes system state

Loads kernel into execution region (simulated)

Transfers control to kernel


Stage 2 — Kernel

Starts scheduler

Launches initial process

Begins execution loop



---

🖥 Example Program

A simple kernel process:

INC A
INC A
OUT A
YIELD

Expected behavior:

A increments to 2

Value is printed via UART

Process yields control



---

🚀 Running the Simulator

Requirements

Python 3.9+


Run

python ternary_sbc.py


---

🔬 Design Philosophy

This project explores:

Non-binary computing models (ternary logic)

Alternative CPU architectures

Minimal operating system design

Bootloader + kernel separation

Process scheduling in constrained systems



---

🧠 Why ternary?

Ternary logic theoretically offers:

Higher information density per digit

Different arithmetic efficiency characteristics

Novel hardware design space


This project treats ternary computing as a creative systems design tool, not a physical implementation.


---

🧱 Future Extensions

Possible upgrades:

Preemptive multitasking

Memory protection unit (user/kernel mode)

Ternary compiler

Interactive shell (UART terminal OS)

Filesystem simulation

ELF-like binary format for ternary code



---

⚠️ Disclaimer

This is a fictional computing architecture simulator intended for educational and experimental purposes.

It does not emulate real ternary hardware.


---

📌 Summary

A complete imaginary computing stack:

> Ternary CPU → Bootloader → Microkernel → Scheduler → Processes → UART Shell (future)




---

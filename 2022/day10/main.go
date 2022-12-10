package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"

	"github.com/pkg/profile"
)

var (
	inputFile = flag.String("f", "input.txt", "puzzle input file")
	profiling = flag.String("profile", "", "enable profiler, specify 'cpu' or 'mem'")
)

func panicOnErr(err error) {
	if err != nil {
		panic(err)
	}
}

type CPU struct {
	instructions     [][]string
	registersInitial map[string]int

	pc    int
	cycle int

	registers map[string]int

	pipeline struct {
		cyclesRemaining int
		register        string
		data            int
	}
}

func NewCPU(program string, registersInitial map[string]int) *CPU {
	cpu := &CPU{
		instructions:     [][]string{},
		registersInitial: map[string]int{},
	}

	for _, instr := range strings.Split(strings.TrimSpace(program), "\n") {
		cpu.instructions = append(cpu.instructions, strings.Split(instr, " "))
	}

	for reg, val := range registersInitial {
		cpu.registersInitial[reg] = val
	}

	cpu.Reset()

	return cpu
}

func (c *CPU) Reset() {
	c.pc = 0
	c.cycle = 1

	c.registers = map[string]int{}
	for reg, val := range c.registersInitial {
		c.registers[reg] = val
	}
}

func (c *CPU) Run(cycleEvalFn func(int, map[string]int)) {
	for c.pc < len(c.instructions) || c.pipeline.cyclesRemaining > 0 {
		cycleEvalFn(c.cycle, c.registers)

		c.pipeline.cyclesRemaining -= 1

		if c.pipeline.cyclesRemaining == 0 {
			c.registers[c.pipeline.register] += c.pipeline.data
		} else {
			switch c.instructions[c.pc][0] {
			case "addx":
				num, err := strconv.Atoi(c.instructions[c.pc][1])
				panicOnErr(err)

				c.pipeline.register = "x"
				c.pipeline.cyclesRemaining = 1
				c.pipeline.data = num
			}

			c.pc += 1
		}

		c.cycle += 1
	}
}

func solve(input *os.File) (int, string) {
	s1 := 0
	s2 := ""

	inputBytes, err := ioutil.ReadAll(input)
	panicOnErr(err)

	cpu := NewCPU(
		string(inputBytes),
		map[string]int{"x": 1},
	)

	cpu.Run(func(cycle int, registers map[string]int) {
		// Part 2
		xPos := (cycle - 1) % 40

		if xPos == 0 {
			s2 += "\n"
		}

		if registers["x"]-1 <= xPos && xPos <= registers["x"]+1 {
			s2 += "█"
		} else {
			s2 += " "
		}

		// Part 1
		if cycle == 20 || (cycle-20)%40 == 0 {
			s1 += registers["x"] * cycle
		}

	})

	return s1, s2
}

func main() {
	flag.Parse()

	// Profiler
	switch *profiling {
	case "cpu":
		defer profile.Start(profile.CPUProfile, profile.ProfilePath(".")).Stop()
	case "mem":
		defer profile.Start(profile.MemProfile, profile.ProfilePath(".")).Stop()
	}

	// Open file
	file, err := os.Open(*inputFile)
	panicOnErr(err)
	defer file.Close()

	// Solve
	s1, s2 := solve(file)
	fmt.Printf("Star 1: %v\n", s1)
	fmt.Printf("Star 2: %v\n", s2)
}

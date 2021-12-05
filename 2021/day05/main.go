package main

import (
	"flag"
	"fmt"
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

type Point struct {
	x int
	y int
}

func (p *Point) Add(other Point) Point {
	return Point{p.x + other.x, p.y + other.y}
}

type Line struct {
	from Point
	to   Point
}

func (l *Line) Direction() Point {
	dir := Point{0, 0}

	if l.from.x < l.to.x {
		dir.x = 1
	} else if l.from.x > l.to.x {
		dir.x = -1
	}

	if l.from.y < l.to.y {
		dir.y = 1
	} else if l.from.y > l.to.y {
		dir.y = -1
	}

	return dir
}

func (l *Line) Points() []Point {
	points := []Point{l.from}

	dir := l.Direction()
	next := l.from
	for next != l.to {
		next = next.Add(dir)
		points = append(points, next)
	}

	return points
}

func solve(lines []Line, diagonals bool) int {
	seenPoints := map[Point]int{}

	for _, line := range lines {
		direction := line.Direction()

		// Ignore diagonal lines
		if !diagonals && direction.x != 0 && direction.y != 0 {
			continue
		}

		// Generate all points between the from and to points of the line
		for _, point := range line.Points() {
			seenPoints[point]++
		}
	}

	// Count the overlapping points (that have been seen more than once)
	overlaped := 0
	for _, c := range seenPoints {
		if c > 1 {
			overlaped++
		}
	}

	return overlaped
}

func parsePoint(point string) Point {
	coords := strings.Split(point, ",")

	x, err := strconv.Atoi(coords[0])
	panicOnErr(err)
	y, err := strconv.Atoi(coords[1])
	panicOnErr(err)

	return Point{x, y}
}

func parseLines(input string) []Line {
	lines := []Line{}

	for _, l := range strings.Split(strings.TrimSpace(input), "\n") {
		points := strings.Split(l, " -> ")

		lines = append(lines, Line{parsePoint(points[0]), parsePoint(points[1])})
	}

	return lines
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

	// Read file
	input, err := os.ReadFile(*inputFile)
	panicOnErr(err)

	// Parse input
	lines := parseLines(string(input))

	// Solve
	fmt.Printf("Star 1: %d\n", solve(lines, false))
	fmt.Printf("Star 2: %d\n", solve(lines, true))
}

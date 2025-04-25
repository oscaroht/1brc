package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"runtime"
	"strconv"
	"strings"
	"time"
)

func chuck(offset int64, channel chan map[string][4]int) {
	fmt.Println("func s")
	file, err := os.Open("./measurements.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	fmt.Println("Put cursor at offset: ", offset)
	file.Seek(offset, 0)

	city_map := make(map[string][4]int)

	fmt.Println("Create new scanner")
	scanner := bufio.NewScanner(file)
	// optionally, resize scanner's capacity for lines over 64K, see next example
	line := ""
	total := 0
	cnt := 0
	for scanner.Scan() {
		line = scanner.Text()
		splts := strings.Split(line, ";")
		if len(splts) != 2 {
			continue
		}
		city := splts[0]
		// fmt.Println(city)
		temp_str := splts[1]
		tmp := temp_str[:len(temp_str)-2] + string(temp_str[len(temp_str)-1])
		tmp_int, err := strconv.Atoi(tmp)
		if err != nil {
			log.Fatal(err)
		}
		val, ok := city_map[city]
		// If the key exists
		if !ok {
			city_map[city] = [4]int{0, 0, 0, 0}
		}
		minimum := min(val[0], tmp_int)
		total += tmp_int
		cnt += 1
		maximum := max(val[2], tmp_int)
		city_map[city] = [4]int{minimum, total, cnt, maximum}
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	channel <- city_map
}

func main() {
	start := time.Now()

	fi, err := os.Stat("./small_measurements.txt")
	if err != nil {
		log.Fatal(err)
	}
	// get the size
	size := fi.Size()
	fmt.Println("File size: ", size)
	chunks_amount := runtime.NumCPU()
	fmt.Printf("Running with %v cores", chunks_amount)
	chunk_size := size / int64(chunks_amount)
	channel := make(chan map[string][4]int)
	for i := 0; i < chunks_amount; i++ {
		fmt.Printf("start routine: %v with offset %v\n", i, i*int(chunk_size))
		go chuck(int64(i)*chunk_size, channel)
	}
	for i := range channel {
		fmt.Println(i)
	}

	elapsed := time.Now().Sub(start)
	fmt.Println("Time elapsed: ", elapsed)
}

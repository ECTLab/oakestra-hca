package main

import (
        "fmt"
        "log"
        "math"
        "net/http"
        "time"
)

func isPrime(n int) bool {
        if n < 2 {
                return false
        }
        for i := 2; i <= int(math.Sqrt(float64(n))); i++ {
                if n%i == 0 {
                        return false
                }
        }
        return true
}

func findNextNPrimes(start, count int) []int {
        primes := []int{}
        num := start
        for len(primes) < count {
                if isPrime(num) {
                        primes = append(primes, num)
                }
                num++
        }
        return primes
}

func simulateHighCPU() {
        _ = findNextNPrimes(1, 150000)
        fmt.Println("Finished CPU-intensive task.")
}

func highCPUHandler(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        simulateHighCPU()
        duration := time.Since(start)
        w.WriteHeader(http.StatusOK)
        fmt.Fprintf(w, "High CPU task completed in %s", duration)
}

func main() {
        http.HandleFunc("/", highCPUHandler)

        port := 80
        log.Printf("Starting server on :%d", port)
        log.Fatal(http.ListenAndServe(fmt.Sprintf(":%d", port), nil))
}
package main

import (
        "fmt"
        "net/http"
)

func main() {
        fmt.Println("starting server on port 80")
        http.HandleFunc("/", hello)
        http.HandleFunc("ok", ok)
        http.ListenAndServe(":80", nil)
}

func hello(w http.ResponseWriter, r *http.Request) {
        msg := "hello from app!"

        cnt := 1000000

        for i := 0; i < cnt; i++ {
                fmt.Println(i)
        }

        fmt.Println(msg)
        w.WriteHeader(http.StatusOK)
        w.Write([]byte(string(msg)))
}

func ok(w http.ResponseWriter, r *http.Request) {
        msg := "ok!"

        fmt.Println(msg)

        w.WriteHeader(http.StatusOK)
        w.Write([]byte(string(msg)))
}

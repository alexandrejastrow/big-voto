package main

import (
	"fmt"
	"net/http"
)

func hello(w http.ResponseWriter, req *http.Request) {
	fmt.Fprintf(w, "Hello, %s!", req.URL.Path[1:])
}
func main() {
	http.HandleFunc("/", hello)
	http.ListenAndServe(":8050", nil)
}

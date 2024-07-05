package main

import (
	"embed"
	"flag"
	"fmt"
	"io/fs"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"strings"
)

//go:embed frontend
var cryofront embed.FS

// Returns the embedded static files
func handler() http.Handler {
	stripped, err := fs.Sub(cryofront, "frontend")
	if err != nil {
		log.Fatalln(err)
	}
	return http.FileServer(http.FS(stripped))
}

// Middleware to add logger that prints to stdout
func addLogger(h http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("%s %s", r.Method, r.URL.Path)
		h.ServeHTTP(w, r)
	})
}

func NewProxy(targetHost string) (*httputil.ReverseProxy, error) {
	url, err := url.Parse(targetHost)
	if err != nil {
		return nil, err
	}
	return httputil.NewSingleHostReverseProxy(url), nil
}

func ProxyRequestHandler(proxy *httputil.ReverseProxy) func(http.ResponseWriter, *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		// Trim '/api' from incoming request so it could reach the backend
		apiPath := strings.TrimPrefix(r.URL.Path, "/api")
		log.Printf("%s [Cryo] %s", r.Method, apiPath)
		r.URL.Path = apiPath

		proxy.ServeHTTP(w, r)
	}
}

func main() {
	port := flag.Int("port", 9091, "Port to serve Cryonogen Frontend.")
	backend := flag.String("backend", "http://localhost:5000", "Url to the Cryo JSON REST API backend.")
	flag.Parse()

	mux := http.NewServeMux()
	mux.Handle("/", addLogger(handler()))

	proxy, err := NewProxy(*backend)
	if err != nil {
		panic(err)
	}

	mux.HandleFunc("/api/", ProxyRequestHandler(proxy))

	log.Printf("Listening at :%d\n", *port)
	http.ListenAndServe(fmt.Sprintf(":%d", *port), mux)
}

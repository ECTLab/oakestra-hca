package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
)

type RequestBody struct {
	ScaleType string `json:"scale_type"`
	ServiceID string `json:"service_id"`
	ClusterID string `json:"cluster_id,omitempty"`
}

type HCARequestBody struct {
	CPUThreshold int `json:"cpu_threshold"`
	RAMThreshold int `json:"ram_threshold"`
	MaxReplicas  int `json:"max_replicas"`
	MinReplicas  int `json:"min_replicas"`
}

func makeRequest(serviceID string) {
	address := os.Getenv("API_URL")
	if address == "" {
		address = "http://46.249.99.42:10080"
	}
	url := fmt.Sprintf("%s/api/v1/hca/manual", address)
	data := RequestBody{
		ScaleType: "up",
		ServiceID: serviceID,
		// ClusterID: "67dda17adea7a1ce9586ad94",
	}

	jsonData, err := json.Marshal(data)
	if err != nil {
		fmt.Println("Error marshalling JSON:", err)
		return
	}

	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error making request:", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		fmt.Println("Manual scale request failed with status code:", resp.StatusCode)
		return
	}

	_, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading response:", err)
		return
	}

	fmt.Println("Test execution was successful")
}

func runHCACommands(serviceID string) {
	baseURL := os.Getenv("API_URL")
	if baseURL == "" {
		baseURL = "http://46.249.99.42:10080"
	}

	postURL := fmt.Sprintf("%s/api/v1/hca/%s", baseURL, serviceID)
	getURL := fmt.Sprintf("%s/api/v1/hca/%s", baseURL, serviceID)

	data := HCARequestBody{
		CPUThreshold: 1,
		RAMThreshold: 40,
		MaxReplicas:  4,
		MinReplicas:  1,
	}

	jsonData, err := json.Marshal(data)
	if err != nil {
		fmt.Println("Error marshalling JSON:", err)
		return
	}

	req, err := http.NewRequest("POST", postURL, bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Println("Error creating request:", err)
		return
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error making POST request:", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != 201 {
		fmt.Println("HCA POST request failed with status code:", resp.StatusCode)
		return
	}

	fmt.Println("HCA POST request sent successfully")

	req, err = http.NewRequest("GET", getURL, nil)
	if err != nil {
		fmt.Println("Error creating GET request:", err)
		return
	}

	resp, err = client.Do(req)
	if err != nil {
		fmt.Println("Error making GET request:", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		fmt.Println("HCA GET request failed with status code:", resp.StatusCode)
		return
	}

	_, err = ioutil.ReadAll(resp.Body)
	if err != nil {
		fmt.Println("Error reading GET response:", err)
		return
	}

	fmt.Println("Test execution was successful")
}

func main() {
	if len(os.Args) < 3 {
		fmt.Println("Usage: ./program [manual|hca] <serviceID>")
		return
	}

	command := os.Args[1]
	serviceID := os.Args[2]

	if command == "manual" {
		makeRequest(serviceID)
	} else if command == "hca" {
		runHCACommands(serviceID)
	} else {
		fmt.Println("Unknown command")
	}
}

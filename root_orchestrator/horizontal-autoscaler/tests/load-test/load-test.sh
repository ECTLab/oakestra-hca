#!/bin/bash

# Arguments for load test, spike test, and stress test
test_type=$1  # "load", "spike", or "stress"
num_requests=$2
parallel_jobs=$3  # Adjust based on system capacity
duration=$4  # Duration in seconds for load or spike tests

# Temporary files for safe concurrent updates
success_file=$(mktemp)
failure_file=$(mktemp)
time_file=$(mktemp)

# Ensure cleanup of temp files
trap "rm -f $success_file $failure_file $time_file" EXIT

# Function to perform the HTTP request
run_request() {
  start_time=$(date +%s%N)  # Start time in nanoseconds
  response=$(sudo ip netns exec test.test.nginx.nginx.instance.0 curl -s -o /dev/null -w "%{http_code}" http://10.30.0.4:80/)
  end_time=$(date +%s%N)  # End time in nanoseconds

  duration=$(( (end_time - start_time) / 1000000 ))  # Convert to milliseconds
  echo "$duration" >> "$time_file"

  if [[ "$response" == "200" ]]; then
    echo 1 >> "$success_file"
  else
    echo 1 >> "$failure_file"
  fi

  echo "Request took: ${duration} ms, Response code: ${response}"
}

# Function for load test
load_test() {
  for ((i = 1; i <= num_requests; i++)); do
    run_request &

    # Limit the number of parallel jobs
    if (( i % parallel_jobs == 0 )); then
      wait
    fi
  done
}

# Function for spike test
spike_test() {
  # Initial low load
  for ((i = 1; i <= num_requests / 2; i++)); do
    run_request &

    # Limit the number of parallel jobs
    if (( i % parallel_jobs == 0 )); then
      wait
    fi
  done

  # Sudden spike
  for ((i = 1; i <= num_requests / 2; i++)); do
    run_request &

    # Limit the number of parallel jobs
    if (( i % parallel_jobs == 0 )); then
      wait
    fi
  done
}

# Function for stress test
stress_test() {
  for ((i = 1; i <= num_requests; i++)); do
    run_request &

    # Limit the number of parallel jobs
    if (( i % parallel_jobs == 0 )); then
      wait
    fi
  done
}

# Execute the test based on the test type
case $test_type in
  load)
    echo "Starting load test for $duration seconds..."
    load_test
    ;;
  spike)
    echo "Starting spike test..."
    spike_test
    ;;
  stress)
    echo "Starting stress test..."
    stress_test
    ;;
  *)
    echo "Unknown test type: $test_type. Please use 'load', 'spike', or 'stress'."
    exit 1
    ;;
esac

wait  # Ensure all background jobs finish before exiting

# Aggregate results
total_time=$(awk '{sum+=$1} END {print sum}' "$time_file")
success_count=$(wc -l < "$success_file")
failure_count=$(wc -l < "$failure_file")
avg_time=$((total_time / num_requests))

# Display statistics
echo "All requests completed."
echo "Total Requests: $num_requests"
echo "Successful Requests: $success_count"
echo "Failed Requests: $failure_count"
echo "Average Response Time: ${avg_time} ms"


#!/bin/bash

num_requests=$1
parallel_jobs=$2  # Adjust based on system capacity

# Temporary files for safe concurrent updates
success_file=$(mktemp)
failure_file=$(mktemp)
time_file=$(mktemp)

# Ensure cleanup of temp files
trap "rm -f $success_file $failure_file $time_file" EXIT

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

for ((i = 1; i <= num_requests; i++)); do
  run_request &

  # Limit the number of parallel jobs
  if (( i % parallel_jobs == 0 )); then
    wait
  fi
done

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

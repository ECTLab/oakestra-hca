#!/bin/bash

num_requests=100
parallel_jobs=50  # Adjust this number based on system capacity

run_request() {
  sudo ip netns exec test.test.nginx.nginx.instance.0 curl -s http://10.30.0.1:80/ > /dev/null
  echo "curl done"
}

for ((i = 1; i <= num_requests; i++)); do
  run_request &

  # Limit the number of parallel jobs
  if (( i % parallel_jobs == 0 )); then
    wait
  fi

done

wait  # Ensure all background jobs finish before exiting
echo "All requests completed."
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  vus: 10, // Number of virtual users
  iterations: 80, // Total number of requests
};

export default function () {
  let res = http.get('http://127.0.0.1:8888/');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}

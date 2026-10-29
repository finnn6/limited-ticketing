import http from "k6/http";
import { check } from "k6";

export const options = {
  scenarios: {
    issue: {
      executor: "shared-iterations",
      vus: 100,          // 동시 사용자 100명
      iterations: 1000,  // 총 요청 1000건
      maxDuration: "30s",
    },
  },
};

const EVENT_ID = __ENV.EVENT_ID || 1;

export default function () {
  const userId = `user-${__VU}-${__ITER}`; // 요청마다 다른 사용자
  const res = http.post(
    `http://localhost:8000/events/${EVENT_ID}/issue`,
    JSON.stringify({ user_id: userId }),
    { headers: { "Content-Type": "application/json" } },
  );
  check(res, { "201 or 409": (r) => r.status === 201 || r.status === 409 });
}
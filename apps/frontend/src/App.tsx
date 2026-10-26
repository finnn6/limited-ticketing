import { useState } from "react";

type Result = "idle" | "success" | "duplicate" | "soldout";

const messages: Record<Result, string> = {
  idle: "",
  success: "발급 완료!",
  duplicate: "이미 발급받은 사용자입니다.",
  soldout: "마감되었습니다.",
};

export default function App() {
  const total = 1;
  const [remaining, setRemaining] = useState(1);
  const [userId, setUserId] = useState("");
  const [issued, setIssued] = useState<string[]>([]);
  const [result, setResult] = useState<Result>("idle");

  // 임시 로직: 나중에 POST /events/{id}/issue 호출로 교체
  const handleIssue = () => {
    if (!userId) return;
    if (remaining <= 0) return setResult("soldout");
    if (issued.includes(userId)) return setResult("duplicate");
    setIssued([...issued, userId]);
    setRemaining(remaining - 1);
    setResult("success");
  };

  return (
    <main style={{ maxWidth: 360, margin: "80px auto", fontFamily: "sans-serif" }}>
      <h1>선착순 할인권</h1>
      <p>남은 수량: {remaining} / {total}</p>
      <input
        placeholder="사용자 ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
      />
      <button onClick={handleIssue} disabled={remaining <= 0}>
        발급 신청하기
      </button>
      <p>{messages[result]}</p>
    </main>
  );
}
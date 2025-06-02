
import { useEffect, useState } from 'react';
import Timetable from './components/Timetable';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('https://band-matcher.onrender.com', {
      method: 'POST'
    })
      .then(res => res.json())
      .then(json => setData(json))
      .catch(err => alert("에러 발생: " + err));
  }, []);

  if (!data) return <div>불러오는 중...</div>;

  return (
    <div>
      <h1>자동 스케줄링 시간표</h1>
      <Timetable rooms={data.rooms} schedule={data.schedule} />
    </div>
  );
}

export default App;

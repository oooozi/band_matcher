
import React from 'react';

function Timetable({ rooms, schedule }) {
  const allTimes = Object.keys(schedule).sort();
  const times = [...new Set(allTimes.map(t => t.split(" ")[1]))].sort();
  const dates = [...new Set(allTimes.map(t => t.split(" ")[0]))].sort();

  const handleClick = (time, roomIdx) => {
    const entries = schedule[time];
    const songObj = entries[roomIdx];
    const song = Object.keys(songObj)[0];
    const [participants, absentees] = songObj[song];
    alert(`곡명: ${song}\n\n참여자: ${participants.join(', ')}\n불참자: ${absentees.join(', ')}`);
  };

  return (
    <table>
      <thead>
        <tr>
          <th rowSpan="2">시간</th>
          {dates.map(date => (
            <th key={date} colSpan={rooms}>{date}</th>
          ))}
        </tr>
        <tr>
          {dates.map(date =>
            Array.from({ length: rooms }, (_, i) => (
              <th key={`${date}-room-${i}`}>합주실{i + 1}</th>
            ))
          )}
        </tr>
      </thead>
      <tbody>
        {times.map(time => (
          <tr key={time}>
            <td>{time}</td>
            {dates.map(date => {
              const key = `${date} ${time}`;
              const roomEntries = schedule[key] || [];
              return Array.from({ length: rooms }, (_, i) => {
                const cell = roomEntries[i];
                if (cell) {
                  const song = Object.keys(cell)[0];
                  const [participants, absentees] = cell[song];
                  return (
                    <td key={`${key}-room-${i}`} onClick={() => handleClick(key, i)}>
                      {song} ({participants.length}/{participants.length + absentees.length})
                    </td>
                  );
                } else {
                  return <td key={`${key}-room-${i}`}>-</td>;
                }
              });
            })}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default Timetable;

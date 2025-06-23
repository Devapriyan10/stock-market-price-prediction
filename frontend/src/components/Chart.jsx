import { Line } from 'react-chartjs-2';

export default function Chart({ data }) {
  const labels = data.map(d => d.ds);
  const vals = data.map(d => d.y);
  return <Line data={{ labels, datasets: [{ label: 'Close', data: vals }] }} />;
}

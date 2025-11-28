"use client";

import { useEffect, useRef } from "react";
import { Chart, registerables, type ChartOptions } from "chart.js";

Chart.register(...registerables);

type StackedBarProps = {
  labels: string[];
  data: { label: string; values: number[]; color: string }[];
  height?: number | string;
};

export default function StackedBar({ labels, data, height = 200 }: StackedBarProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const chartRef = useRef<Chart | null>(null);

  useEffect(() => {
    if (!canvasRef.current) return;
    if (chartRef.current) chartRef.current.destroy();

    const options: ChartOptions<"bar"> = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { stacked: true, grid: { display: false } },
        y: { stacked: true, beginAtZero: true, grid: { color: "rgba(15,23,42,0.06)" }, suggestedMax: 10 }
      },
      plugins: {
        legend: { display: true, position: "bottom", labels: { boxWidth: 12, boxHeight: 12 } },
        tooltip: {
          mode: "index",
          intersect: false,
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${ctx.formattedValue}`
          }
        }
      }
    };

    const datasets = data.map((d) => ({
      label: d.label,
      data: d.values,
      backgroundColor: d.color,
      borderColor: d.color,
      borderWidth: 1,
      barPercentage: 0.65,
      categoryPercentage: 0.6
    }));

    chartRef.current = new Chart(canvasRef.current, {
      type: "bar",
      data: { labels, datasets },
      options
    });

    return () => chartRef.current?.destroy();
  }, [labels, data]);

  return <canvas ref={canvasRef} style={{ width: "100%", height }} />;
}

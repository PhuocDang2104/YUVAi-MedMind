"use client";

import { useEffect, useRef } from "react";
import { Chart, registerables, type ChartOptions } from "chart.js";

Chart.register(...registerables);

type BarChartProps = {
  labels: string[];
  data: number[];
  color?: string;
  height?: number | string;
  title?: string;
};

export default function BarChart({ labels, data, color = "#2563eb", height = "210px", title }: BarChartProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const chartRef = useRef<Chart | null>(null);

  useEffect(() => {
    if (!canvasRef.current) return;
    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const options: ChartOptions<"bar"> = {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: { mode: "index", intersect: false },
        title: title ? { display: true, text: title } : undefined
      },
      scales: {
        y: { beginAtZero: true, ticks: { precision: 0 } }
      }
    };

    chartRef.current = new Chart(canvasRef.current, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: title || "Value",
            data,
            backgroundColor: `${color}99`,
            borderColor: color,
            borderWidth: 1.5,
            borderRadius: 8,
            maxBarThickness: 28
          }
        ]
      },
      options
    });

    return () => {
      chartRef.current?.destroy();
    };
  }, [labels, data, color, title]);

  return <canvas ref={canvasRef} style={{ width: "100%", height }} />;
}

"use client";

import { useEffect, useRef } from "react";
import { Chart, registerables, type ChartOptions, type TooltipItem } from "chart.js";

Chart.register(...registerables);

type LineChartProps = {
  labels: string[];
  series: { label: string; data: number[]; color?: string; type?: "line" | "scatter"; yAxisID?: "y" | "y1" }[];
  markers?: { x: string; label: string; y?: number }[];
  height?: number | string;
  showFill?: boolean;
};

export default function LineChart({ labels, series, markers, height = "220px", showFill = true }: LineChartProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const chartRef = useRef<Chart | null>(null);

  useEffect(() => {
    if (!canvasRef.current) return;
    if (chartRef.current) {
      chartRef.current.destroy();
    }

    const ctx = canvasRef.current.getContext("2d");
    const baseSeriesForMarkers = series.find((s) => (s.type || "line") !== "scatter") || series[0];
    const markerPoints =
      markers && markers.length
        ? markers
            .map((m) => {
              const idx = labels.indexOf(m.x);
              const yValue = m.y ?? (idx >= 0 && baseSeriesForMarkers ? baseSeriesForMarkers.data[idx] : undefined);
              if (yValue === undefined || yValue === null) return null;
              return { x: m.x, y: yValue, alertLabel: m.label };
            })
            .filter(Boolean) as { x: string; y: number; alertLabel: string }[]
        : [];

    const options: ChartOptions<"line" | "scatter"> = {
      responsive: true,
      interaction: { mode: "nearest", intersect: false },
      layout: { padding: { top: 8, right: 8, bottom: 6, left: 4 } },
      scales: {
        y: { beginAtZero: true, position: "left", suggestedMax: 100, grid: { color: "rgba(15,23,42,0.06)" } },
        ...(series.some((s) => s.yAxisID === "y1")
          ? { y1: { beginAtZero: true, position: "right", grid: { drawOnChartArea: false }, ticks: { precision: 0 } } }
          : {})
      },
      plugins: {
        legend: { display: true, position: "bottom", labels: { boxWidth: 12, boxHeight: 12, usePointStyle: true } },
        tooltip: {
          mode: "nearest",
          intersect: false,
          callbacks: {
            label: (ctx: TooltipItem<"line" | "scatter">) => {
              const raw: any = ctx.raw;
              if (ctx.dataset.type === "scatter" && raw?.alertLabel) {
                return raw.alertLabel;
              }
              const label = ctx.dataset.label || "Value";
              return `${label}: ${ctx.formattedValue}`;
            }
          }
        }
      }
    };

    const datasets = series.map((s) => {
      const color = s.color || "#2563eb";
      let backgroundColor: string | CanvasGradient = "rgba(37,99,235,0.15)";
      if (ctx && showFill && s.type !== "scatter") {
        const gradient = ctx.createLinearGradient(0, 0, 0, canvasRef.current!.height);
        gradient.addColorStop(0, `${color}33`);
        gradient.addColorStop(1, `${color}05`);
        backgroundColor = gradient;
      } else if (!showFill) {
        backgroundColor = "transparent";
      }
      return {
        label: s.label,
        data: s.data,
        type: s.type || "line",
        borderColor: color,
        backgroundColor,
        borderWidth: 2,
        fill: showFill && s.type !== "scatter",
        tension: 0.35,
        pointRadius: 3.5,
        yAxisID: s.yAxisID || "y",
        showLine: s.type === "scatter" ? false : true,
        pointHoverRadius: 5
      };
    });

    if (markerPoints.length) {
      datasets.push({
        label: "Alerts",
        type: "scatter",
        data: markerPoints,
        parsing: { xAxisKey: "x", yAxisKey: "y" },
        showLine: false,
        borderColor: "#ef4444",
        backgroundColor: "#ef4444",
        pointRadius: 5,
        pointHoverRadius: 7,
        pointBorderWidth: 2,
        pointBackgroundColor: "#ef4444",
        pointBorderColor: "#fff",
        yAxisID: "y"
      } as any);
    }

    chartRef.current = new Chart(canvasRef.current, {
      type: "line",
      data: { labels, datasets },
      options
    });
    return () => {
      chartRef.current?.destroy();
    };
  }, [labels, markers, series, showFill]);

  return <canvas ref={canvasRef} style={{ width: "100%", height }} />;
}

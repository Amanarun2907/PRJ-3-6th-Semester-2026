import React from 'react';
import Plot from 'react-plotly.js';

const BASE_LAYOUT = {
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor:  'rgba(0,0,0,0)',
  font: { color: '#c9d1d9', family: 'Inter, sans-serif', size: 12 },
  xaxis: {
    gridcolor: 'rgba(33,38,45,0.8)',
    zerolinecolor: '#30363d',
    tickfont: { color: '#8b949e', size: 11 },
    linecolor: '#21262d',
  },
  yaxis: {
    gridcolor: 'rgba(33,38,45,0.8)',
    zerolinecolor: '#30363d',
    tickfont: { color: '#8b949e', size: 11 },
    linecolor: '#21262d',
  },
  legend: {
    bgcolor: 'rgba(17,24,39,0.8)',
    bordercolor: '#21262d',
    borderwidth: 1,
    font: { color: '#c9d1d9', size: 11 },
  },
  margin: { l: 55, r: 20, t: 45, b: 45 },
  hoverlabel: {
    bgcolor: '#111827',
    bordercolor: '#00d4ff',
    font: { color: '#f0f6fc', size: 12 },
  },
  hovermode: 'x unified',
  title: { font: { color: '#8b949e', size: 13 }, x: 0.01 },
};

export default function PlotlyChart({ data, layout = {}, style = {}, config = {} }) {
  const mergedLayout = {
    ...BASE_LAYOUT,
    ...layout,
    xaxis: { ...BASE_LAYOUT.xaxis, ...(layout.xaxis || {}) },
    yaxis: { ...BASE_LAYOUT.yaxis, ...(layout.yaxis || {}) },
    legend: { ...BASE_LAYOUT.legend, ...(layout.legend || {}) },
    margin: { ...BASE_LAYOUT.margin, ...(layout.margin || {}) },
    hoverlabel: { ...BASE_LAYOUT.hoverlabel, ...(layout.hoverlabel || {}) },
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor:  'rgba(0,0,0,0)',
  };

  return (
    <Plot
      data={data}
      layout={mergedLayout}
      config={{
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d','select2d','lasso2d','resetScale2d','toImage'],
        displaylogo: false,
        responsive: true,
        ...config,
      }}
      style={{ width: '100%', ...style }}
      useResizeHandler
    />
  );
}

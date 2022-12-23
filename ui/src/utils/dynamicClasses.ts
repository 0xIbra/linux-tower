export const metricTextColorClass = (metricValue: Number) => {
  if (metricValue >= 80) {
    return "text-color-danger";
  }
  if (metricValue > 50) {
    return "text-color-warning";
  }

  return "text-color-primary";
};

export const metricBgColorClass = (metricValue: Number) => {
  if (metricValue >= 80) {
    return "bg-color-danger";
  }
  if (metricValue > 50) {
    return "bg-color-warning";
  }

  return "bg-color-primary";
};

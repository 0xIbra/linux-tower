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

export const stateTextColorClass = (state: String) => {
  if (state === "running") {
    return "text-color-primary";
  }

  return "text-color-danger";
};

export const stateBgColorClass = (state: String) => {
  if (state === "running") {
    return "bg-color-primary";
  }

  return "bg-color-danger";
};

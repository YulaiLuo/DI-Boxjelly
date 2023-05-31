const formatTime = (time) => {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'Australia/Melbourne',
  }).format(time);
};

const calTimeDifference = (timeDifference) => {
  const secondsDifference = Math.floor(timeDifference / 1000);
  const minutesDifference = Math.floor(secondsDifference / 60);
  const hoursDifference = Math.floor(minutesDifference / 60);
  const daysDifference = Math.floor(hoursDifference / 24);

  let formattedTimeDifference;

  if (daysDifference > 365) {
    // Format for years
    const years = Math.floor(daysDifference / 365);
    formattedTimeDifference = `${years} year${years > 1 ? 's' : ''} ago`;
  } else if (daysDifference >= 30) {
    // Format for months
    const months = Math.floor(daysDifference / 30);
    formattedTimeDifference = `${months} month${months > 1 ? 's' : ''} ago`;
  } else if (daysDifference >= 1) {
    // Format for days
    formattedTimeDifference = `${daysDifference} day${daysDifference > 1 ? 's' : ''} ago`;
  } else if (hoursDifference >= 1) {
    // Format for hours
    formattedTimeDifference = `${hoursDifference} hour${hoursDifference > 1 ? 's' : ''} ago`;
  } else {
    // Format for minutes
    formattedTimeDifference = `${minutesDifference} minute${minutesDifference > 1 ? 's' : ''} ago`;
  }
  return formattedTimeDifference;
};

export { formatTime, calTimeDifference };

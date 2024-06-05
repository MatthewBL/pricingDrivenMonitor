import axios from 'axios';

export default function sendActivityData(activityData = window.sessionStorage.getItem('activityData') || '') {
    // If the activityData surpasses a certain threshold, send it to the backend
    if (activityData.length > 0) {
      axios.post('/backend-endpoint', { activityData })
        .then(() => {
          // If the data was sent successfully, clear the activityData from the session
          window.sessionStorage.removeItem('activityData');
        })
        .catch((error) => {
          console.error('Failed to send activityData to the backend:', error);
        });
    }
}
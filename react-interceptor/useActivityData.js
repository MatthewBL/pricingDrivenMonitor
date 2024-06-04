import { useEffect } from 'react';
import sendActivityData from './sendActivityData';

export default function useActivityData() {
  useEffect(() => {
    // Add an event listener for the beforeunload event
    window.addEventListener('beforeunload', () => {
      sendActivityData();
    });

    // Remove the event listener when the component is unmounted
    return () => {
      window.removeEventListener('beforeunload', sendActivityData);
    };
  }, []); // Empty dependency array means this effect runs once on mount and cleanup on unmount
}
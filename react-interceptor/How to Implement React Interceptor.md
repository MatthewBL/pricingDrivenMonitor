## How to Implement the React Interceptor
Follow these steps to implement the React Interceptor in your project:

1. Include the necessary files in your project:

* react-interceptor.js
* sendActivityData.js
* useActivityData.js

Ensure all these files are in the same directory.

2. Use the Axios instance from react-interceptor.js:

* Import the Axios instance from react-interceptor.js in the components where you need to make HTTP requests.
* Use this instance instead of the global axios instance to make requests.

Here's an example:

```javascript
// SomeComponent.js
import React from 'react';
import api from './react-interceptor'; // adjust the path if necessary

function SomeComponent() {
  // Use the Axios instance with interceptors
  api.get('/some-endpoint')
    .then(response => {
      // Handle the response...
    });

  // Rest of the component...
}
```

3. Modify your logout function:

* Import the sendActivityData function from sendActivityData.js in the React component that manages user logout.
* Call the sendActivityData() function in your logout function.

Here's an example:

```javascript
// logout.js
import sendActivityData from './sendActivityData'; // adjust the path if necessary

function logout() {
  // Send the activityData to the backend
  sendActivityData();

  // Rest of the logout function...
}
```

4. Modify your top-level React component:

* Import the useActivityData hook from useActivityData.js.
* Call useActivityData() inside the component.

Here's an example:
```javascript
// App.js
import React from 'react';
import useActivityData from './useActivityData'; // adjust the path if necessary

function App() {
  // Use the custom hook
  useActivityData();

  // Rest of the component...
}
```

By following these steps, you can ensure that user activity data is sent to the backend both when the user logs out and when they close the browser window or tab.
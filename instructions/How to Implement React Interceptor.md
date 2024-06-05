## How to Implement the React Interceptor
Follow these steps to implement the React Interceptor in your project:

1. Include the necessary files in your project:

* react-interceptor.js
* sendActivityData.js
* useActivityData.js
* JwtUtil.java

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

However, to track the user's pricing plan, you need to modify the implementation of the JWT.

### Including the user pricing plan in the JWT

To include the user pricing plan in the JWT, a method named addPricingPlanClaim has been implemented in the JwtUtil class.

The addPricingPlanClaim method is a utility function that adds a custom claim to a JWT (JSON Web Token). This claim is named "pricingPlan" and its value is the pricing plan that you pass to the method.

1. Importing the JwtUtil Class

Before you can use the addPricingPlanClaim method, you need to import the JwtUtil class into your project. If you've packaged the JwtUtil class as a JAR file, you can add it as a dependency in your pom.xml or build.gradle file.

Here's how you can do it in Maven:

```xml
<dependencies>
    <dependency>
        <groupId>com.isa</groupId>
        <artifactId>jwtutil</artifactId>
        <version>1.0.0</version>
        <scope>system</scope>
        <systemPath>${project.basedir}/lib/jwtutil-1.0.0.jar</systemPath>
    </dependency>
</dependencies>
```

Replace ${project.basedir}/lib/jwtutil-1.0.0.jar with the actual path to your JAR file.

After adding the dependency, you can import the JwtUtil class in your Java code like this:

```java
import com.isa.jwtutil.JwtUtil;
```

2. Using the addPricingPlanClaim method

This method is intended to be used during the JWT creation process. After you've created a Claims object and set the subject (usually the username), you can call this method to add the pricing plan to the claims.

Example:

```java
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;

import java.security.Key;
import java.util.Date;

public class JwtGenerator {

    private Key secretKey = Keys.secretKeyFor(SignatureAlgorithm.HS256);

    public String generateTokenWithPricingPlan(String username, String pricingPlan) {
        Claims claims = Jwts.claims().setSubject(username);
        JwtUtil.addPricingPlanClaim(claims, pricingPlan);                             // add this line

        return Jwts.builder()
            .setClaims(claims)
            .setIssuedAt(new Date(System.currentTimeMillis()))
            .setExpiration(new Date(System.currentTimeMillis() + 1000 * 60 * 60 * 10)) // 10 hours token validity
            .signWith(secretKey)
            .compact();
    }
}
```
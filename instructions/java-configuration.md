## Java configuration

### Add the packaged tool as a dependency in your pom.xml or build.gradle file:

Before using any Java functions, you need to install the package using the ```mvn install:install-file``` command:

```shell
mvn install:install-file -Dfile=<path-to-file> -DgroupId=com.isa -DartifactId=pricingdrivenmonitor -Dversion=1.0.0 -Dpackaging=jar
```

After running this command, you can add the library as a dependency in your pom.xml file like this:

```xml
<dependencies>
    <dependency>
        <groupId>com.isa</groupId>
        <artifactId>pricingDrivenMonitor</artifactId>
        <version>1.0.0</version>
    </dependency>
</dependencies>
```

### Including the Spring interceptor in your Spring project

1. Register the interceptor: In Spring, you register an interceptor by adding it to the interceptor registry. You can do this in a configuration class that implements the WebMvcConfigurer interface. Here's an example:
```java
import com.isa.pricingDrivenMonitor.UsageInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new UsageInterceptor());
    }
}
```
In this code, the addInterceptors method adds the UsageInterceptor to the interceptor registry. This makes Spring call the UsageInterceptor for every incoming HTTP request.

2. If your app is ready for production, make sure to set an environment variable NODE_ENV to prevent the interceptor from having an impact on the performance of your system: The UsageInterceptor doesn't monitor the usage if the NODE_ENV environment variable is set to 'production'. You can set this variable in the environment where you run your Spring application. If you're running the application from a command line, you can set the variable like this:
```shell
export NODE_ENV=production
```
If you're running the application from an IDE, you can usually set the environment variable in the run configuration.

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
## How to include the Spring interceptor in your Spring project
1. Add the packaged tool as a dependency in your pom.xml or build.gradle file:

First, you need to install the package using the ```mvn install:install-file``` command:

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

2. Register the interceptor: In Spring, you register an interceptor by adding it to the interceptor registry. You can do this in a configuration class that implements the WebMvcConfigurer interface. Here's an example:
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

3. If your app is ready for production, make sure to set an environment variable NODE_ENV to prevent the interceptor from having an impact on the performance of your system: The UsageInterceptor doesn't monitor the usage if the NODE_ENV environment variable is set to 'production'. You can set this variable in the environment where you run your Spring application. If you're running the application from a command line, you can set the variable like this:
```shell
export NODE_ENV=production
```
If you're running the application from an IDE, you can usually set the environment variable in the run configuration.
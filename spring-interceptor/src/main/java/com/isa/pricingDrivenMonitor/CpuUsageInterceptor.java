package main.java.com.isa.pricingDrivenMonitor;
import java.lang.management.ManagementFactory;
import java.lang.management.OperatingSystemMXBean;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

public class CpuUsageInterceptor implements HandlerInterceptor {

    private OperatingSystemMXBean osBean;

    public CpuUsageInterceptor() {
        osBean = ManagementFactory.getOperatingSystemMXBean();
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        double cpuLoad = osBean.getSystemLoadAverage();
        System.out.println("CPU Load: " + cpuLoad);
    }
}
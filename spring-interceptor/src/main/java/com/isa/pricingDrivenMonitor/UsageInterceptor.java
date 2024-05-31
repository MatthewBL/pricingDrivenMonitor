package com.isa.pricingDrivenMonitor;
import java.lang.management.ManagementFactory;
import java.lang.management.OperatingSystemMXBean;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import java.util.concurrent.atomic.AtomicInteger;

public class UsageInterceptor implements HandlerInterceptor {

    private OperatingSystemMXBean osBean;
    private AtomicInteger concurrentRequests;

    public UsageInterceptor() {
        osBean = ManagementFactory.getOperatingSystemMXBean();
        concurrentRequests = new AtomicInteger(0);
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        concurrentRequests.incrementAndGet();
        double cpuLoadBefore = osBean.getSystemLoadAverage();
        long usedMemoryBefore = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        request.setAttribute("cpuLoadBefore", cpuLoadBefore);
        request.setAttribute("usedMemoryBefore", usedMemoryBefore);
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        double cpuLoadAfter = osBean.getSystemLoadAverage();
        long usedMemoryAfter = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        double cpuLoadBefore = (Double) request.getAttribute("cpuLoadBefore");
        long usedMemoryBefore = (Long) request.getAttribute("usedMemoryBefore");
        double cpuUsage = cpuLoadAfter - cpuLoadBefore;
        long memoryUsage = usedMemoryAfter - usedMemoryBefore;
        String endpoint = request.getRequestURI();
        System.out.println("Endpoint: " + endpoint + ", CPU Usage: " + cpuUsage + ", Memory Usage: " + memoryUsage + ", Concurrent requests: " + concurrentRequests.get());
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        concurrentRequests.decrementAndGet();
    }
}
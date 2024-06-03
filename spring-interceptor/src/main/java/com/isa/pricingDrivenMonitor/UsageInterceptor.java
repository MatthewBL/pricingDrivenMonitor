package com.isa.pricingDrivenMonitor;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.lang.management.ManagementFactory;
import java.lang.management.OperatingSystemMXBean;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import java.nio.file.FileStore;
import java.nio.file.Files;
import java.nio.file.Paths;
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
        long freeSpaceBefore = getFreeSpace();
        request.setAttribute("cpuLoadBefore", cpuLoadBefore);
        request.setAttribute("usedMemoryBefore", usedMemoryBefore);
        request.setAttribute("freeSpaceBefore", freeSpaceBefore);
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        double cpuLoadAfter = osBean.getSystemLoadAverage();
        long usedMemoryAfter = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
        long freeSpaceAfter = getFreeSpace();
        double cpuLoadBefore = (Double) request.getAttribute("cpuLoadBefore");
        long usedMemoryBefore = (Long) request.getAttribute("usedMemoryBefore");
        long freeSpaceBefore = (Long) request.getAttribute("freeSpaceBefore");
        double cpuUsage = cpuLoadAfter - cpuLoadBefore;
        long memoryUsage = usedMemoryAfter - usedMemoryBefore;
        long storageUsage = freeSpaceBefore - freeSpaceAfter;
        String endpoint = request.getRequestURI();
        int concurrentRequestsCount = concurrentRequests.get();
        System.out.println("Endpoint: " + endpoint + ", CPU Usage: " + cpuUsage + ", Memory Usage: " + memoryUsage + ", Storage Usage: " + storageUsage + ", Concurrent requests: " + concurrentRequests.get());
        
        String parentDir = new File(System.getProperty("user.dir")).getParent();
        String filePath = parentDir + "/machine-learning/backend_access_data.csv";

        try (PrintWriter writer = new PrintWriter(new FileWriter(filePath, true))) {
            writer.println(endpoint + "," + cpuUsage + "," + memoryUsage + "," + storageUsage + "," + concurrentRequestsCount);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) throws Exception {
        concurrentRequests.decrementAndGet();
    }

    private long getFreeSpace() throws Exception {
        FileStore fs = Files.getFileStore(Paths.get("."));
        return fs.getUsableSpace();
    }
}
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

public class UsageInterceptor implements HandlerInterceptor {

    private OperatingSystemMXBean osBean;

    public UsageInterceptor() {
        osBean = ManagementFactory.getOperatingSystemMXBean();
    }

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        if (!"production".equals(System.getenv("NODE_ENV"))) {
            double cpuLoadBefore = osBean.getSystemLoadAverage();
            long usedMemoryBefore = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
            long freeSpaceBefore = getFreeSpace();
            request.setAttribute("cpuLoadBefore", cpuLoadBefore);
            request.setAttribute("usedMemoryBefore", usedMemoryBefore);
            request.setAttribute("freeSpaceBefore", freeSpaceBefore);
        }
        return true;
    }
    
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView modelAndView) throws Exception {
        if (!"production".equals(System.getenv("NODE_ENV"))) {
            double cpuLoadAfter = osBean.getSystemLoadAverage();
            long usedMemoryAfter = Runtime.getRuntime().totalMemory() - Runtime.getRuntime().freeMemory();
            long freeSpaceAfter = getFreeSpace();
            double cpuLoadBefore = (Double) request.getAttribute("cpuLoadBefore");
            long usedMemoryBefore = (Long) request.getAttribute("usedMemoryBefore");
            long freeSpaceBefore = (Long) request.getAttribute("freeSpaceBefore");
            double cpuUsage = cpuLoadAfter - cpuLoadBefore;
            long memoryUsage = usedMemoryAfter - usedMemoryBefore;
            long storageUsage = freeSpaceBefore - freeSpaceAfter;
            String requestId = request.getHeader("X-Request-ID"); // Get the requestId from the headers
            System.out.println("Request ID: " + requestId + ", CPU Usage: " + cpuUsage + ", Memory Usage: " + memoryUsage + ", Storage Usage: " + storageUsage);
    
            String parentDir = new File(System.getProperty("user.dir")).getParent();
            String filePath = parentDir + "/machine-learning/training/dataset/backend_access_data.csv";
    
            File file = new File(filePath);
            if (!file.exists()) {
                try (PrintWriter writer = new PrintWriter(new FileWriter(filePath, true))) {
                    writer.println("Request ID,CPU Usage,Memory Usage,Storage Usage");
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
    
            try (PrintWriter writer = new PrintWriter(new FileWriter(filePath, true))) {
                writer.println(requestId + "," + cpuUsage + "," + memoryUsage + "," + storageUsage); // Include the requestId in the CSV
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private long getFreeSpace() throws Exception {
        FileStore fs = Files.getFileStore(Paths.get("."));
        return fs.getUsableSpace();
    }
}
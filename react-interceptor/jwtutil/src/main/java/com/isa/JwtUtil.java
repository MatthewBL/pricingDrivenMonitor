package jwtutil.src.main.java.com.isa;
import io.jsonwebtoken.Claims;

public class JwtUtil {

    public static void addPricingPlanClaim(Claims claims, String pricingPlan) {
        claims.put("pricingPlan", pricingPlan);
    }
}
export function addUserPricingPlan(user, getPricingPlanForUser) {
    // Add the pricing plan to the user object
    user.pricingPlan = getPricingPlanForUser(user);
  
    // Return the modified user object
    return user;
  }
package com.hmdp.controller.interceptor;

import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

import javax.annotation.Resource;

@Configuration
public class MvcConfig implements WebMvcConfigurer {

    @Resource
    StringRedisTemplate stringRedisTemplate;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
//        指定开放链接，不走拦截器的链接
        registry.addInterceptor(new LoginInterceptor(stringRedisTemplate)).excludePathPatterns(
                "/user/code",
                "/user/login",
                "/shop/**",
                "/voucher/**",
                "/shop-type/**",
                "/upload/**",
                "/blog/host"
                );
    }
}

package com.hmdp.utils;

import java.beans.IntrospectionException;
import java.beans.PropertyDescriptor;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

public class MyBeanUtil {
    public static Map<String,String> beanToMap(Object object) throws  InvocationTargetException, IllegalAccessException, IntrospectionException {
        Map<String, String> beanStringMap = new HashMap<>();
        Class<?> aClass = object.getClass();
        Field[] fields = aClass.getDeclaredFields();
        for (int i = 0; i < fields.length; i++) {
            //设置可以访问私有变量
            fields[i].setAccessible(true);
            //获取属性名称
            String name = fields[i].getName();
//            获取属性值
            PropertyDescriptor pd = new PropertyDescriptor(fields[i].getName(), aClass);
            Method getMethod = pd.getReadMethod();
//            传入本身对象作为运行参数
            String value = getMethod.invoke(object).toString();
            beanStringMap.put(name,value);
        }
        return beanStringMap;
    }
}

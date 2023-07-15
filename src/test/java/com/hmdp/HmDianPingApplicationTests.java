package com.hmdp;

import com.hmdp.dto.UserDTO;
import com.hmdp.utils.MyBeanUtil;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import java.beans.IntrospectionException;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.util.Locale;
import java.util.Map;

@SpringBootTest
class HmDianPingApplicationTests {
    @Test
    public void test_1(){
        System.out.println("00000");
    }


    @Test
    public void test_2() throws IntrospectionException, InvocationTargetException, IllegalAccessException {
        UserDTO userDTO = new UserDTO();
        userDTO.setIcon("www");
        userDTO.setId(123L);
        userDTO.setNickName("prxd");
        Map<String, String> stringStringMap = MyBeanUtil.beanToMap(userDTO);
        System.out.println(stringStringMap);
        //遍历所有属性

            }
}

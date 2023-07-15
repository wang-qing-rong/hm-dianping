package com.hmdp.service.impl;

import cn.hutool.core.bean.BeanUtil;
import cn.hutool.core.util.RandomUtil;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.hmdp.dto.LoginFormDTO;
import com.hmdp.dto.Result;
import com.hmdp.dto.UserDTO;
import com.hmdp.entity.User;
import com.hmdp.mapper.UserMapper;
import com.hmdp.service.IUserService;
import com.hmdp.utils.MyBeanUtil;
import com.hmdp.utils.RegexUtils;
import com.hmdp.utils.SystemConstants;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import javax.servlet.http.HttpSession;

import java.beans.IntrospectionException;
import java.lang.reflect.InvocationTargetException;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

import static com.hmdp.utils.SystemConstants.USER_NICK_NAME_PREFIX;

/**
 * <p>
 * 服务实现类
 * </p>
 *
 * @author 虎哥
 * @since 2021-12-22
 */
@Slf4j
@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements IUserService {

    @Resource
    StringRedisTemplate stringRedisTemplate;
    @Override
    public Result getCode(String phone, HttpSession session) {
//        获取手机号
        if (RegexUtils.isPhoneInvalid(phone)) {
            return Result.fail("手机号不符合格式");
        }
        String code = RandomUtil.randomNumbers(6);   //获取6位数验证码
//将验证码存到redis中,code的保存时间设置为2分钟
        stringRedisTemplate.opsForValue().set(SystemConstants.LOGIN_CODE_KEY +phone,code,SystemConstants.LOGIN_CODE_TLL, TimeUnit.MINUTES);
//        返回状态
        log.debug("验证码="+code);
        return Result.ok();
    }

    @Override
    public Result login(LoginFormDTO loginForm, HttpSession session) {
//        获取验证码
        String cacheCode = stringRedisTemplate.opsForValue().get(SystemConstants.LOGIN_CODE_KEY+loginForm.getPhone());
        if (loginForm.getCode()==null||!loginForm.getCode().equals(cacheCode)){
            return Result.fail("验证码不正确");
        }
//        根据电话号码向表中查询是否存在该用户
        User user=query().eq("phone",loginForm.getPhone()).one();
        if (user==null){
//            该用户原本是不存在的，就重新将用户存到数据库中，然后保存在session中
            user=saveUser(loginForm);
        }
//        随机生成登录令牌token
        String token = SystemConstants.LOGIN_USER_KEY+UUID.randomUUID().toString();
//        将user对象转成userDTO
        UserDTO userDTO = BeanUtil.copyProperties(user, UserDTO.class);
        Map<String, String> userMap = null;  //要转换成Map<String String>
        try {
            userMap = MyBeanUtil.beanToMap(userDTO);
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        } catch (IntrospectionException e) {
            e.printStackTrace();
        }
        stringRedisTemplate.opsForHash().putAll(token,userMap);
//        设置存放时间
        stringRedisTemplate.expire(token,SystemConstants.LOGIN_TOKEN_TLL,TimeUnit.MINUTES);
        return Result.ok(token);  //返回令牌到前端
    }

    private User saveUser(LoginFormDTO loginForm) {
        User user = new User();
        user.setPhone(loginForm.getPhone());  //保存电话号码
        user.setNickName(USER_NICK_NAME_PREFIX+RandomUtil.randomString(10)); //保存用户尼称
        save(user);//保存用户信息
        return user;
    }
}

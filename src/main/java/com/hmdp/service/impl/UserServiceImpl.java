package com.hmdp.service.impl;

import cn.hutool.core.util.PhoneUtil;
import cn.hutool.core.util.RandomUtil;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.hmdp.dto.LoginFormDTO;
import com.hmdp.dto.Result;
import com.hmdp.entity.User;
import com.hmdp.mapper.UserMapper;
import com.hmdp.service.IUserService;
import com.hmdp.utils.RegexUtils;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpSession;

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
    @Override
    public Result getCode(String phone, HttpSession session) {
//        获取手机号
        if (RegexUtils.isPhoneInvalid(phone)) {
            return Result.fail("手机号不符合格式");
        }
        String code = RandomUtil.randomNumbers(6);   //获取6位数验证码
//将验证码存到session域中
        session.setAttribute("code",code);
//        返回状态
        log.debug("验证码="+code);
        return Result.ok();
    }

    @Override
    public Result login(LoginFormDTO loginForm, HttpSession session) {
//        验证登录用户
        String cacheCode = (String) session.getAttribute("code");
        if (loginForm.getCode()==null||!loginForm.getCode().equals(cacheCode)){
            return Result.fail("验证码不正确");
        }
//        向表中查询是否存在该用户
        User user=query().eq("phone",loginForm.getPhone()).one();
        if (user==null){
//            该用户原本是不存在的，就重新将用户存到数据库中，然后保存在session中
            user=saveUser(loginForm);
        }
        session.setAttribute("user",user);
        return Result.ok();
    }

    private User saveUser(LoginFormDTO loginForm) {
        User user = new User();
        user.setPhone(loginForm.getPhone());  //保存电话号码
        user.setNickName(USER_NICK_NAME_PREFIX+RandomUtil.randomString(10)); //保存用户尼称
        save(user);//保存用户信息
        return user;
    }
}
